from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def facebook(request):
    import json
    from django.http import HttpResponse
    """Connection to facebook verification"""
    if request.method == 'GET':
        return HttpResponse(request.GET['hub.challenge'])
    else:
        try:
            process_request(json.loads(request.body.decode('utf-8')))
        except Exception as e:
            pass
            # traceback.print_exc()
        return HttpResponse('OK')


def process_request(request):
    from .tasks import route_message
    """Handle all incoming message from facebook."""
    for entry in request.get("entry", []):
        timestamp = entry.get("time")
        message = entry.get("messaging")[0]
        sender_id = message.get("sender", dict()).get("id")
        message_content = message.get("message", dict())
        message_text = message_content.get("text")
        quick_reply = message_content.get("quick_reply", dict()).get("payload")
        attachment = message_content.get("attachments", list())
        attachment_type = None
        attachment_url = None
        if attachment:
            attachment_type = attachment[0].get("type")
            attachment_url = attachment[0].get("payload", dict()).get("url")
        postback = message.get('postback', dict()).get('payload')
        route_message(sender_id, message_text, quick_reply, postback, attachment_url, attachment_type)


def health_check(request):
    """Heath check needed for https validations"""
    from django.http import HttpResponse
    return HttpResponse('OK')


@xframe_options_exempt
def add_date(request):
    """Generates the date selection page"""
    return render(request, 'date_page.html')


@csrf_exempt
@xframe_options_exempt
def post_date(request):
    from .tasks import route_message
    from django.http import HttpResponse
    """User has selected and submited a date"""

    route_message(
        sender_id=request.POST.get('sender_id'),
        message_text=request.POST.get('date'),
        quick_reply=None,
        postback=None,
        attachment_url=None,
        attachment_type=None
    )
    return HttpResponse('OK')


@xframe_options_exempt
def update_project(request):
    from bot.models import Project
    from bot.lib.maker import get_maker_id
    from common.utilities import get_file_url
    """Generates all inprogress projects for the user, allowing them to select which one to update."""

    maker_id = get_maker_id(request.GET.get('sender_id'))
    projects = Project.objects.filter(
        maker_id=maker_id
    ).exclude(
        finished=True
    ).filter(
        complete=True
    ).prefetch_related("tags").prefetch_related("patterns__files")
    # project name: str, project img: url, project id: str, project tags: str
    project_dicts = []
    for project in projects:
        project_dict = dict(
            id=project.id,
            name=project.name,
            img_url=get_file_url(project.patterns.first().files.first()),
            tags=", ".join([i.name for i in project.tags.all()])
        )
        project_dicts.append(project_dict)
    return render(request, 'projects.html', context=dict(projects=project_dicts))


@csrf_exempt
@xframe_options_exempt
def post_project(request):
    from .tasks import route_message
    from django.http import HttpResponse
    """User select a project from the list and routes to the next message"""

    route_message(
        sender_id=request.POST.get('sender_id'),
        message_text=None,
        quick_reply=None,
        postback=request.POST.get('project_id'),
        attachment_url=None,
        attachment_type=None
    )
    return HttpResponse('OK')


@xframe_options_exempt
def select_supply(request):
    from bot.models import Pattern, Material
    from bot.lib.maker import get_maker_id
    from common.utilities import get_file_url
    """Generates gallery for the user,
    allowing them to select which supplies they want to use."""

    supply_class = Pattern
    if "material" in request.path.lower():
        supply_class = Material
    maker_id = get_maker_id(request.GET.get('sender_id'))
    supplies = supply_class.objects.filter(
        maker_id=maker_id
    ).prefetch_related("tags").prefetch_related("files")
    supply_dicts = []
    for supply in supplies:
        supply_dict = dict(
            id=supply.id,
            img_url=get_file_url(supply.files.first()),
            tags=", ".join([i.name for i in supply.tags.all()])
        )
        supply_dicts.append(supply_dict)
    return render(request, 'supplies.html', context=dict(supplies=supply_dicts))


@csrf_exempt
@xframe_options_exempt
def post_supply(request):
    from .tasks import route_message
    from django.http import HttpResponse
    """User select a supply id from the list and routes to the next message"""

    route_message(
        sender_id=request.POST.get('sender_id'),
        message_text=None,
        quick_reply=None,
        postback=request.POST.get('supply_id'),
        attachment_url=None,
        attachment_type=None
    )
    return HttpResponse('OK')
