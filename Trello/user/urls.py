from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
from .serializers import ListDeleteAPIView


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("create-team/", create_team, name="create_team"),
    path("team/<int:team_id>/create-board/", create_board, name="create-board"),
    #path('create/', create_board, name='create_board'),
    path('list/<int:list_id>/update/', update_list_name, name='update_list_name'),
    path('lists/<int:list_id>/delete', ListDeleteAPIView.as_view(), name='delete_list'),
   path('tasks/<int:list_id>/create/', CreateTaskAPIView.as_view(), name='add_task'),
    path('task/<int:task_id>/details/',task_details_json, name='task_details_json'),
    path('task/<int:task_id>/move/', move_task_to_list, name='move_task_to_list'),
    path('tasks/<int:task_id>/update/', update_task, name='task_update'),
    path('boardlist/', board_list, name='board_list'),
    path('board/<int:board_id>/', board_detail, name='board_detail'),
   #path('list/<int:list_id>/add_task/',add_task, name='add_task'),
    
]