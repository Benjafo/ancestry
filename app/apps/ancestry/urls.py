from django.urls import path
from . import views

app_name = 'ancestry'
urlpatterns = [
    # Auth
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    # Ancestry
    path('', views.trees, name='home'),
    path('tree/<int:tree_id>/', views.tree, name='tree'),
    path('person/<int:person_id>/', views.person, name='person'),
    path('person/<int:person_id>/event/<int:event_id>', views.event, name='event'),
    path('person/<int:person_id>/source/<int:source_id>', views.source, name='source'),
    # Management
    path('management/crud_panel', views.crud_panel, name='crud_panel'),
    path('management/tree/create', views.TreeCreate.as_view(), name='management_create_tree'),
    path('management/tree/<int:pk>', views.TreeRead.as_view(), name='management_read_tree'),
    path('management/tree/<int:pk>/update', views.TreeUpdate.as_view(), name='management_update_tree'),
    path('management/tree/<int:pk>/delete', views.TreeDelete.as_view(), name='management_delete_tree'),
    path('management/person/create', views.PersonCreate.as_view(), name='management_create_person'),
    path('management/person/<int:pk>', views.PersonRead.as_view(), name='management_read_person'),
    path('management/person/<int:pk>/update', views.PersonUpdate.as_view(), name='management_update_person'),
    path('management/person/<int:pk>/delete', views.PersonDelete.as_view(), name='management_delete_person'),
    path('management/source/create', views.SourceCreate.as_view(), name='management_create_source'),
    path('management/source/<int:pk>', views.SourceRead.as_view(), name='management_read_source'),
    path('management/source/<int:pk>/update', views.SourceUpdate.as_view(), name='management_update_source'),
    path('management/source/<int:pk>/delete', views.SourceDelete.as_view(), name='management_delete_source'),
    path('management/event/create', views.EventCreate.as_view(), name='management_create_event'),
    path('management/event/<int:pk>', views.EventRead.as_view(), name='management_read_event'),
    path('management/event/<int:pk>/update', views.EventUpdate.as_view(), name='management_update_event'),
    path('management/event/<int:pk>/delete', views.EventDelete.as_view(), name='management_delete_event'),
]