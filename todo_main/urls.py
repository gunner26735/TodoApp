from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("",views.Home.as_view(),name="home"),
    path("todo/", views.TodoList.as_view(), name="todo-list"),
    path("todo/<int:pk>/", views.TodoDetail.as_view(), name="todo-detail"),
    path("todo/register/", views.UserRegisteration.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
