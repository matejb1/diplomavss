from django.urls import path

from . import views

urlpatterns = [
    path('users', views.manage_users_view, name='manageusersview'),
    path('users/<int:id>', views.manage_single_user_view, name='managesingleuserview'),
    path('users/get_users', views.get_users, name='get_users'),
    path('users/get_user/<int:id>', views.get_user, name='get_user'),
    path('users/edit_user', views.edit_user, name='edit_user'),
    path('users/remove_user', views.remove_user, name='remove_user'),
    path('users/get_permissions', views.get_all_user_permissions, name='get_all_user_permissions'),
    path('users/add_permission', views.add_user_permission, name='add_user_permission'),
    path('users/update_permission', views.update_user_permission, name='update_user_permission'),
    path('rights', views.manage_rights_view, name='managerightsview'),
    path('groups/get_groups', views.get_groups, name='get_groups'),
    path('groups/get_groups_user', views.get_groups_user, name='get_groups_user'),
    path('groups/add_user_to_group', views.add_user_to_group, name='add_user_to_group'),
    path('groups/remove_user_from_group', views.remove_user_from_group, name='remove_user_from_group'),
    path('groups/add_group', views.add_group, name='add_group'),
    path('groups/remove_group', views.remove_group, name='remove_group'),
    path('groups/add_permission', views.add_group_permission, name='add_group_permission'),
    path('groups/update_permission', views.update_group_permission, name='update_group_permission'),
    path('can', views.can, name='can'),
    path('entities_permissions', views.entities_permissions, name='entities_permissions'),
    path('get_entities', views.get_entities, name='get_entities'),
]
