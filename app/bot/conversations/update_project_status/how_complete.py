def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project_status import update_project_status

    completion_percentage = int(message_text.strip())
    new_context = None
    project_status = update_project_status(sender_id=sender_id, project_status_id=context['project_status_id'], completion_percentage=completion_percentage)

    if completion_percentage == 100:
        response = dict(message_text = "Congrats on finishing your project! You now have room to start a new project. Use the main menu to do so")
    
    else:
        response = dict(message_text = "your project has be saved as {0} complete reminder it to due on {1}. Use the menu below if you need anything else".format(completion_percentage, project_status.project.project_due_date.due_date.date))
    conversation = dict(name='menu', stage='menu')
    return response, new_context, conversation

def validate(message_text, attachment_type, postback, quick_reply):
    try:
        value = int(message_text.strip())
    except AttributeError:
        value = None
    except ValueError:
        value = None
    else:
        if 1 <= value <=100:
            value = value
        else:
            value = None
    if value:
        return True, dict()
    else:
        return False, dict(message_text='Please give me a number from 1 - 100 for the precentage complete')