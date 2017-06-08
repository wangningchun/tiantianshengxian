from django.conf.urls import url
import views

urlpatterns = [
    url(r'^add(\d+)_(\d*)/$', views.add),
    url(r'^cart/$',views.cart),
    url(r'^count_change/$',views.count_change),
    url(r'^delete/$',views.delete),
    url(r'place_order/$',views.place_order),


]