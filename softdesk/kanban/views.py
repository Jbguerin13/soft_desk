from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from django.db import models
from rest_framework import serializers, status



class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        return Project.objects.filter(
                models.Q(author=self.request.user) | models.Q(contributors__user=self.request.user)
            ).distinct()
    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Contributor.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_pk']
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Le projet spécifié n'existe pas.")
        
        serializer.save(project=project)
        
class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_pk']
        if not Contributor.objects.filter(user=self.request.user, project_id=project_id).exists():
            raise serializers.ValidationError("You must be a contributor of the project to create an issue.")
        serializer.save(project_id=project_id, author=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        issue_id = issue.id
        self.perform_destroy(issue)
        return Response(
            {"message": f"L'issue {issue_id} a été correctement supprimée."},
            status=status.HTTP_200_OK
        )

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        issue_id = self.kwargs['issue_pk']
        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        issue_id = self.kwargs['issue_pk']
        project_id = self.kwargs['project_pk']

        try:
            contributor = Contributor.objects.get(user=self.request.user, project_id=project_id)
        except Contributor.DoesNotExist:
            raise serializers.ValidationError("You must be contributor of the project to manage issue.")

        serializer.save(issue_id=issue_id, author=contributor)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            { "message": "Le commentaire a été correctement supprimé." },
            status=status.HTTP_200_OK
        )