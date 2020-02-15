"""Online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.urls import path
from apps.users.views import LoginView, LogoutView, RegisterView, NoticeView
from django.views.static import serve
from Online.settings import MEDIA_ROOT
from apps.operations.views import IndexView
import xadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('notice/', NoticeView.as_view(), name="notice"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    url(r'^captcha/', include('captcha.urls')),
    # 配置上传文件的访问url
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^org/', include(('apps.organizations.urls', "organizations"), namespace="org")),
    url(r'^course/', include(('apps.courses.urls', "courses"), namespace="course")),
    url(r'^op/', include(('apps.operations.urls', "operations"), namespace="op")),
    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]
