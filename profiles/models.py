from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  # user = models.ForeignKey(User, unique=True)
  user = models.OneToOneField(User)

  picture = models.URLField(max_length=255, blank=True, null=True)
  facebook_uid = models.PositiveIntegerField(blank=True, null=True)
  facebook_access_token = models.CharField(blank=True, max_length=255)
  facebook_access_token_expires = models.PositiveIntegerField(blank=True, null=True)

  father_name = models.CharField(blank=True, max_length=55)
  address = models.CharField(blank=True, max_length=255)
  hobbies = models.CharField(blank=True, max_length=255)

  def __str__(self):
  	return str(self.user)

  	