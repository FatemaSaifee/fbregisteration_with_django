from django.conf.urls import patterns, include, url
from  . import views
# import pdb
# from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^facebook/', views.facebook, name='facebook'),
	url(r'^logout/', views.logout, name='logout'),
	# url(r'^register-by-token/(?P<backend>[^/]+)/$',views.register_by_access_token, name='register_by_access_token'),

)
# pdb.set_trace()