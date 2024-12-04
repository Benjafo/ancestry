from django.urls import path
from . import views

app_name = 'ancestry'
urlpatterns = [
    # Auth
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    # Ancestry
    path('', views.home, name='home'),
    path('tree/<int:tree_id>/', views.tree, name='tree'),
    path('person/<int:person_id>/', views.person, name='person'),
    path('person/<int:person_id>/event/<int:event_id>/', views.event, name='event'),
    path('person/<int:person_id>/source/<int:source_id>/', views.source, name='source'),
    # Management
    path('crud_panel/', views.crud_panel, name='crud_panel'),
    path('management/', views.management, name='management'),
    path('management/tree/create/', views.ManagementTreeCreate.as_view(), name='management_create_tree'),
    path('management/tree/<int:pk>/', views.ManagementTreeRead.as_view(), name='management_read_tree'),
    path('management/tree/<int:pk>/update/', views.ManagementTreeUpdate.as_view(), name='management_update_tree'),
    path('management/tree/<int:pk>/delete/', views.ManagementTreeDelete.as_view(), name='management_delete_tree'),
    path('management/tree/<int:pk>/person/create/', views.ManagementPersonCreate.as_view(), name='management_create_person'),
    path('management/person/<int:pk>/', views.ManagementPersonRead.as_view(), name='management_read_person'),
    path('management/person/<int:pk>/update/', views.ManagementPersonUpdate.as_view(), name='management_update_person'),
    path('management/person/<int:pk>/delete/', views.ManagementPersonDelete.as_view(), name='management_delete_person'),
    path('management/person/<int:pk>/source/create/', views.ManagementSourceCreate.as_view(), name='management_create_source'),
    path('management/source/<int:pk>/', views.ManagementSourceRead.as_view(), name='management_read_source'),
    path('management/source/<int:pk>/update/', views.ManagementSourceUpdate.as_view(), name='management_update_source'),
    path('management/source/<int:pk>/delete/', views.ManagementSourceDelete.as_view(), name='management_delete_source'),
    path('management/person/<int:pk>/event/create/', views.ManagementEventCreate.as_view(), name='management_create_event'),
    path('management/event/<int:pk>/', views.ManagementEventRead.as_view(), name='management_read_event'),
    path('management/event/<int:pk>/update/', views.ManagementEventUpdate.as_view(), name='management_update_event'),
    path('management/event/<int:pk>/delete/', views.ManagementEventDelete.as_view(), name='management_delete_event'),
]