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
        process_message(sender_id, message_text, quick_reply, postback, attachment_url, attachment_type)

def process_message(sender_id, message_text, quick_reply, postback, attachment_url, attachment_type):
    # TODO get current conversation & stage - DATABASE
    current_conversation = None
    conversation = load_conversation(conversation_name=current_conversation.name, stage_name=current_conversation.stage)
    valid, failure_response = conversation.validate(message_text=message_text, quick_reply=quick_reply, postback=postback, attachment_type=attachment_type)
    if not valid:
        send_facebook_message(
            sender_id=sender_id, 
            message_text=failure_response.get('message_text'), 
            buttons=failure_response.get('buttons'), 
            quick_replies=failure_response.get('quick_replies')
        )
    else:
        # TODO get current context (project_id, status_update_id, etc.) - DATABASE
        response, next_conversation  = conversation.respond(
            sender_id=sender_id,
            message_text=message_text, 
            quick_reply=quick_reply, 
            postback=postback, 
            attachment_type=attachment_type,
            attachment_url=attachment_url
        )
        # TODO update context - DATABASE
        send_facebook_message(
            sender_id=sender_id, 
            message_text=response.get('message_text'), 
            buttons=response.get('buttons'), 
            quick_replies=response.get('quick_replies')
        )
        # TODO update stage - DATABASE
    return valid    

def send_facebook_message(sender_id, message_text, buttons, quick_replies):
    pass