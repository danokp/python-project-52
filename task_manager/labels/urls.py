from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('', views.LabelView.as_view(), name='show_labels'),
    path('create/', views.LabelCreateView.as_view(), name='create_label'),
    path(
        '<int:pk>/update/',
        views.LabelUpdateView.as_view(),
        name='update_label',
    ),
    path(
        '<int:pk>/delete/',
        views.LabelDeleteView.as_view(),
        name='delete_label',
    ),
]
