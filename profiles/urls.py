from django.conf.urls import patterns, include, url
from  . import views
import pdb
# from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^facebook/', views.facebook, name='facebook'),
	url(r'^logout/', views.logout, name='logout'),
	url(r'^complete_signup/(?P<pk>\d+)/', views.CompleteSignupView.as_view(), name='complete_signup'),

	# url(r'^register-by-token/(?P<backend>[^/]+)/$',views.register_by_access_token, name='register_by_access_token'),

)
# 