from django.shortcuts import render

# Create your views here.
def facebook(request):
    import json
    from django.http import HttpResponse
    from bot.conversations.utilities import process_request
    if request.method == 'GET':
        return HttpResponse(request.GET['hub.challenge'])
    else:
        try:
            process_request(json.loads(request.body.encode('utf-8')))
        except Exception as e:
            print(e)
        return HttpResponse('OK')