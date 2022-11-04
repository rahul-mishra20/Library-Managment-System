from django.urls import path
from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.userlogin,name='login'),
    path('logout',views.userlogout,name='logout'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    path('library',views.library,name='library'),
    path('contact',views.contact,name='contact'),
    path('test',views.test,name='test'),
]