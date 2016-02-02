from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response, render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as django_logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView

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

  # Find access token and expire 
  params = content.split('&')
  # pdb.set_trace()
  ACCESS_TOKEN = params[0].split('=')[1]
  EXPIRE = params[1].split('=')[1]

  # Get basic information about the person
  response, content = http.request('https://graph.facebook.com/me?access_token=%s' % ACCESS_TOKEN)
  data = json.loads(content)
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
    profile.facebook_access_token = ACCESS_TOKEN
    profile.facebook_access_token_expires = EXPIRE
    profile.save()
    # go to Complete the registration
    return HttpResponseRedirect(reverse_lazy('profiles:complete_signup',kwargs={'pk': profile.pk}))
  # Update token and expire fields on profile
  profile.facebook_access_token = ACCESS_TOKEN
  profile.facebook_access_token_expires = EXPIRE
  profile.save()

  # Authenticate and log user in
  user = authenticate(username=profile.user.username, password=profile.facebook_uid)
  login(request, user)

  return HttpResponseRedirect('/')

class CompleteSignupView(UpdateView):
  model = Profile
  fields = ['father_name',"address","hobbies"]
  template_name = "signup/complete_signup.html"
  success_url=reverse_lazy('profiles:home')

  def form_valid(self, form):
    self.object = form.save()
    user = authenticate(username=self.object.user.username, password=self.object.facebook_uid)
    login(self.request, user)
    # pdb.set_trace()
    return super(CompleteSignupView, self).form_valid(form)

