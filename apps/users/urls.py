from django.conf.urls import url

from apps.users.views import UserInfoView, ChangePwdView, MyCourseView, MyFavOrgView, MyFavCourseView, MyMessageView, \
    IndexTestView

urlpatterns = [
    url(r'^list/$', UserInfoView.as_view(), name="info"),
    url(r'^update/pwd/$', ChangePwdView.as_view(), name="update_pwd"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    url(r'^myfavorg/$', MyFavOrgView.as_view(), name="myfavorg"),
    url(r'^myfav_course/$', MyFavCourseView.as_view(), name="myfav_course"),
    url(r'^messages/$', MyMessageView.as_view(), name="messages"),
    url(r'^index/$', IndexTestView.as_view(), name="test"),
]
