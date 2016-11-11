"""IRProjectEnv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

from irproject import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='Login'),
    url(r'^signup/$', views.signup, name='Sign Up'),
    url(r'^logout/$', views.logout, name='Logout'),
    url(r'^home/$', views.home, name='Home'),
    url(r'^friendrequests/$', views.friendrequests, name='Friend Requests'),
    url(r'^receivedqueries/$', views.receivedqueries, name='Received Queries'),
    url(r'^askedqueries/$', views.receivedqueries, name='Asked Queries'),
    url(r'^addtopics/$', views.addtopics, name='Add Topics'),
    url(r'^addfriend/(?P<receiver>[a-zA-Z0-9]+)/$', views.addfriend, name='Add Friend'),
    url(r'^acceptfriend/(?P<sender>[a-zA-Z0-9]+)/$', views.acceptfriend, name='Accept Friend'),
    url(r'^query/(?P<id>\d+)/$', views.queries, name='Queries'),
    #url(r'^$', include('irproject.urls'), name="ir"),
]
