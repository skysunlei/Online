from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operations.models import UserFavorite, UserCourse, CourseComments
import requests
from apps.users.models import UserProfile
import re


class VideoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        """
        获取课程章节详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # 查询客户是否已经关联课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        video = Video.objects.get(id=int(video_id))
        # 学习过该课程的所有学生
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        # 课程资源下载
        course_resources = CourseResource.objects.filter(course=course)

        # 获取视频资源
        agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        header = {
            "Host": "weibo.com",
            # "Referer": "https://weibo.com/tv/v/Ig92m5Vqy?fid=1034:4438479548141050",
            "Referer": video.url,
            "User-Agent": agent,
            "Cookie": "SINAGLOBAL=9674389647084.594.1579611267612; SCF=AjGepE5Zsp90usSe0y7VWIzT1ms08Z4xPkisgPWubY6yz5xPhePegZiBlLswHW0kGSbch2cFGVOdhQl0fIOHero.; SUHB=0OMkiw7z2HH7Ki; ALF=1611147342; YF-V5-G0=4e19e5a0c5563f06026c6591dbc8029f; SUB=_2AkMpZGVSf8NxqwJRmfwdz2Lgbo10yA3EieKfOJSJJRMxHRl-yT92qhEetRB6AuRLvUXY1ClSGEp5Tte-m9_VOzlbwJya; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFYOsGaOd4DmT.RdqwG2bDR; login_sid_t=98a544eb9a4c8f6508b3484d7de56e7a; cross_origin_proto=SSL; Ugrow-G0=9ec894e3c5cc0435786b4ee8ec8a55cc; WBStorage=42212210b087ca50|undefined; wb_view_log=2560*14401; _s_tentry=passport.weibo.com; Apache=8735107876994.117.1580788331237; ULV=1580788331249:2:1:1:8735107876994.117.1580788331237:1579611267626"

        }
        video_url = video.url
        # response = requests.get("https://weibo.com/tv/v/Ig92m5Vqy?fid=1034:4438479548141050", headers=header)
        response = requests.get(video_url, headers=header)
        r = response.text

        # d = re.findall(r"001kCDEJlx07yzHzQKHm01041201iZAQ0E010.mp4(.+?)KID", r)
        video_name = video.video_name
        s = video_name + "(.+?)KID"
        d = re.findall(s, r)
        c = d[0]
        ssig = re.findall(r"ssig%3D(.+?)%26", c)[0]
        expires = re.findall(r"Expires%3D(.+?)%26", c)[0]
        new = ssig.replace("%25", "%")
        # url = "https://f.video.weibocdn.com/001kCDEJlx07yzHzQKHm01041201iZAQ0E010.mp4?label=mp4_720p&template=960x720.25.0&trans_finger=721584770189073627c6ee9d880087b3&Expires=" + expires + "&ssig=" + new + "&KID=unistore,video"
        url = "https://f.video.weibocdn.com/" + video_name + "?label=mp4_720p&template=960x720.25.0&trans_finger=721584770189073627c6ee9d880087b3&Expires=" + expires + "&ssig=" + new + "&KID=unistore,video"

        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video,
            "url": url

        })


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course).order_by("-add_time")
        # 查询客户是否已经关联课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()
        # 学习过该课程的所有学生
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        is_VIP = request.user.is_VIP

        if is_VIP is True:
            # 课程资源下载
            course_resources = CourseResource.objects.filter(course=course)
            user_is_vip = "true"
            return render(request, "course-comment.html", {
                "course": course,
                "course_resources": course_resources,
                "related_courses": related_courses,
                "user_is_vip": user_is_vip,
                "comments": comments,

            })

        else:
            user_is_vip = "false"
            # 课程资源下载
            return render(request, "course-comment.html", {
                "course": course,
                "related_courses": related_courses,
                "user_is_vip": user_is_vip,
                "comments": comments,

            })

            # return render(request, "course-comment.html", {
            #     "course": course,
            #     "course_resources": course_resources,
            #     "related_courses": related_courses,
            #     "comments": comments
            #
            # })


# Create your views here.
class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # 查询客户是否已经关联课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()
        # 学习过该课程的所有学生
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        comments = CourseComments.objects.filter(course=course)
        comments_count = comments.count()
        is_VIP = request.user.is_VIP

        if is_VIP is True:
            course_resources = CourseResource.objects.filter(course=course)
            user_is_vip = "true"
            return render(request, "course-video.html", {
                "course": course,
                "course_resources": course_resources,
                "related_courses": related_courses,
                "user_is_vip": user_is_vip,
                "comments_count": comments_count

            })

        else:
            user_is_vip = "false"
            # 课程资源下载
            return render(request, "course-video.html", {
                "course": course,
                "related_courses": related_courses,
                "user_is_vip": user_is_vip,
                "comments_count": comments_count

            })


class CourseDetailCommentsView(View):
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course).order_by("-add_time")
        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        # 通过课程的tag做课程的推荐
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     related_courses = Course.objects.filter(tag=tag).exclude(id=course.id)[:3]
        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)
        return render(request, "course-detail-comment.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
            "comments": comments
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)
        comments_count = comments.count()
        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        # 通过课程的tag做课程的推荐
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     related_courses = Course.objects.filter(tag=tag).exclude(id=course.id)[:3]
        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)
        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
            "comments_count": comments_count
        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """获取课程列表信息"""
        all_courses = Course.objects.order_by("-add_time")
        # 课程推荐
        hot_courses = Course.objects.order_by("-click_nums")[:3]
        # 对课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")
        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, per_page=9, request=request)

        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses
        })
