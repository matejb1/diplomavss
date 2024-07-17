from django.test import TestCase, TransactionTestCase
import authuser.repository as repository
import authuser.helper as helper
from authuser import repository
from authuser.models import Group, User, Group_User, Entities, EntityType, PermissionType
from unittest import TestCase as UTestCase


# Create your tests here.
class RepositoryTest(TransactionTestCase):
    def setUp(self):
        # Users
        root = User.objects.create_user('root', 'root@algator.si', 'root', is_superuser=True, uid='u0')
        anonymous = User.objects.create_user('anonymous', 'anonymous@algator.si', 'anonymous', is_active=False,
                                             uid='u1')

        everyone_group = Group.objects.create(id='g0', name='everyone', owner=root)
        anonymous_group = Group.objects.create(id='g1', name='anonymous', owner=root)

        et0 = EntityType.objects.create(id='et0', name='system')
        e0 = Entities.objects.create(id='e0', name='system', entity_type= et0, is_private=False, parent=None, owner=root)

        pt0 = PermissionType.objects.create(id='pt0', name='Can read?', codename='can_read', value=1)

    def test_add_group(self):
        repository.add_group('u0', 'flintstones')
        self.assertTrue(Group.objects.filter(name='flintstones').exists())
        repository.add_group('u0', 'flintstones')  # Already in database, it shouldn't add.
        self.assertRaises(ValueError, repository.add_group, 'u0', '')  # Empty group name
        self.assertRaises(ValueError, repository.add_group, 'u0', None)  # Empty group name
        self.assertRaises(ValueError, repository.add_group, 'homer', 'simpsons')  # Invalid uid.
        repository.add_group('u23', 'simpsons')  # User doesn't exists. Skip adding.

    def test_add_user(self):
        repository.add_user("lolek", "lolek@bolek.si", "bolek123")
        self.assertTrue(User.objects.filter(username='lolek').exists())
        self.assertRaises(ValueError, repository.add_user, "", "lolek@bolek.si", "bolek123")  # Empty username
        self.assertRaises(ValueError, repository.add_user, "bolek", None, "bolek123")  # Empty mail
        self.assertRaises(ValueError, repository.add_user, "bolek", "lolek@bolek.si", "       ")  # Empty password
        repository.add_user("lolek", "lolek@bolek.si", "bolek123")  # Already in database.

    def test_add_user_to_group(self):
        repository.add_user("lolek", "lolek@bolek.si", "bolek123")
        repository.add_user_to_group('lolek', 'g0')  # Should be added.
        self.assertTrue(Group_User.objects.all().exists())

        repository.add_user_to_group('lolek', 'g0')  # Shouldn't be added.
        self.assertTrue(Group_User.objects.all().count() == 1)

        repository.add_user_to_group('bart_simpson', 'g0')  # Unknown username
        self.assertTrue(Group_User.objects.all().count() == 1)

        repository.add_user_to_group('lolek', 'g22')  # Unknown group
        self.assertTrue(Group_User.objects.all().count() == 1)

        self.assertRaises(ValueError, repository.add_user_to_group, '   ', '   ')  # Unknown data
        self.assertRaises(ValueError, repository.add_user_to_group, '   ', 'g0')  # Unknown data
        self.assertRaises(ValueError, repository.add_user_to_group, 'lolek', None)  # Unknown data

    def test_edit_user(self):
        user = User.objects.create_user("lolek", "lolek@bolek.si", "bolek123")
        repository.edit_user(user.id, "bolek", "bolek@lolek.si")
        self.assertTrue(User.objects.filter(username="bolek").exists())
        self.assertRaises(ValueError, repository.edit_user, 0, "bolek", "bolek@lolek.si")  # Invalid ID

        repository.edit_user(user.id, "root", "bolek@lolek.si")  # bolek wants to rename to root
        self.assertTrue(User.objects.get(username="root") != user.id)

        self.assertRaises(ValueError, repository.edit_user, user.id, "    ", "    ")
        self.assertRaises(ValueError, repository.edit_user, user.id, "bolek", None)

    def test_remove_group(self):
        user = User.objects.create_user("lolek", "lolek@bolek.si", "bolek123")
        group1 = Group.objects.create(id='g5', name='strawberries', owner=user)
        repository.remove_group('g5')
        self.assertFalse(Group.objects.filter(name="strawberries").exists())
        repository.remove_group('g5')
        self.assertRaises(ValueError, repository.remove_group, "unknown_id")

    def test_remove_user(self):
        user = User.objects.create_user("lolek", "lolek@bolek.si", "bolek123")
        repository.remove_user(user.uid)
        self.assertRaises(ValueError, repository.remove_user, ' ')
        self.assertRaises(ValueError, repository.remove_user, None)

    def test_remove_user_from_group(self):
        user = User.objects.create_user("lolek", "lolek@bolek.si", "bolek123")
        group1 = Group.objects.create(id='g5', name='strawberries', owner=user)
        user2 = User.objects.create_user("bolek", "bolek@lolek.si", "lolek123")

        repository.remove_user_from_group('bolek', 'g5')
        self.assertRaises(ValueError, repository.remove_user_from_group, None, 'qw')
        self.assertRaises(ValueError, repository.remove_user_from_group, '    ', '   ')

    def test_add_permission_to_user(self):
        user = User.objects.create_user("lolek", "lolek@bolek.si", "bolek123")
        repository.add_permission_to_user('lolek', 'can_read', 'e0')
        self.assertRaises(ValueError, repository.add_permission_to_user, '', 'can_read', 'e0')
        repository.add_permission_to_user('lolek', 'BREZ_PRAVIC', 'e0')

    def test_add_permission_to_group(self):
        user = User.objects.create_user("lolek", "lolek@bolek.si", "bolek123")
        group1 = Group.objects.create(id='g5', name='strawberries', owner=user)
        repository.add_permission_to_group('g5', 'can_read', 'e0')
        self.assertRaises(ValueError, repository.add_permission_to_group, '', 'can_read', 'e0')
        repository.add_permission_to_group('g5', 'BREZ_PRAVIC', 'e0')

    def test_update_user_permission(self):
        user = User.objects.create_user("lolek", "lolek@bolek.si", "bolek123")
        repository.add_permission_to_user(user.uid, 'can_add_project', 'e0')
        repository.update_user_permission(user.uid, 'p3', 'e0', 8)
        self.assertRaises(ValueError, repository.update_user_permission, "        ", 'p3', 'e0', 8)

    def test_update_group_permission(self):
        user = User.objects.create_user("lolek", "lolek@bolek.si", "bolek123")
        group1 = Group.objects.create(id='g5', name='strawberries', owner=user)
        repository.add_permission_to_group('g5', 'can_add_project', 'e0')
        repository.update_group_permission('g5', 'p3', 'e0', 8)
        self.assertRaises(ValueError, repository.update_group_permission, "        ", 'p3', 'e0', 8)

    def test_add_entity(self):
        repository.add_entity('u0', 'test project', 'et1', None, True)



class HelperTest(UTestCase):
    def test_is_valid_id(self):
        self.assertTrue(helper.is_valid_id("u", "u1269"))
        self.assertFalse(helper.is_valid_id("u", "u126a"))
        self.assertFalse(helper.is_valid_id("u", "test"))
        self.assertFalse(helper.is_valid_id("u", ""))
        self.assertFalse(helper.is_valid_id("g", None))
