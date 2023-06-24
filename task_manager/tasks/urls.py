from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='show_tasks'),
    path('create/', views.TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/', views.TaskView.as_view(), name='task'),
    path(
        '<int:pk>/update/',
        views.TaskUpdateView.as_view(),
        name='update_task',
    ),
    path(
        '<int:pk>/delete/',
        views.TaskDeleteView.as_view(),
        name='delete_task',
    ),
]
