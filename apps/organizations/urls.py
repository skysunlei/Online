from django.conf.urls import url

from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView, \
    TeacherListView, TeacherDetailView, OpenYVIP, OpenNVIP, SubmitVIP

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="list"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    url(r'^(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="home"),
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name="desc"),
    url(r'^vip/$', TeacherListView.as_view(), name="vip"),
    url(r'^nvip/$', OpenNVIP.as_view(), name="nvip"),
    url(r'^yvip/$', OpenYVIP.as_view(), name="yvip"),
    url(r'^submit_vip/$', SubmitVIP.as_view(), name="submit_vip"),
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
