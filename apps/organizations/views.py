from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from apps.operations.models import UserFavorite, UserAsk
from apps.organizations.models import CourseOrg, City, Teacher

from django.http import JsonResponse
from apps.organizations.forms import AddAskForm
from pure_pagination import Paginator, PageNotAnInteger

from apps.users.models import UserProfile

import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header

import time


# 用于构建邮件头


class SubmitVIP(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        if request.user.ask_numb > 1:
            # 发信方的信息：发信邮箱，QQ 邮箱授权码
            from_addr = '4868569@qq.com'
            password = 'kzwfkfgsdxhgbjbf'

            # 收信方邮箱
            to_addr = '86568954@qq.com'

            # 发信服务器
            smtp_server = 'smtp.qq.com'

            # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
            msg = MIMEText(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), 'plain', 'utf-8')

            # 邮件头信息
            msg['From'] = Header(from_addr)
            msg['To'] = Header(to_addr)
            msg['Subject'] = Header(request.user.username)

            # 开启发信服务，这里使用的是加密传输
            server = smtplib.SMTP_SSL(host=smtp_server)
            server.connect(smtp_server, 465)
            # 登录发信邮箱
            server.login(from_addr, password)
            # 发送邮件
            server.sendmail(from_addr, to_addr, msg.as_string())
            # 关闭服务器
            server.quit()
            i = request.user.ask_numb
            a = i - 1
            request.user.ask_numb = a
            request.user.save()

            teacher = Teacher.objects.get(id=int(4))
            msg = "信息已经提交成功！订单正在审核中，付款后3分钟左右自动开通哟！  有疑问请联系官方邮箱" + teacher.work_company
            return render(request, "submit-vip.html", {
                "msg": msg
            })
        else:
            teacher = Teacher.objects.get(id=int(4))
            msg = "提交失败，您的账户有风险请把您的付款页面截图以及您的账号名发给官方邮箱：" + teacher.work_company + " 管理员会及时处理的哟"
            return render(request, "submit-vip.html", {
                "msg": msg
            })


class OpenYVIP(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        alipay = Teacher.objects.get(id=int(5))
        wechat = Teacher.objects.get(id=int(7))
        return render(request, "open-yvip.html", {
            "alipay": alipay,
            "wechat": wechat
        })


class OpenNVIP(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        alipay = Teacher.objects.get(id=int(4))
        wechat = Teacher.objects.get(id=int(6))
        return render(request, "open-nvip.html", {
            "alipay": alipay,
            "wechat": wechat
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True

        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "org_fav": org_fav,
            "teacher_fav": teacher_fav,
            "hot_teachers": hot_teachers
        })


class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        # 对讲师进行排序
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        # 对讲师机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, per_page=5, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "teachers": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "hot_teachers": hot_teachers
        })


# 机构介绍
class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


# 机构课程
class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_courses = course_org.course_set.all()
        all_courses = all_courses.order_by("-click_nums")

        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "new":
            all_courses = all_courses.order_by("-add_time")
        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


            # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, per_page=9, request=request)

        course = p.page(page)
        return render(request, "org-detail-desc.html", {
            "all_courses": course,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
            "sort": sort,
        })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


class AddAskView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        return render(request, 'add-ask-view.html')

    """
    处理用户的咨询
    """

    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            # userask_form.save(commit=True)
            ask_numb = request.user.ask_numb
            if ask_numb > 1:

                userask = UserAsk(name=request.user.username)
                userask.mobile = userask_form.cleaned_data.get("mobile")
                userask.course_name = userask_form.cleaned_data.get("course_name")
                userask.save()

                # user = UserProfile(username=request.user.username)
                # i = user.ask_numb
                # user.ask_numb = i - 1
                # print(i)
                # user.save()
                i = request.user.ask_numb
                a = i - 1
                request.user.ask_numb = a
                request.user.save()
                return JsonResponse({
                    "status": "success"
                })
            else:
                return JsonResponse({
                    "status": "fail",
                    "msg": "您的账号出现异常，请联系管理员"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


class OrgView(View):
    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        # 课程机构排名
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 对课程机构进行筛选
        category = request.GET.get("ct", "")

        if category:
            all_orgs = all_orgs.filter(category=category)

        # 通过所在城市进行筛选
        city_id = request.GET.get("city", "")
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")
        org_nums = all_orgs.count()
        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, per_page=5, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_nums": org_nums,
            "all_citys": all_citys,
            "category": category,
            "city_id": city_id,
            "sort": sort,
            "hot_orgs": hot_orgs,
        })
