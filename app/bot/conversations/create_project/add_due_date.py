def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import update_project
    project = update_project(sender_id=sender_id, project_id=context['project_id'], date_string=message_text)
    print(project.complete)
    new_context = context
    
    response = dict(message_text = "Great. Do you want to add tags? or ... head back to the menu if you are done.")
    conversation = dict(name='create_project', stage='add_tags')
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    from datetime import datetime
    try:
        date = datetime.strptime(message_text, '%Y-%m-%d')
    except ValueError:
        print('FUCKKK')
        return False, dict(message_text='Sorry I need a date like YYYY-MM-DD')
    else:
        if date > datetime.now():
            print('yay!')
            return True, dict()
        else:
            print('time_traveler')
            return False, dict(message_text='Woah a time traveler. Seriously though, when do you want to finish this... in the future.')
        