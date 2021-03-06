from django.conf.urls import url

from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentsView, VideoView, \
    CourseDetailCommentsView, FreeLessonView, FreeVideoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^(?P<course_id>\d+)/course/$', CourseDetailView.as_view(), name="detail"),
    url(r'^(?P<course_id>\d+)/lesson/$', CourseLessonView.as_view(), name="lesson"),
    url(r'^(?P<course_id>\d+)/freelesson/$', FreeLessonView.as_view(), name="freelesson"),
    url(r'^(?P<course_id>\d+)/comments/$', CourseCommentsView.as_view(), name="comments"),
    url(r'^(?P<course_id>\d+)/freevideo/(?P<video_id>\d+)$', VideoView.as_view(), name="video"),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', FreeVideoView.as_view(), name="freevideo"),
    url(r'^(?P<course_id>\d+)/detail-comments/$', CourseDetailCommentsView.as_view(), name="detail_comments"),

]
