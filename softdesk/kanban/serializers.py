from rest_framework import serializers
from .models import Contributor, Project, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['created_time']

class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.id')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']
        read_only_fields = ['created_time', 'project']
        extra_kwargs = {
            'user': {'required': True},
        }

class IssueSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.id')

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'author', 'assignee',
            'priority', 'tag', 'status', 'project', 'created_time'
        ]
        read_only_fields = ['author', 'created_time']
    
    def validate_assignee(self, value):
        project_id = self.context['view'].kwargs['project_pk']
        if not Contributor.objects.filter(user=value, project_id=project_id).exists():
            raise serializers.ValidationError("L'utilisateur assigné doit être un contributeur du projet.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    issue = serializers.ReadOnlyField(source='issue.id')

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']