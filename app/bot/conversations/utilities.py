def load_conversation(conversation_name, stage_name):
    import importlib
    conversation = importlib.import_module("bot.conversations.{0}.{1}".format(conversation_name, stage_name))
    return conversation


def process_request(request):
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
        if postback in ["ADD_PROJECT_PAYLOAD", "UPDATE_PROJECT_PAYLOAD", "ADD_PATTERN_PAYLOAD", "ADD_MATERIAL_PAYLOAD"]:
            handle_menu(sender_id, postback)
        elif postback == "START":
            handle_start(sender_id)
        else:
            process_message(sender_id, message_text, quick_reply, postback, attachment_url, attachment_type)


def process_message(sender_id, message_text, quick_reply, postback, attachment_url, attachment_type):
    from common.facebook import send_message
    from bot.models import Maker
    from bot.lib.maker import get_maker_id, update_maker
    send_message(sender_id=sender_id, action='mark_seen')
    maker = Maker.objects.prefetch_related("conversation_stage__conversation").get(id = get_maker_id(sender_id=sender_id))

    conversation = load_conversation(conversation_name=maker.conversation_stage.conversation.name, stage_name=maker.conversation_stage.name)
    valid, failure_response = conversation.validate(message_text=message_text, quick_reply=quick_reply,
                                                    postback=postback, attachment_type=attachment_type)
    if not valid:
        send_message(
            sender_id=sender_id,
            text=failure_response.get('message_text'),
            buttons=failure_response.get('buttons'),
            quick_replies=failure_response.get('quick_replies')
        )
    else:
        send_message(sender_id=sender_id, action='typing_on')
        response, context, next_conversation = conversation.respond(
            maker=maker,
            message_text=message_text,
            quick_reply=quick_reply,
            postback=postback,
            attachment_type=attachment_type,
            attachment_url=attachment_url
        )
        send_message(
            sender_id=sender_id,
            text=response.get('message_text'),
            buttons=response.get('buttons'),
            quick_replies=response.get('quick_replies')
        )
        update_maker(sender_id=sender_id, context=context, conversation=next_conversation)
    return valid


def handle_menu(sender_id, postback):
    from bot.lib.maker import update_maker
    from common.facebook import send_message
    context = None
    conversation = dict()
    if postback == "ADD_PROJECT_PAYLOAD":
        conversation=dict(name="create_project", stage="name_project")
        # TODO handle when a user has too many projects
        message_text = "Great! What would you like to call this project?"
    
    elif postback == "UPDATE_PROJECT_PAYLOAD":
        conversation=dict(name="update_project_status", stage="select_project")
        
        # TODO handle when a user has no unfinished projects
        message_text = "Please select a project"
    
    elif postback in ["ADD_PATTERN_PAYLOAD", "ADD_MATERIAL_PAYLOAD"]:
        conversation=dict(name="create_supplies", stage="add_image")
        context=dict(type = postback.replace.split("_")[1].lower())
        message_text = "Awesome! Please take a photo of the {0} to get started".format(context['type'])
    
    update_maker(sender_id=sender_id, conversation=conversation, context=context)
    send_message(sender_id=sender_id, text=message_text)

def handle_start(sender_id):
    from bot.lib.maker import create_maker
    from common.facebook import send_message
    create_maker(sender_id=sender_id)
    send_message(sender_id=sender_id, text="Welcome to CraftyBot select from menu to get started")

