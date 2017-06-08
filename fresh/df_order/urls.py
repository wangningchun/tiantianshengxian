from django.conf.urls import url
import views

urlpatterns = [
    url(r'order/$',views.order),
]