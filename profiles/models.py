from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  # user = models.ForeignKey(User, unique=True)
  user = models.OneToOneField(User)

  facebook_uid = models.PositiveIntegerField(blank=True, null=True)
  facebook_access_token = models.CharField(blank=True, max_length=255)
  facebook_access_token_expires = models.PositiveIntegerField(blank=True, null=True)

  def __str__(self):
  	return self.user