from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def facebook(request):
    import json, traceback
    from django.http import HttpResponse
    from bot.conversations.utilities import process_request
    if request.method == 'GET':
        return HttpResponse(request.GET['hub.challenge'])
    else:
        try:
            process_request(json.loads(request.body.decode('utf-8')))
        except Exception as e:
            print(e)
            traceback.print_exc()
        return HttpResponse('OK')
