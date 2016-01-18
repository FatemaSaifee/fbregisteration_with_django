from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response, render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as django_logout

try:
    from django.utils import simplejson as json
except:
    import simplejson as json

import httplib2
import urllib
import pdb

from .models import Profile
from fbregisteration.settings import FACEBOOK_APP_ID

def home(request):
	context = RequestContext(request,
	                       {'request': request,
	                        'user': request.user,
	                        'facebook_app_id': FACEBOOK_APP_ID})
	return render_to_response('signup/home.html',
	                         context_instance=context)

def logout(request):
	django_logout(request)
	return HttpResponseRedirect('/')

def facebook(request):
  params = {
    'client_id': settings.FACEBOOK_APP_ID,
    'redirect_uri': 'http://localhost:8000/facebook/',
    'client_secret': settings.FACEBOOK_SECRET_KEY,
    'code': request.GET['code']
  }

  http = httplib2.Http(timeout=15)
  response, content = http.request('https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(params))

  # Find access token and expire (this is really gross)
  params = content.split('&')
  # pdb.set_trace()
  ACCESS_TOKEN = params[0].split('=')[1]
  EXPIRE = params[1].split('=')[1]

  # Get basic information about the person
  response, content = http.request('https://graph.facebook.com/me?access_token=%s' % ACCESS_TOKEN)
  data = json.loads(content)
  # pdb.set_trace()
  # Try to find existing profile, create a new user if one doesn't exist
  try:
    profile = Profile.objects.get(facebook_uid=data['id'])
  except Profile.DoesNotExist:
    user = User.objects.create_user(data['name'], '', data['id'])
		# get user's photo # is_silhouette is true if the user has not uploaded a profile picture
    graph_url = 'https://graph.facebook.com/me/picture?' \
                + 'type=large' \
                + '&redirect=false' \
                + '&access_token=' + ACCESS_TOKEN

    response = urllib.urlopen(graph_url).read()
    picture = json.loads(response)
		# ensure the user has uploaded a picture
    if not picture['data']['is_silhouette']:
      picture = picture['data']['url']
    else:
		  picture = ''

    Profile.objects.create(user=user,picture=picture, facebook_uid=data['id'])
    profile = Profile.objects.get(facebook_uid=data['id'])
  # Update token and expire fields on profile
  profile.facebook_access_token = ACCESS_TOKEN
  profile.facebook_access_token_expires = EXPIRE
  profile.save()

  # Authenticate and log user in
  user = authenticate(username=profile.user.username, password=profile.facebook_uid)
  login(request, user)

  return HttpResponseRedirect('/')


# ##########################################################################
# from django.core.urlresolvers import reverse
# from django.core.context_processors import csrf


# def get_authorization_url(request):
#         # URL to where Facebook will redirect to
#         redirect_url = urllib.quote_plus(settings.SITE_URL + reverse('register_facebook'))

#         # create a unique state value for CSRF validation
#         request.session['facebook_state'] = unicode(csrf(request)['csrf_token'])

#         # redirect to facebook for approval
#         url = 'https://www.facebook.com/dialog/oauth?' \
#               + 'client_id=' + settings.FACEBOOK_APP_ID \
#               + '&redirect_uri=' + redirect_url \
#               + '&scope=email' \
#               + '&state=' + request.session['facebook_state']

#         return url

# def verify(request):
#         # Facebook will direct with state and code in the URL
#         # ?state=ebK3Np...&code=AQDJEtIZEDU...#_=_

#         # ensure we have a session state and the state value is the same as what facebook returned
#         # also ensure we have a code from facebook (not present if the user denied the application)
#         if 'facebook_state' not in request.session \
#            or 'state' not in request.GET \
#            or 'code' not in request.GET \
#            or request.session['facebook_state'] != request.GET['state']:
#             HttpResponseRedirect(reverse('register'))# return False
#         else:
#             return True


# import urllib
# import urllib2
# import urlparse
# import json
# from django.conf import settings
# from django.core.urlresolvers import reverse


# def get_user_data(request):

#         data = {}

#         # if we don't have a token yet, get one now
#         if 'facebook_access_token' not in request.session:

#             # URL to where we will redirect to
#             redirect_url = urllib.quote_plus(settings.SITE_URL + reverse('register_facebook'))

#             # set the token URL
#             url = 'https://graph.facebook.com/oauth/access_token?' \
#                   + 'client_id=' + settings.FACEBOOK_APP_ID \
#                   + '&redirect_uri=' + redirect_url \
#                   + '&client_secret=' + settings.FACEBOOK_API_SECRET \
#                   + '&code=' + request.GET['code']

#             # grab the token from FB
#             response = urllib2.urlopen(url).read()

#             # parse the response
#             # {'access_token': ['AAAGVChRC0ygBAF3...'], 'expires': ['5183529']}
#             params = urlparse.parse_qs(response)

#             # save the token
#             request.session['facebook_access_token'] = params['access_token'][0]
#             request.session['facebook_access_expires'] = params['expires'][0]

#         # set the graph URL using the token we just fetched
#         graph_url = 'https://graph.facebook.com/me?' \
#                     + 'access_token=' + request.session['facebook_access_token']

#         # get the user's data from facebook
#         response = urllib2.urlopen(graph_url).read()
#         user = json.loads(response)

#         # get their photo
#         # is_silhouette is true if the user has not uploaded a profile picture
#         graph_url = 'https://graph.facebook.com/me/picture?' \
#                     + 'type=large' \
#                     + '&redirect=false' \
#                     + '&access_token=' + request.session['facebook_access_token']

#         response = urllib2.urlopen(graph_url).read()
#         picture = json.loads(response)

#         # get the user's info
#         data['user_id'] = user['id']
#         data['username'] = user['username']
#         data['email'] = user['email']
#         data['full_name'] = user['first_name'] + ' ' + user['last_name']
#         data['first_name'] = user['first_name']
#         data['last_name'] = user['last_name']
#         data['timezone'] = user['timezone']

#         # ensure the user has uploaded a picture
#         if not picture['data']['is_silhouette']:
#             data['picture'] = picture['data']['url']
#         else:
#             data['picture'] = ''

#         return data