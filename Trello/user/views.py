from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .forms import *

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect("home") 
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def create_team(request):
    user_teams = Team.objects.filter(members=request.user)
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user  
            team.save()
            team.members.add(request.user)  
            users = form.cleaned_data["members_usernames"]
            team.members.add(*users)

            return redirect("home")  

    else:
        form = TeamForm()

    return render(request, "create_team.html", {"form": form,'user_teams':user_teams})

@login_required
def create_board(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.members.all():
        return redirect("create-team") 

    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user 
            board.team = team  
            board.save()
            return redirect("board_list")  
    else:
        form = BoardForm()

    return render(request, "create_board.html", {"form": form, "team": team})
def board_list(request):
    user_teams = Team.objects.filter(members=request.user)
    boards = Board.objects.filter(team__in=user_teams)
    return render(request, 'board_list.html', {'boards': boards})

def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    lists = List.objects.filter(board=board).prefetch_related('tasks')
    if request.method == 'POST':
        list_form = ListForm(request.POST)
        if list_form.is_valid():
            new_list = list_form.save(commit=False)
            new_list.board = board
            new_list.save()
            return redirect('board_detail', board_id=board.id)
    else:
        list_form = ListForm()

    lists = board.lists.all()
    return render(request, 'board_detail.html', {'board': board, 'list_form': list_form, 'lists': lists,})

def add_task(request, list_id):
    task_list = get_object_or_404(List, id=list_id)
    team = task_list.board.team
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        task_form.fields["assigned_users"].queryset = team.members.all()    
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.list = task_list
            new_task.save()
            task_form.save_m2m() 
            return redirect('board_detail', board_id=task_list.board.id)
    else:
        task_form = TaskForm()
        task_form.fields["assigned_users"].queryset = team.members.all()
    return render(request, 'add_task.html', {'task_form': task_form, 'list': task_list})

def update_list_name(request, list_id):
    if request.method == 'POST':
        list = get_object_or_404(List, id=list_id)
        new_name = request.POST.get('name')
        if new_name:
            list.name = new_name
            list.save()
            return JsonResponse({'message': 'Name updated successfully', 'new_name': list.name})
        return JsonResponse({'error': 'Invalid name'}, status=400)

@api_view(['POST'])
def update_list_name(request, list_id):
    list = get_object_or_404(List, id=list_id)
    new_name = request.data.get('name')
    if new_name:
        list.name = new_name
        list.save()
        serializer = ListSerializer(list)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid name'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def task_details_json(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['POST'])
def move_task_to_list(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    #if task.assigned_users.filter(id=request.user.id).exists():
    new_list_id = request.data.get('new_list_id')
    new_list = get_object_or_404(List, id=new_list_id)
    task.list = new_list
    task.save()
    return Response("با موفقیت انجام شد!", status=status.HTTP_200_OK)
   # else:
       # return Response("شما دسترسی لازم برای اینکار را ندارید!", status=status.HTTP_403_FORBIDDEN)

@api_view(['PATCH'])
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def assign_user(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        user_id = request.POST.get("user_id")
        is_assigned = request.POST.get("is_assigned") == "true"
        task = get_object_or_404(Task, id=task_id)
        user = get_object_or_404(User, id=user_id)
        if is_assigned:
            task.assigned_users.add(user)
        else:
            task.assigned_users.remove(user)
        return JsonResponse({"message": "تغییرات با موفقیت انجام شد."}, status=200)
    return JsonResponse({"error": "متد مجاز نیست."}, status=400)

def is_user_assigned(request, task_id, username):
    task = get_object_or_404(Task, id=task_id)
    is_assigned = task.assigned_users.filter(username=username).exists()
    return JsonResponse({"is_assigned": is_assigned})