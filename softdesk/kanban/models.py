from django.db import models
from users.models import User
import uuid


class Contributor(models.Model):
    """
    Represents a contributor associated with a specific project.
    Each contributor is linked to both a user and a project.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributions")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name="contributors")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        # Ensures that a user cannot be linked to the same project multiple times.


class Project(models.Model):
    """
    Represents a project within the application.
    A project has a title, description, type, and is linked to an author (creator).
    """
    id = models.AutoField(primary_key=True)
    TYPE_CHOICES = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_projects")
    created_time = models.DateTimeField(auto_now_add=True)


class Issue(models.Model):
    """
    Represents an issue (task, bug, or feature request) within a project.
    An issue is associated with a project and has an author and optional assignee.
    """
    id = models.AutoField(primary_key=True)
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]
    
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_issues")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_issues")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='LOW')
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default='TASK')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='TODO')
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Represents a comment linked to an issue.
    Comments are created by contributors of the associated project.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name="created_comments")
    created_time = models.DateTimeField(auto_now_add=True)
