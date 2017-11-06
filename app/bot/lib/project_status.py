def create_project_status(sender_id, project_id, url, file_type):
    from django.utils.timezone import now
    from .maker import get_maker_id
    from bot.models import ProjectStatus
    from bot.lib.utilities import add_file
    from common.utilities import generate_unique_key

    maker_id = get_maker_id(sender_id)

    project_status_id = generate_unique_key(project_id, now())
    project_status, created = ProjectStatus.objects.get_or_create(id=project_status_id,
                                                                  defaults=dict(project_id=project_id,
                                                                                maker_id=maker_id))

    add_file(obj=project_status, file_type=file_type, url=url)
    return project_status


def update_project_status(sender_id, project_status_id, file=None, tags=None, completion_percentage=None):
    from .utilities import add_file, add_tags
    from bot.models import ProjectStatus
    from .maker import get_maker_id

    maker_id = get_maker_id(sender_id)
    project_status = ProjectStatus.objects.prefetch_related('project__project_due_date__due_date').get(id=project_status_id, maker_id=maker_id)

    if file:
        add_file(obj=project_status, url=file['url'], file_type=file['file_type'])

    if tags:
        add_tags(obj=project_status, tags=tags)

    if completion_percentage:
        add_completion_percentage(project_status=project_status, completion_percentage=completion_percentage)
    return project_status


def add_completion_percentage(project_status, completion_percentage):
    from bot.models import ProjectStatusCompletion
    ProjectStatusCompletion.objects.update_or_create(
        project_status=project_status,
        defaults=dict(percentage=completion_percentage)
    )
    if completion_percentage >= 100:
        project_status.project.finished = True
        project_status.project.save()
    project_status.complete = True
    project_status.save()
    return project_status
