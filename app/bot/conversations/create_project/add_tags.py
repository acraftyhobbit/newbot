def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import update_project
    
    tags = [i.strip() for i in message_text.split('#')]
    update_project(sender_id=sender_id, project_id=context['project_id'], tags=tags)
    new_context = context
    
    response = dict(message_text = "You're all done! Head back to the menu if you want to do anything else")
    conversation = dict(name='menu', stage='menu')
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    if message_text:
        return True, dict()
    else:
        return False, dict(message_text='Want to add some tags?')