from celery import shared_task


@shared_task()
def route_message(sender_id, message_text, quick_reply, postback, attachment_url, attachment_type):
    """Routes messages to New User setup, ongoing conversation, and handles menu conversation interrupts"""

    if isinstance(postback, str) and postback.upper() in ["ADD_PROJECT_PAYLOAD", "UPDATE_PROJECT_PAYLOAD",
                                                          "ADD_PATTERN_PAYLOAD", "ADD_MATERIAL_PAYLOAD"]:
        process_menu_selection(sender_id, postback)
    elif isinstance(postback, str) and postback.upper() == "START":
        welcome_new_user(sender_id)
    else:
        process_message(sender_id, message_text, quick_reply, postback, attachment_url, attachment_type)


def process_message(sender_id, message_text, quick_reply, postback, attachment_url, attachment_type):
    from common.facebook import send_message
    from bot.models import Maker
    from bot.lib.maker import get_maker_id, update_maker
    from bot.lib.conversation import load_conversation
    """Processes user input and responds with the next stage of the conversation.

    Function processes user input, loads the current conversation and validates the input before continuing. Bot responds
    with a prompt for valid input or continues the conversation. 

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param str attachment_type: dentifies attachment type i.e photo (optional, defaults to None)
    :param str attachment_url: The location of the attachment (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic reply (optional, defaults to None)

    :returns: ``valid`` a boolean whether the message was valid
    """
    send_message(sender_id=sender_id, action='mark_seen')
    maker = Maker.objects.prefetch_related("conversation_stage__conversation").get(id=get_maker_id(sender_id=sender_id))
    # Loads conversation by name.
    # #Conversations are located in bot/conversations/{conversation_name}/{stage_name}.py
    conversation = load_conversation(
        conversation_name=maker.conversation_stage.conversation.name,
        stage_name=maker.conversation_stage.name
    )

    valid, failure_response = conversation.validate(
        sender_id=sender_id,
        message_text=message_text,
        quick_reply=quick_reply,
        postback=postback,
        attachment_type=attachment_type)
    if not valid:
        send_message(
            sender_id=sender_id,
            text=failure_response.get('message_text'),
            buttons=failure_response.get('buttons'),
            attachment=failure_response.get('attachment'),
            quick_replies=failure_response.get('quick_replies')
        )
    else:
        # Starts typing so that the user can see that the bot is processing.
        send_message(sender_id=sender_id, action='typing_on')
        response, context, next_conversation = conversation.respond(
            sender_id=sender_id,
            message_text=message_text,
            quick_reply=quick_reply,
            postback=postback,
            attachment_type=attachment_type,
            attachment_url=attachment_url,
            context=maker.context
        )
        r = send_message(
            sender_id=sender_id,
            text=response.get('message_text'),
            buttons=response.get('buttons'),
            attachment=response.get('attachment'),
            quick_replies=response.get('quick_replies')
        )
        # Sets the next stage of the conversation and persists and conversation context.
        update_maker(sender_id=sender_id, context=context, conversation=next_conversation)
    return valid


def process_menu_selection(sender_id, postback):
    from bot.lib.maker import update_maker, get_maker_id
    from common.facebook import send_message
    from bot.models import Project
    """"""
    context = dict()
    message_text = None
    conversation = dict()
    attachment = None
    if postback == "ADD_PROJECT_PAYLOAD":
        conversation = dict(name="create_project", stage="name_project")
        # TODO handle when user projects settings
        projects = Project.objects.filter(maker_id=get_maker_id(
            sender_id=sender_id)).filter(complete=True).exclude(finished=True)
        if projects.count() == 6:
            message_text = "Sorry it looks like you have max out your new project. You need to finish something before you can add anything new"
        else:
            message_text = "Great! What would you like to call this project?"

    elif postback == "UPDATE_PROJECT_PAYLOAD":
        conversation = dict(name="update_project_status", stage="project_selection")
        projects = Project.objects.filter(maker_id=get_maker_id(sender_id=sender_id)).filter(complete=True).exclude(
            finished=True)

        if projects.count() == 0:
            message_text = "It looks like you don't have any active projects. Add a project to get started!"
            conversation = dict(name="menu", stage="menu")
        elif projects.count() <= 2:
            attachment = format_project_carousel(projects=projects)
        elif projects.count() > 2:
            attachment = send_update_project(sender_id=sender_id)

    elif postback in ["ADD_PATTERN_PAYLOAD", "ADD_MATERIAL_PAYLOAD"]:
        conversation = dict(name="create_supplies", stage="add_image")
        context = dict(type=postback.split("_")[1].lower())
        message_text = "Awesome! Please take a photo of the {0} to get started".format(context['type'])
    update_maker(sender_id=sender_id, conversation=conversation, context=context)
    send_message(sender_id=sender_id, text=message_text, attachment=attachment)


def welcome_new_user(sender_id):
    from bot.lib.maker import create_maker
    from common.facebook import send_message
    """Creates the welcome message for a new user"""

    create_maker(sender_id=sender_id)
    send_message(sender_id=sender_id, text="Welcome to CraftyBot select from menu to get started")


def send_update_project(sender_id):
    from app.settings import DOMAIN
    """"""
    attachment = {
        "type": "template",
        "payload": {
            "template_type": "button",
            "text": "Which project do you want update today?",
            "buttons": [
                {
                    "type": "web_url",
                    "url": "{0}/bot/project/?sender_id={1}".format(DOMAIN, sender_id),
                    "title": "Select A Project",
                    "messenger_extensions": True
                }
            ]
        }
    }
    return attachment


def format_project_carousel(projects):
    from common.utilities import get_file_url
    carousel = {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": []
        }
    }
    for project in projects[0:10]:
        element = {
            "title": project.name,
            "subtitle": " ".join(["#{0}".format(tag.name) for tag in project.tags.all()]),
            "image_url": get_file_url(project.materials.first().files.first()),
            "buttons": [
                {
                    "title": "Select",
                    "type": "postback",
                    "payload": str(project.id)
                }
            ]
        }
        if len(element['subtitle']) > 30:
            element.pop('subtitle')
        if len(element['title']) > 30:
            element['title'] = element['title'][:30] + '...'
        carousel['payload']['elements'].append(
            element
        )
    return carousel
