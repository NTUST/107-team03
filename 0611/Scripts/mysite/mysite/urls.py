"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from NightView import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	url(r'^index/', views.index),
    url(r'^foodmap/(\d+)', views.foodmap),
    url(r'^foodmap/add/(\d+)/(\w+)', views.add_f),
    url(r'^nightview/(\d+)', views.nightview),
    url(r'^nightview/add/(\d+)/(\w+)', views.add_n),
    url(r'^mytrip/(\w+)', views.mytrip),
    url(r'^clean/(\w+)', views.cleantrip),
	url(r'^logout/', views.logout),
    url(r'^admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()