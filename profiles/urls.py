from django.conf.urls import patterns, include, url
from  . import views
import pdb


urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^facebook/', views.facebook, name='facebook'),
	url(r'^logout/', views.logout, name='logout'),
	url(r'^complete_signup/(?P<pk>\d+)/', views.CompleteSignupView.as_view(), name='complete_signup'),

)
