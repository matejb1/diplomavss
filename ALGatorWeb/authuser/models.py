from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    user = models.ManyToManyField(User)
    name = models.CharField(max_length=255, default='')

class EntityType(models.Model):
    name = models.CharField(max_length=255, default='')

class Entities(models.Model):
    entity_id = models.CharField(max_length=10, default='')
    entity_type = models.ForeignKey(EntityType, on_delete=models.DO_NOTHING)
    is_private = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class PermissionType(models.Model):
    name = models.CharField(max_length=255, default='')
    codename = models.CharField(max_length=255, default='')

class EntityPermissionUser(models.Model):
    entity = models.ForeignKey(Entities, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    permission = models.ForeignKey(PermissionType, on_delete=models.DO_NOTHING)

class EntityPermissionGroup(models.Model):
    entity = models.ForeignKey(Entities, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    permission = models.ForeignKey(PermissionType, on_delete=models.DO_NOTHING)
