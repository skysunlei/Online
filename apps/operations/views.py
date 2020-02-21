from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from apps.courses.models import Course
from apps.operations.models import UserFavorite, CourseComments, Banner
from apps.operations.forms import UserFavForm, CommentsForm
from django.http import JsonResponse

from apps.organizations.models import CourseOrg, Teacher

from django.contrib.auth.mixins import LoginRequiredMixin

from apps.users.models import UserProfile


# 首页开发
class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_banner=False)[:8]
        banner_courses = Course.objects.filter(is_banner=True)
        course_orgs = CourseOrg.objects.all()[:15]

        android = CourseOrg.objects.get(id=1)
        web = CourseOrg.objects.get(id=2)
        php = CourseOrg.objects.get(id=3)
        java = CourseOrg.objects.get(id=4)
        wechat = CourseOrg.objects.get(id=5)
        c = CourseOrg.objects.get(id=6)
        python = CourseOrg.objects.get(id=7)
        ios = CourseOrg.objects.get(id=8)
        net = CourseOrg.objects.get(id=9)
        database = CourseOrg.objects.get(id=10)
        bigdata = CourseOrg.objects.get(id=11)
        mstudy = CourseOrg.objects.get(id=12)
        xitong = CourseOrg.objects.get(id=13)
        heike = CourseOrg.objects.get(id=14)
        ps = CourseOrg.objects.get(id=15)
        morelangue = CourseOrg.objects.get(id=16)
        ebook = CourseOrg.objects.get(id=17)
        ui = CourseOrg.objects.get(id=19)
        yingyin = CourseOrg.objects.get(id=21)
        other_design = CourseOrg.objects.get(id=20)
        return render(request, "index.html", {
            "banners": banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,

            "android": android,
            "web": web,
            "php": php,
            "java": java,
            "wechat": wechat,
            "c": c,
            "python": python,
            "ios": ios,
            "net": net,
            "database": database,
            "bigdata": bigdata,
            "mstudy": mstudy,
            "xitong": xitong,
            "heike": heike,
            "ps": ps,
            "morelangue": morelangue,
            "ebook": ebook,
            "ui": ui,
            "yingyin": yingyin,
            "other_design": other_design

        })


class ShareView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        if request.user.is_VIP is True:
            return render(request, "share.html")
        elif request.user.is_nian_VIP is True:
            return render(request, "share.html")
        else:
            return render(request, "teachers-list.html")


class CommentView(View):
    def post(self, request, *args, **kwargs):
        # 判断用户是否登陆
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


class AddFavView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏
        :param request:
        :param org_id:
        :param args:
        :param kwargs:
        :return:
        """

        # 判断用户是否登陆
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })
        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            # 判断是不是已经收藏如果是就执行取消收藏操作
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()

                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.user = request.user
                user_fav.fav_type = fav_type
                user_fav.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })
