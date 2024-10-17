from django.urls import path
from . import views

app_name = 'ancestry'
urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Base
    path('', views.index, name='index'),
    path('tree/<int:tree_id>/', views.tree, name='tree'),
    path('person/<int:person_id>/', views.person, name='person'),
    # Admin
    path('admin', views.admin, name='admin'),
    path('admin/tree/<int:tree_id>', views.admin_tree, name='admin_tree'),
    path('admin/tree/<int:tree_id>/edit', views.admin_edit_tree, name='admin_edit_tree'),
    path('admin/tree/create', views.admin_create_tree, name='admin_create_tree'),
    path('admin/tree/<int:tree_id>/person/<int:person_id>/event/create', views.admin_create_event, name='admin_create_event'),
    path('admin/tree/<int:tree_id>/person/<int:person_id>/edit', views.admin_edit_person, name='admin_edit_person'),
    path('admin/tree/<int:tree_id>/person/create', views.admin_create_person, name='admin_create_person'),
    path('admin/source/<int:source_id>/edit', views.admin_edit_source, name='admin_edit_source'),
    path('admin/source/create', views.admin_create_source, name='admin_create_source'),
]