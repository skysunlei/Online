from pure_pagination import Paginator, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.courses.models import Course
from apps.operations.models import UserCourse, UserFavorite, UserMessage
from apps.organizations.models import CourseOrg
from apps.users.forms import LoginForm, ChangePwdForm


# 配置消息未读全局变量
def message_nums(request):
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class IndexTestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index-test.html")


# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "message"
        messages = UserMessage.objects.filter(user=request.user)
        for message in messages:
            message.has_read = True
            message.save()
        # 对讲师机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(messages, per_page=1, request=request)

        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page
        })


# 我的收藏课程
class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass

        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            "current_page": current_page
        })


# 我的收藏机构
class MyFavOrgView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavorg"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
            "current_page": current_page
        })


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "mycourse"
        my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "my_courses": my_courses,
            "current_page": current_page
        })


# 更改密码
class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return JsonResponse({
                    "status": "fail",
                    "msg": "密码不一致"
                })
            user = request.user
            user.set_password(pwd1)
            user.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "info"
        return render(request, "usercenter-info.html", {
            "current_page": current_page
        })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
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
        course_orgs = CourseOrg.objects.all()[:4]
        return render(request, "index-test.html", {
            "next": next,
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
            "morelangue": morelangue
        })

    def post(self, request, *args, **kwargs):

        # 表单验证
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)

            if user is not None:
                login(request, user)
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名不存在或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})
