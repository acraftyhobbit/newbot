import uuid
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Conversation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)


class ConversationStage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.TextField(unique=True)
    conversation = models.ForeignKey('Conversation', related_name='stages')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('conversation', 'name')


class ConversationArtifact(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    conversation = models.ForeignKey('Conversation', related_name='artifacts')
    stage = models.ForeignKey('ConversationStage', related_name='artifacts')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ('conversation', 'stage', 'created')
