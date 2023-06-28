from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.UsersView.as_view(), name='show_users'),
    path('create/', views.UserFormCreateView.as_view(), name='create_user'),
    path(
        '<int:pk>/update/',
        views.UserUpdateView.as_view(),
        name='update_user',
    ),
    path(
        '<int:pk>/delete/',
        views.UserDeleteView.as_view(),
        name='delete_user',
    ),
]
