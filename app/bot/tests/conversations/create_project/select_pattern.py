def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import add_pattern
    
    add_pattern(project=context["project_id"], pattern_id=postback)
    new_context = context
    conversation = dict(name='create_project', stage='material_menu')
    response = dict(message_text="Great! Now you want to add a new material or select an existing one?", quick_replies=[
                {
                    "content_type":"text",
                    "title":"New Material",
                    "payload":"ADD_MATERIAL",
                },
                {
                    "content_type":"text",
                    "title":"Select Material",
                    "payload":"SELECT_MATERIAL",
                },
            ]
    )
    return response, new_context, conversation



def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    if postback:
        return True, dict(message_text='')
    else:
        return False, dict(message_text='Please select from the menu.')
    #TODO probably need to see what happen with other things here