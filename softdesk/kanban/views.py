from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from django.db import models
from rest_framework import serializers



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

    def perform_create(self, serializer):
        serializer.save()
        
class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        project_id = self.kwargs['project_pk']
        serializer.save(project_id=project_id, author=self.request.user)

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
            raise serializers.ValidationError("Vous devez être contributeur du projet pour commenter une issue.")

        serializer.save(issue_id=issue_id, author=contributor)
