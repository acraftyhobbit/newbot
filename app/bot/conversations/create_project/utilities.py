def send_date_picker(sender_id):
    from app.settings import DOMAIN
    """ Utility function generates date picker web page for the user to select a specific date

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID

    :returns: Reponse dict with attachment to web url containing date selector
    """
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
    """ Utility function generates user stored patterns on web page for the user 
    to select a specific pattern id to use in the project

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID

    :returns: Reponse dict with attachment to web url containing date selector
    """
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
    """ Utility function generates user stored materials on web page for the user 
    to select a specific material id to use in the project

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID

    :returns: Reponse dict with attachment to web url containing date selector
    """
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
