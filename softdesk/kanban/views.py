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
    """
    ViewSet for managing projects.
    Allows authenticated users to create, retrieve, update, and delete projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retrieve projects where the user is either the author or a contributor.
        """
        return Project.objects.filter(
            models.Q(author=self.request.user) | models.Q(contributors__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Create a new project and add the creator as a contributor.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a project and return a success message.
        """
        project = self.get_object()
        project_id = project.id
        self.perform_destroy(project)
        return Response(
            {"message": f"Le projet {project_id} a été correctement supprimé."},
            status=status.HTTP_200_OK
        )

class ContributorViewSet(ModelViewSet):
    """
    ViewSet for managing contributors.
    Allows adding or removing contributors from a project.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retrieve contributors for a specific project.
        """
        project_id = self.kwargs['project_pk']
        return Contributor.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        """
        Add a contributor to a specific project.
        """
        project_id = self.kwargs['project_pk']
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Le projet spécifié n'existe pas.")

        serializer.save(project=project)

class IssueViewSet(ModelViewSet):
    """
    ViewSet for managing issues.
    Allows contributors to create, retrieve, update, and delete issues for a project.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retrieve issues for a specific project.
        """
        project_id = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        """
        Create a new issue for a specific project if the user is a contributor.
        """
        project_id = self.kwargs['project_pk']
        if not Contributor.objects.filter(user=self.request.user, project_id=project_id).exists():
            raise serializers.ValidationError("You must be a contributor of the project to create an issue.")
        serializer.save(project_id=project_id, author=self.request.user)

    def perform_update(self, serializer):
        """
        Update an issue for a specific project if the user is a contributor.
        """
        project_id = self.kwargs['project_pk']
        if not Contributor.objects.filter(user=self.request.user, project_id=project_id).exists():
            raise serializers.ValidationError("You must be a contributor of the project to update an issue.")
        serializer.save(project_id=project_id, author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an issue and return a success message.
        """
        issue = self.get_object()
        issue_id = issue.id
        self.perform_destroy(issue)
        return Response(
            {"message": f"L'issue {issue_id} a été correctement supprimée."},
            status=status.HTTP_200_OK
        )

class CommentViewSet(ModelViewSet):
    """
    ViewSet for managing comments.
    Allows contributors to create, retrieve, update, and delete comments for an issue.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retrieve comments for a specific issue.
        """
        issue_id = self.kwargs['issue_pk']
        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        """
        Create a new comment for a specific issue if the user is a contributor.
        """
        issue_id = self.kwargs['issue_pk']
        project_id = self.kwargs['project_pk']

        try:
            contributor = Contributor.objects.get(user=self.request.user, project_id=project_id)
        except Contributor.DoesNotExist:
            raise serializers.ValidationError("You must be a contributor of the project to manage issue.")

        serializer.save(issue_id=issue_id, author=contributor)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a comment and return a success message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Le commentaire a été correctement supprimé."},
            status=status.HTTP_200_OK
        )
