from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^techlab/about/$', views.about, name='about'),
    url(r'^techlab/contact/$', views.contact, name='contact'),
]
