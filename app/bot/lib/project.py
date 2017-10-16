def get_project_id(maker_id, name):
    from common.utilities import generate_unique_key
    project_id = generate_unique_key(maker_id, name)
    return project_id


def create_project(sender_id, name):
    from bot.models import Project
    from .maker import get_maker_id
    maker_id = get_maker_id(sender_id=sender_id)
    project_id = get_project_id(maker_id, name)
    project, created = Project.objects.get_or_create(id=project_id, defaults=dict(maker_id=maker_id, name=name))
    return project, created


def update_project(sender_id, project_id, material_id=None, pattern_id=None, date_string=None, tags=None):
    from bot.models import Project
    from common.utilities import generate_unique_key
    from bot.lib.utilities import add_tags
    maker_id = generate_unique_key(sender_id)
    project = Project.objects.get(maker_id=maker_id, id=project_id)
    if material_id:
        add_material(project=project, material_id=material_id)
    if pattern_id:
        add_pattern(project=project, pattern_id=pattern_id)
    if date_string:
        add_due_date(project=project, date_string=date_string)
        project.complete = True
        project.save()
    if tags:
        add_tags(obj=project, tags=tags)
    return project


def add_due_date(project, date_string):
    from bot.models import ProjectDueDate, DueDate
    from common.utilities import generate_unique_key
    from datetime import datetime
    date = datetime.strptime(date_string, '%Y-%m-%d')
    due_date_id = generate_unique_key(project.maker_id, date)
    due_date, created = DueDate.objects.get_or_create(id=due_date_id, defaults=dict(maker=project.maker, date=date))
    project_due_date, created = ProjectDueDate.objects.get_or_create(project=project, due_date=due_date)
    return project_due_date


def add_material(project, material_id):
    from bot.models import ProjectMaterial
    from common.utilities import generate_unique_key
    project_material_id = generate_unique_key(project.id, material_id)
    project_material, created = ProjectMaterial.objects.get_or_create(id=project_material_id,
                                                                      defaults=dict(project=project,
                                                                                    material_id=material_id))
    return project_material


def add_pattern(project, pattern_id):
    from bot.models import ProjectPattern
    from common.utilities import generate_unique_key
    project_pattern_id = generate_unique_key(project.id, pattern_id)
    project_pattern, created = ProjectPattern.objects.get_or_create(id=project_pattern_id,
                                                                    defaults=dict(project=project,
                                                                                  pattern_id=pattern_id))
    return project_pattern
