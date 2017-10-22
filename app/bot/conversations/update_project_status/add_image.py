def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project_status import create_project_status 

    
    project_status = create_project_status(sender_id=sender_id, project_id=context['project_id'], url=attachment_url, file_type=attachment_type)
    new_context = dict(project_status_id = str(project_status.id))
    conversation = dict(name='update_project_status', stage='how_complete')
    response = dict(message_text = "Awesome! Now tell me what pecentage between 1 - 100 complete are you?")
    return response, new_context, conversation


def validate(message_text, attachment_type, postback, quick_reply):
    if attachment_type in ['image']:
        return True, dict(message_text='')
    else:
        return False, dict(message_text='Please take a photo to update your project')