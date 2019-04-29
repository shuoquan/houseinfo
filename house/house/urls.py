"""house URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
import sechouse.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',sechouse.views.index,name="index"),
    path('houseinfo/',sechouse.views.info,name="houseinfo"),
    path('houseinfo/getdata',sechouse.views.showtable,name="getdata"),
    path('sechouseinfo/',sechouse.views.showsecinfo,name="sechouseinfo"),
    path('sechouseinfo/query/',sechouse.views.filter,name="query"),
    path('housenum/',sechouse.views.housenum),
    path('renthouse/',sechouse.views.renthouse),
    path('sechouse/', sechouse.views.sechouse),
    path('getrenthouse/',sechouse.views.getrenthouse),
    path('getsechouse/', sechouse.views.getsechouse),
    # path('houseinfo/getdata',sechouse.views.),
]
