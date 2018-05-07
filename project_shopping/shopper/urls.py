from django.conf.urls import url

from shopper import views

urlpatterns = [
    url(r'^home/',views.home),
    url(r'^login/',views.login),
    url(r'^regist/',views.regist),
    url(r'^logout/',views.logout)
]