from rest_framework import serializers
from .models import Contributor, Project, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    Handles serialization and deserialization of project-related data.
    """

    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['created_time']

class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model.
    Manages data for contributors associated with a specific project.
    """

    project = serializers.ReadOnlyField(source='project.id')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']
        read_only_fields = ['created_time', 'project']
        extra_kwargs = {
            'user': {'required': True},
        }

class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for the Issue model.
    Handles issue-related data for a specific project.
    Validates that the assigned user is a contributor of the project.
    """

    project = serializers.ReadOnlyField(source='project.id')

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'author', 'assignee',
            'priority', 'tag', 'status', 'project', 'created_time'
        ]
        read_only_fields = ['author', 'created_time']
    
    def validate_assignee(self, value):
        """
        Validates that the assignee is a contributor to the project.
        """
        project_id = self.context['view'].kwargs['project_pk']
        if not Contributor.objects.filter(user=value, project_id=project_id).exists():
            raise serializers.ValidationError("The assigned user must be a contributor of the project.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Manages comment-related data for issues in a project.
    """

    issue = serializers.ReadOnlyField(source='issue.id')

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']
