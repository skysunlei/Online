from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operations.models import UserFavorite, UserCourse, CourseComments
import requests

from apps.organizations.models import Teacher
from apps.users.models import UserProfile
import re
import datetime


class FreeVideoView(View):
    def get(self, request, course_id, video_id, *args, **kwargs):
        """
        获取课程章节详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        video = Video.objects.get(id=int(video_id))
        # 学习过该课程的所有学生
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        course_resources = CourseResource.objects.filter(course=course)
        teacher = Teacher.objects.get(id=(course.learn_times))

        # 获取视频资源
        agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        header = {
            "Host": "www.hzzlgy.cn",
            "Referer": video.video_name,
            "User-Agent": agent,
            "Cookie": "csrftoken=kdzOQtfsZtiMG1NX2BBE4zx30KyXz0YuifeQ7KuBdxgNKi4Q4Kf1V8iLC1BrXSaJ; sessionid=yhq9ieyk6ree78ozzuzmunu7ybwwnquj"

        }
        response = requests.get(video.url, headers=header)

        r = response.text

        d = re.findall("https://f.video.weibocdn.com/(.+?)KID", r)

        e = d[0]

        c = e.replace("&amp;", "&")
        url = "https://f.video.weibocdn.com/" + c + "KID=unistore,video"

        return render(request, "course-free-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video,
            "url": url,
            "teacher":teacher

        })


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
        if video.url == "none":
            return render(request, "course-play-benfeng.html", {
                "course": course,
                "course_resources": course_resources,
                "related_courses": related_courses,
            })

        cookies = Teacher.objects.get(id=int(7))

        # 获取视频资源
        # agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        # header = {
        #     "Host": "weibo.com",
        #     # "Referer": "https://weibo.com/tv/v/Ig92m5Vqy?fid=1034:4438479548141050",
        #     "Referer": video.url,
        #     "User-Agent": agent,
        #     "Cookie": cookies.points
        # }
        # video_url = video.url
        #
        # response = requests.get(video_url, headers=header)
        # r = response.text
        #
        # video_name = video.video_name
        # s = video_name + "(.+?)KID"
        # d = re.findall(s, r)
        # c = d[0]
        # ssig = re.findall(r"ssig%3D(.+?)%26", c)[0]
        # expires = re.findall(r"Expires%3D(.+?)%26", c)[0]
        # new = ssig.replace("%25", "%")
        #
        # # url = "https://f.video.weibocdn.com/001kCDEJlx07yzHzQKHm01041201iZAQ0E010.mp4?label=mp4_720p&template=960x720.25.0&trans_finger=721584770189073627c6ee9d880087b3&Expires=" + expires + "&ssig=" + new + "&KID=unistore,video"
        # url = "https://f.video.weibocdn.com/" + video_name + "?label=mp4_720p&template=960x720.25.0&trans_finger=721584770189073627c6ee9d880087b3&Expires=" + expires + "&ssig=" + new + "&KID=unistore,video"
        # # url = "https://f.video.weibocdn.com/002rJVj8gx07B6rI753O01041204EKCy0E020.mp4?label=mp4_720p&template=960x720.25.0&trans_finger=721584770189073627c6ee9d880087b3&Expires=1584091647&ssig=I%2BUuMLJP8%2B&KID=unistore,video"

        # 获取视频资源
        agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        header = {
            "Host": "www.hzzlgy.cn",
            "Referer": video.video_name,
            "User-Agent": agent,
            "Cookie": "sessionid=xbt2fra3u43y42dnxwj8tlc185hhbpi5; csrftoken=aOEJdHNmq7l4AMcr0lzPS1QqYSQv7ridgDfDENyCgd63iu26PHJ3plRkp0Q8bcwb"

        }
        response = requests.get(video.url, headers=header)

        r = response.text

        d = re.findall("https://f.video.weibocdn.com/(.+?)KID", r)

        e = d[0]

        c = e.replace("&amp;", "&")
        url = "https://f.video.weibocdn.com/" + c + "KID=unistore,video"

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
        is_nianVIP = request.user.is_nian_VIP

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(comments, per_page=9, request=request)

        detailcomment = p.page(page)

        if is_VIP is True:
            # 课程资源下载
            course_resources = CourseResource.objects.filter(course=course)
            user_is_vip = "true"
            user_is_nianVIP = "flase"
            return render(request, "course-comment.html", {
                "course": course,
                "course_resources": course_resources,
                "related_courses": related_courses,
                "user_is_vip": user_is_vip,
                "comments": comments,
                "detailcomment": detailcomment,
                "user_is_nianVIP": user_is_nianVIP

            })

        else:
            if is_nianVIP is True:
                course_resources = CourseResource.objects.filter(course=course)
                user_is_nianVIP = "true"
                user_is_vip = "false"
                return render(request, "course-comment.html", {
                    "course": course,
                    "course_resources": course_resources,
                    "related_courses": related_courses,
                    "user_is_vip": user_is_vip,
                    "user_is_nianVIP": user_is_nianVIP,
                    "comments": comments,
                    "detailcomment": detailcomment,

                })

            user_is_vip = "false"
            user_is_nianVIP = "flase"
            # 课程资源下载
            return render(request, "course-comment.html", {
                "course": course,
                "related_courses": related_courses,
                "user_is_vip": user_is_vip,
                "comments": comments,
                "user_is_nianVIP": user_is_nianVIP,
                "detailcomment": detailcomment,

            })

            # return render(request, "course-comment.html", {
            #     "course": course,
            #     "course_resources": course_resources,
            #     "related_courses": related_courses,
            #     "comments": comments
            #
            # })


class FreeLessonView(View):
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        related_courses = [user_course.course for user_course in all_courses if
                           user_course.course.id != course.id]  # Create your views here.
        comments = CourseComments.objects.filter(course=course)
        comments_count = comments.count()
        user_is_vip = "true"
        user_is_nianVIP = "true"
        # 课程资源下载


        teacher = Teacher.objects.get(id=(course.learn_times))

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-free-video.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "user_is_vip": user_is_vip,
            "comments_count": comments_count,
            "user_is_nianVIP": user_is_nianVIP,
            "comments": comments,
            "teacher":teacher


        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # a=datetime.date.today()
        # request.user.birthday = a
        # request.user.save()
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
        is_nianVIP = request.user.is_nian_VIP

        if is_VIP is True:
            a = datetime.date.today()
            if request.user.birthday != a:
                request.user.birthday = a
                request.user.request_numb = 1
                request.user.save()
            else:
                if request.user.request_numb > 20:
                    teacher = Teacher.objects.get(id=int(4))
                    msg = "您的账户有风险请把您的账号名发给官方邮箱：" + teacher.work_company + " 管理员会及时处理的哟!    温馨提示：请不要随意把账号分享给别人，异地登录可能会触发封号系统"
                    return render(request, "submit-vip.html", {
                        "msg": msg
                    })

            course_resources = CourseResource.objects.filter(course=course)
            user_is_vip = "true"
            user_is_nianVIP = "flase"
            request.user.request_numb += 1
            request.user.save()
            return render(request, "course-video.html", {
                "course": course,
                "course_resources": course_resources,
                "related_courses": related_courses,
                "user_is_vip": user_is_vip,
                "comments_count": comments_count,
                "user_is_nianVIP": user_is_nianVIP

            })


        else:
            if is_nianVIP is True:

                a = datetime.date.today()
                if request.user.birthday != a:
                    request.user.birthday = a
                    request.user.request_numb = 1
                    request.user.save()
                else:
                    if request.user.request_numb > 20:
                        teacher = Teacher.objects.get(id=int(4))
                        msg = "您的账户有风险请把您的账号名发给官方邮箱：" + teacher.work_company + " 管理员会及时处理的哟!    温馨提示：请不要随意把账号分享给别人，异地登录可能会触发封号系统"
                        return render(request, "submit-vip.html", {
                            "msg": msg
                        })

                course_resources = CourseResource.objects.filter(course=course)
                user_is_nianVIP = "true"
                user_is_vip = "false"
                return render(request, "course-video.html", {
                    "course": course,
                    "course_resources": course_resources,
                    "related_courses": related_courses,
                    "user_is_vip": user_is_vip,
                    "comments_count": comments_count,
                    "user_is_nianVIP": user_is_nianVIP

                })

            user_is_vip = "false"
            user_is_nianVIP = "flase"
            # 课程资源下载
            return render(request, "course-video.html", {
                "course": course,
                "related_courses": related_courses,
                "user_is_vip": user_is_vip,
                "comments_count": comments_count,
                "user_is_nianVIP": user_is_nianVIP

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
        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(comments, per_page=9, request=request)

        detailcomment = p.page(page)
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
            "comments": comments,
            "detailcomment": detailcomment
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
        all_courses = Course.objects.order_by("-add_time")[:27]
        # # 课程推荐
        # hot_courses = Course.objects.order_by("-click_nums")[:3]
        keywords = request.GET.get("keywords", "")
        if keywords:
            all_courses = Course.objects.filter(name__icontains=keywords)
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
            # "hot_courses": hot_courses
            "keywords": keywords
        })
