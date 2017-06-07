from django.conf.urls import url
import views

urlpatterns = [
    url(r'^add(\d+)_(\d*)/$', views.add),
    url(r'^cart/$',views.cart),
    url(r'^cartadd(\d+)/$',views.cartadd),
    url(r'^cartminus(\d+)/$',views.cartminus),
    url(r'^delete(\d+)/$',views.delete),


]