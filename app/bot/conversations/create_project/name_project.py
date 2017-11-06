def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.maker import get_maker_id
    from bot.lib.project import create_project
    from bot.models import Pattern
    
    project, created = create_project(sender_id=sender_id, name=message_text)
    new_context = dict()
    
    if created:
        new_context = dict(project_id=str(project.id))
        response = dict(
            message_text = "That's a great name. So what are you making?", 
            quick_replies=[
                {
                    "content_type":"text",
                    "title":"New Pattern",
                    "payload":"ADD_PATTERN",
                }])
        if Pattern.objects.filter(maker_id=get_maker_id(sender_id=sender_id)).count() > 0:
            response['quick_replies'].append(
                {
                    "content_type": "text",
                    "title": "Select Material",
                    "payload": "SELECT_MATERIAL",
                }
            )
        conversation = dict(name='create_project', stage='pattern_menu')
    else:
        response = dict(message_text = "It looks like you already have a project called {0}. What would you like to call this project?".format(message_text))
        conversation = dict(name='create_project', stage='name_project')
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    if message_text:
        return True, dict()
    else:
        return False, dict(message_text='Please name your project first!')
