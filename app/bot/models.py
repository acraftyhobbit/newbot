from django.contrib.postgres.fields import JSONField
from django.db import models


class Maker(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    sender_id = models.TextField(unique=True)
    conversation_stage = models.ForeignKey('ConversationStage', null=True, default=None)
    context = JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ConversationStage(models.Model):
    """"""
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=64, editable=False)
    conversation = models.ForeignKey('Conversation')
    created = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    """"""
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=64, editable=False)
    created = models.DateTimeField(auto_now_add=True)


class MakerProfile(models.Model):
    """"""
    maker = models.OneToOneField(
        "Maker",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )
    first_name = models.TextField()
    last_name = models.TextField(null=True, default=None)
    profile_picture = models.ForeignKey('File', null=True, default=None)
    gender = models.CharField(default=None, null=True, max_length=24)
    timezone = models.IntegerField(default=0)
    locale = models.CharField(max_length=24)
    updated = models.DateTimeField(auto_now=True)


class DueDate(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    maker = models.ForeignKey('Maker', related_name='due_dates')
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    maker = models.ForeignKey('Maker', related_name='projects')
    name = models.TextField(editable=False)
    materials = models.ManyToManyField('Material', through='ProjectMaterial', related_name='projects')
    patterns = models.ManyToManyField('Pattern', through='ProjectPattern', related_name='projects')
    tags = models.ManyToManyField('Tag', through='ProjectTag', related_name='projects')
    complete = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)


class ProjectDueDate(models.Model):
    """""""
    project = models.OneToOneField(
        "Project",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='project_due_date'
    )
    due_date = models.ForeignKey('DueDate', related_name='project_due_dates')


class Material(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    maker = models.ForeignKey('Maker', related_name='materials')
    files = models.ManyToManyField('File', through='MaterialFile', related_name='materials')
    tags = models.ManyToManyField('Tag', through='MaterialTag', related_name='materials')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)


class Pattern(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    maker = models.ForeignKey('Maker', related_name='patterns')
    files = models.ManyToManyField('File', through='PatternFile', related_name='patterns')
    tags = models.ManyToManyField('Tag', through='PatternTag', related_name='patterns')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)


class ProjectStatus(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    maker = models.ForeignKey('Maker', related_name='project_statuses', null=True, default=None)
    project = models.ForeignKey('Project', related_name='statuses')
    files = models.ManyToManyField('File', through='ProjectStatusFile', related_name='project_statuses')
    tags = models.ManyToManyField('Tag', through='ProjectStatusTag', related_name='project_statuses')
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class ProjectStatusCompletion(models.Model):
    """"""
    project_status = models.OneToOneField(
        "ProjectStatus",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='completion'
    )
    percentage = models.PositiveIntegerField()


class ProjectMaterial(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    project = models.ForeignKey('Project')
    material = models.ForeignKey('Material')
    created = models.DateTimeField(auto_now_add=True)


class ProjectPattern(models.Model):
    """""""
    id = models.UUIDField(primary_key=True, editable=False)
    project = models.ForeignKey('Project')
    pattern = models.ForeignKey('Pattern')
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Tag(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class PatternFile(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    file = models.ForeignKey('File')
    pattern = models.ForeignKey('Pattern')
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class ProjectStatusFile(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    file = models.ForeignKey('File')
    project_status = models.ForeignKey('ProjectStatus')
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class MaterialFile(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    file = models.ForeignKey('File')
    material = models.ForeignKey('Material')
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class MaterialTag(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    tag = models.ForeignKey('Tag')
    material = models.ForeignKey('Material')
    created = models.DateTimeField(auto_now_add=True)


class PatternTag(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    tag = models.ForeignKey('Tag')
    pattern = models.ForeignKey('Pattern')
    created = models.DateTimeField(auto_now_add=True)


class ProjectTag(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    tag = models.ForeignKey('Tag')
    project = models.ForeignKey('Project')
    created = models.DateTimeField(auto_now_add=True)


class ProjectStatusTag(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    tag = models.ForeignKey('Tag')
    project_status = models.ForeignKey('ProjectStatus')
    created = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    """"""
    id = models.UUIDField(primary_key=True, editable=False)
    url = models.TextField()
    type = models.ForeignKey('FileType', related_name='files')
    downloaded = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


class FileType(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
