from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    uid = models.CharField(max_length=12, unique=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.uid:
            self.uid = f'u{self.id - 1}'
            super().save(*args, **kwargs)


class Group(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='uid')
    name = models.CharField(max_length=255, default='')


class Group_User(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='uid')


class EntityType(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    name = models.CharField(max_length=255, default='')


class Entities(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    name = models.CharField(max_length=255, default='')
    entity_type = models.ForeignKey(EntityType, on_delete=models.DO_NOTHING)
    is_private = models.BooleanField(default=1)
    parent = models.ForeignKey('self', max_length=12, blank=True, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='uid')

class PermissionType(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    name = models.CharField(max_length=255, default='')
    codename = models.CharField(max_length=255, default='')
    value = models.IntegerField(default=0)


class EntityPermissionUser(models.Model):
    entity = models.ForeignKey(Entities, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='uid')
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


class Entity_permission(models.Model):
    permission_type = models.ForeignKey(PermissionType, on_delete=models.DO_NOTHING)
    entity_type = models.ForeignKey(EntityType, on_delete=models.DO_NOTHING)