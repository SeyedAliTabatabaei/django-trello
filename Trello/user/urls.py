from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("create-team/", create_team, name="create_team"),
    path("team/<int:team_id>/create-board/", create_board, name="create-board"),
    #path('create/', create_board, name='create_board'),
    path('task/<int:task_id>/details/',task_details_json, name='task_details_json'),
    path('boardlist/', board_list, name='board_list'),
    path('board/<int:board_id>/', board_detail, name='board_detail'),
    path('list/<int:list_id>/add_task/',add_task, name='add_task'),
    
]