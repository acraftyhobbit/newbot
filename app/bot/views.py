from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


@csrf_exempt
def facebook(request):
    import json, traceback
    from django.http import HttpResponse
    if request.method == 'GET':
        return HttpResponse(request.GET['hub.challenge'])
    else:
        try:
            process_request(json.loads(request.body.decode('utf-8')))
        except Exception as e:
            print(e)
            traceback.print_exc()
        return HttpResponse('OK')


def process_request(request):
    from .tasks import route_message

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

@xframe_options_exempt
def add_date(request):
    return render(request,'date_page.html')

@csrf_exempt
@xframe_options_exempt
def post_date(request):
    from .tasks import route_message
    from django.http import HttpResponse
    route_message(
        sender_id=request.POST.get('sender_id'),
        message_text=request.POST.get('date'),
        quick_reply=None,
        postback=None,
        attachment_url=None, 
        attachment_type=None
    )
    return HttpResponse('OK')
