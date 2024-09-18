from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientListCreate.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', views.ClientDetail.as_view(), name='client-detail'),
    path('clients/<int:client_id>/projects/', views.ProjectCreate.as_view(), name='project-create'),
    path('projects/', views.UserProjectList.as_view(), name='user-project-list'),
]
