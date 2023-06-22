from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.StatusView.as_view(), name='show_statuses'),
    path('create/', views.StatusCreateView.as_view(), name='create_status'),
    path(
        '<int:pk>/update/',
        views.StatusUpdateView.as_view(),
        name='update_status',
    ),
    path(
        '<int:pk>/delete/',
        views.StatusDeleteView.as_view(),
        name='delete_status',
    ),
]
