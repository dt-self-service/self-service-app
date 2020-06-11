from django.db import models

# Create your models here.


class ZonePerms(models.Model):
  class Meta:
    managed = False
    default_permissions = ()
