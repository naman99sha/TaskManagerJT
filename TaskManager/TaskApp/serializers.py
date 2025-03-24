from .models import User, Task
from rest_framework import serializers, viewsets, permissions



# Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description', 'task_type', 'status']


class TaskAssignSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())