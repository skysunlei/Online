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
from apps.users.forms import LoginForm, ChangePwdForm, DynamicLoginForm

from apps.users.models import UserProfile


# 配置消息未读全局变量
def message_nums(request):
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class IndexTestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index-test.html")


# 网站公告
class NoticeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "notice.html")


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
        # current_page = "mycourse"
        my_courses = UserCourse.objects.filter(user=request.user)[:12]
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass

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

        p = Paginator(messages, per_page=5, request=request)

        messages = p.page(page)

        return render(request, "usercenter-info.html", {
            "my_courses": my_courses,
            "current_page": current_page,
            "course_list": course_list,
            "messages": messages

        })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        login_form = DynamicLoginForm()
        all_courses = Course.objects.order_by("-add_time")[:3]
        return render(request, "register.html", {
            "all_courses":all_courses,
            "login_form": login_form,

        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginForm()
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_is_valid = UserProfile.objects.filter(username=username)

        if user_is_valid.count() != 0:
            return render(request, "register.html", {
                "msg": "用户名已存在", "login_form": login_form
            })
        else:
            user = UserProfile(username=username)
            user.set_password(password)
            user.mobile = "11111111111"
            user.nick_name = username
            user.address = "默认"
            user.gender = "male"
            user.is_VIP = False
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            # return render(request, "register.html",{
            #     "msg": "用户名不存在或密码错误"
            # })


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        all_courses = Course.objects.order_by("-add_time")[:3]
        dynamicloginform = DynamicLoginForm()
        return render(request, "index-test.html", {
            "next": next,
            "dynamicloginform": dynamicloginform,
            "all_courses": all_courses,

        })

    def post(self, request, *args, **kwargs):
        dynamicloginform = DynamicLoginForm()
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
                return render(request, "index-test.html",
                              {"msg": "用户名不存在或密码错误", "login_form": login_form, "dynamicloginform": dynamicloginform})
        else:
            return render(request, "index-test.html", {"login_form": login_form, "dynamicloginform": dynamicloginform})
