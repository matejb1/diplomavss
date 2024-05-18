from django.urls import path

from . import views

urlpatterns = [
    path('users', views.manage_users_view, name='manageusersview'),
    path('users/<int:id>', views.manage_single_user_view, name='managesingleuserview'),
    path('users/add_permission', views.add_user_permission, name='add_user_permission'),
    path('users/remove_permission', views.remove_user_permission, name='remove_user_permission'),
    path('groups', views.manage_groups_view, name='managegroupsview'),
    path('groups/<int:id>', views.manage_single_group_view, name='managesinglegroupview'),
    path('groups/add_group', views.add_group, name='add_group'),
    path('groups/remove_group', views.remove_group, name='add_group'),
    path('groups/add_permission', views.add_group_permission, name='add_group_permission'),
    path('groups/remove_permission', views.remove_group_permission, name='remove_group_permission'),
]
