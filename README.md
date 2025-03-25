Daneshkar Django Task Management (Trello) Project

A task management system like Trello built with Django and Django REST Framework.

## Features
- **User Authentication**: Register, login, and logout
- **Team & Boards**: Create Teams(Workspaces) and Task Boards For Them.
- **Task Management**: Create, update, and assign tasks with different statuses For Each User(Team member).
- **Task Details**: Assign due dates, start dates, and track the progress of tasks.
- **REST API**: API endpoints to interact with the task management system, built using Django REST Framework.
## Technologies
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Docker**: For containerization and environment management.


## Installation

To get started with this project, follow these steps:

1.Clone the repository:
  ```
    git clone https://github.com/SeyedAliTabatabaei/django-trello.git
    cd django-trello-main/Trello
  ```

2.Build the project with Docker:
  ```
    docker-compose build
  ```
2.Run the container:
  ```
    docker-compose up -d
  ```
3.Open your Browser and Go to the link below:
```
  http://localhost:8000
```
4.Enjoy!
