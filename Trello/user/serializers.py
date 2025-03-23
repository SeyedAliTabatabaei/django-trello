import jdatetime
from rest_framework import serializers
from .models import Task,List

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    due_date = serializers.SerializerMethodField()
    list_name = serializers.CharField(source='list.name', read_only=True) 
    class Meta:
        model = Task
        fields = ['name', 'description', 'start_date', 'end_date', 'due_date', 'is_completed', 'assigned_users','list_name']

    def get_assigned_users(self, obj):
        return [{"username": user.username} for user in obj.assigned_users.all()]

    def to_shamsi(self, date):
        if date:
            return jdatetime.datetime.fromgregorian(datetime=date).strftime('%Y/%m/%d - %H:%M')
        return None

    def get_start_date(self, obj):
        return self.to_shamsi(obj.start_date)

    def get_end_date(self, obj):
        return self.to_shamsi(obj.end_date)

    def get_due_date(self, obj):
        return self.to_shamsi(obj.due_date)