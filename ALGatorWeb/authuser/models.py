from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    id = models.CharField(max_length=12, default=f'u{user.primary_key-1}', primary_key=True)

class Group(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, default='')

class Group_User(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class EntityType(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    name = models.CharField(max_length=255, default='')

class Entities(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    name = models.CharField(max_length=255, default='')
    entity_type = models.ForeignKey(EntityType, on_delete=models.DO_NOTHING)
    is_private = models.BooleanField(default=1)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class PermissionType(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    name = models.CharField(max_length=255, default='')
    codename = models.CharField(max_length=255, default='')
    value = models.IntegerField(default=0)

class EntityPermissionUser(models.Model):
    entity = models.ForeignKey(Entities, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    value = models.IntegerField(default=0)
    # permission = models.ForeignKey(PermissionType, on_delete=models.DO_NOTHING)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['entity', 'user'], name='unique_entity_user'
            )
        ]

class EntityPermissionGroup(models.Model):
    entity = models.ForeignKey(Entities, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    value = models.IntegerField(default=0)
    # permission = models.ForeignKey(PermissionType, on_delete=models.DO_NOTHING)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['entity', 'group'], name='unique_entity_group'
            )
        ]