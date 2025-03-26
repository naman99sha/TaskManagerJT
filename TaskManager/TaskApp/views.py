from .models import (
    User,
    Task
)
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskAssignSerializer,
    UserSerializer,
    UserRegistrationSerializer
)
from rest_framework import (
    viewsets,
    permissions
)
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# ViewSets
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def assign(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskAssignSerializer(data=request.data)
        if serializer.is_valid():
            user_ids = serializer.validated_data['user_ids']
            users = User.objects.filter(id__in=user_ids)
            task.assigned_users.add(*users)
            return Response({'status': 'Users assigned successfully'})
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_tasks(self, request):
        tasks = Task.objects.filter(assigned_users=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            userObj = User.objects.get(id=user.id)
            token = Token(user=userObj)
            token.save()
            return Response({"token": token.key,"user": UserSerializer(userObj).data}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

