def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import update_project

    

    new_context = dict(project_id = postback)
    conversation = dict(name='update_project_status', stage='add_image')
    response = dict(message_text = "Great! Take or upload a image to update your progress")
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    if postback:
        return True, dict(message_text='')
    else:
        return False, dict(message_text='You need to select a project from the menu')