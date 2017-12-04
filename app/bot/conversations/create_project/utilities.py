def format_supply_carousel(supply_query_set,):
    from common.utilities import get_file_url
    carousel = {
            "type":"template",
            "payload":{
            "template_type":"generic",
            "elements":[]
        }
    }
    ''' supply_count = supply_query_set.count()
    supply_query_set.prefetch_related('files').prefetch_related('tags')
    if page > 0:
        carousel['payload']['elements'].append(
            {
            "title": "Go Back",
            "image_url": 'http://via.placeholder.com/250x250',
            "buttons": [
                {
                    "title": "Click to Go Back",
                    "type": "postback",
                    "payload": "VIEW_MORE_{0}".format(page-1)
                }
            ]
        }
    ) '''
    for supply in supply_query_set:
        element = {
            "title": " ".join(["#{0}".format(tag.name) for tag in supply.tags.all()]),
            "image_url": get_file_url(supply.files.first()),
            "buttons": [
                {
                    "title": "Select",
                    "type": "postback",
                    "payload": str(supply.id)
                }
            ]
        }
        if len(element['title'])> 30:
            element['title'] = element['title'][:30] + '...'
        elif len(element['title']) == 0:
            element['title'] = supply._meta.model_name
        carousel['payload']['elements'].append(
            element
        )
    """if supply_count > 9*(page+1):
        carousel['payload']['elements'].append(
            {
                "title": "View More",
                "image_url": 'http://via.placeholder.com/250x250',
                "webview_height_ratio": "full",
                "buttons": [
                    {
                        "title": "Click to View More",
                        "type": "postback",
                        "payload": "VIEW_MORE_{0}".format(page+1)
                    }
            ]
        }
    )"""
    return carousel

def send_date_picker(sender_id):
    from app.settings import DOMAIN
    response = dict(
        attachment = {
            "type": "template",
            "payload": {
                "template_type":"button",
                "text":"Awesome! That's all I need. When do you want to finish this project by",
                "buttons":[
                    {
                        "type":"web_url",
                        "url":"{0}/bot/date/?sender_id={1}".format(DOMAIN, sender_id),
                        "title":"Select Due Date",
                        "messenger_extensions": True
                    }
                ]
            }
        }
    )
    return response

def send_patterns(sender_id):
    from app.settings import DOMAIN
    response = dict(
        attachment={
        "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Which pattern do you want add to your project?",
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "{0}/bot/pattern/?sender_id={1}".format(DOMAIN, sender_id),
                            "title": "Select A Pattern",
                            "messenger_extensions": True
                        }
                    ]
                }
        }
    )
    return response


def send_materials(sender_id):
    from app.settings import DOMAIN
    response = dict(
        attachment={
            "type": "template",
            "payload": {
                    "template_type": "button",
                    "text": "Which material do you want add to your project?",
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "{0}/bot/material/?sender_id={1}".format(DOMAIN, sender_id),
                            "title": "Select A Material",
                            "messenger_extensions": True
                        }
                    ]
            }
        }
    )
    return response
