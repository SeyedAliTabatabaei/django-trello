from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate
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
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user 
            board.save()
            return redirect('board_list')  
    else:
        form = BoardForm()
    
    return render(request, 'create_board.html', {'form': form})
def board_list(request):
    boards = Board.objects.filter(owner=request.user)
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
    list = get_object_or_404(List, id=list_id)

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.list = list
            new_task.save()
            return redirect('board_detail', board_id=list.board.id)
    else:
        task_form = TaskForm()

    return render(request, 'add_task.html', {'task_form': task_form, 'list': list})