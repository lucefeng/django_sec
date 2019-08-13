"""django_sec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django_learn1.views import *
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', login),
    url(r"^$", index),#空字符地址
    url(r'^page',page),
    url(r'(^\d+)',show),
    url(r'^register',register),
    url(r'^get_valid_img.png',get_valid_img),
    url(r'^content',content),
    url(r'^delivery',delivery),
    url(r'^logout',logout),
    url(r'^index',index),
    url(r'^pdf_read',pdf_read),
    url(r'^pdfshow',pdf_show),
    url(r'^pdf_first',pdf_first),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^haha',return_form)

]
