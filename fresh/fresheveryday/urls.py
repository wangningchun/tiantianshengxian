from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^register/$',views.register),
    url(r'^login/$',views.login),
    url(r'^cart/$',views.cart),
    url(r'^detail/$',views.detail),
    url(r'^list/$', views.list),
    url(r'^login/$', views.login),
    url(r'^place_order/$', views.place_order),
    url(r'^user_center_info/$', views.user_center_info),
    url(r'^user_center_order/$', views.user_center_order),
    url(r'^user_center_site/$', views.user_center_site),
    url(r'^pic_handle/$',views.pic_handle),
    url(r'^pic_handle1/$',views.pic_handle1),
    url(r'^pic_handle2/$', views.pic_handle2),
    url(r'^loginout/$',views.loginout),
    url(r'^register1/$',views.register1),
]
