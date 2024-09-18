from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, UserSerializer
from django.contrib.auth.models import User

class ClientListCreate(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDetail(APIView):
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        data = request.data.copy()
        serializer = ClientSerializer(client, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectCreate(APIView):
    def post(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        data = request.data.copy()
        data['client'] = client.id
        data['created_by'] = request.user.id
        user_ids = [user['id'] for user in request.data.get('users', [])]
        users = User.objects.filter(id__in=user_ids)
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            project = serializer.save(created_by=request.user)
            project.users.set(users)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProjectList(APIView):
    def get(self, request):
        projects = request.user.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
