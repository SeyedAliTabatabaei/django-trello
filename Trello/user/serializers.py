import jdatetime
from rest_framework import serializers,viewsets
from .models import Task,List
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Board

class TeamMembersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, board_id):
        try:
            board = Board.objects.get(id=board_id)
            team_members = board.team.members.all()
            members_data = [{"id": member.id, "username": member.username} for member in team_members]
            return Response({"members": members_data})
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=404)
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name']
class ListDeleteAPIView(APIView):
    def delete(self, request, list_id):
        list_obj = get_object_or_404(List, id=list_id)
        list_obj.delete()
        return Response({"message": "لیست با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)


class CreateTaskAPIView(APIView):
    def post(self, request, list_id):
        list_obj = List.objects.get(id=list_id)  
        task_name = request.data.get('name')
        
        if not task_name:
            return Response({"error": "نام تسک نمی‌تواند خالی باشد."}, status=status.HTTP_400_BAD_REQUEST)
        
        task = Task.objects.create(name=task_name, list=list_obj)
        serializer = TaskSerializer(task)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True) 
    assigned_users = serializers.SerializerMethodField()
    list_name = serializers.CharField(source='list.name', read_only=True) 
    class Meta:
        model = Task
        fields = ['id','name', 'description', 'start_date', 'end_date', 'due_date', 'is_completed', 'assigned_users','list_name']

    def get_assigned_users(self, obj):
            return [{"username": user.username} for user in obj.assigned_users.all()]

    # def to_shamsi(self, date):
    #     if date:
    #         return jdatetime.datetime.fromgregorian(datetime=date).strftime('%Y/%m/%d - %H:%M')
    #     return None

    # def get_start_date(self, obj):
    #     return self.to_shamsi(obj.start_date)

    # def get_end_date(self, obj):
    #     return self.to_shamsi(obj.end_date)

    # def get_due_date(self, obj):
    #     return self.to_shamsi(obj.due_date)
    