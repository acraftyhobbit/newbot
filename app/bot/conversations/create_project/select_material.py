def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import update_project
    from .utilities import send_date_picker
    update_project(sender_id=sender_id, project_id=context["project_id"], material_id=postback)
    conversation = dict(name='create_project', stage='add_due_date')
    response = dict(message_text = "Awesome! That's all I need. When do you want to finish this project by")
    new_context = context
    
    response = send_date_picker(sender_id=sender_id)

    return response, new_context, conversation



def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    if postback:
        return True, dict(message_text='')
    else:
        return False, dict(message_text='Please select from the menu.')
    #TODO probably need to see what happen with other things here