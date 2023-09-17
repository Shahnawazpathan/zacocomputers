from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('todo/', views.todo, name='todo'),
    path('tasks/', views.mytask, name='my_task'),
    path('create_task/', views.created_task, name='create_task'),
    path('status/<int:task_id>/', views.status, name='status'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('checker/', views.checker, name='checker'),

]
