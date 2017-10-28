def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.pattern import create_pattern
    from bot.lib.project import update_project
    pattern = create_pattern(sender_id=sender_id, url=attachment_url, file_type=attachment_type)
    update_project(sender_id=sender_id, project_id=context["project_id"], pattern_id=str(pattern.id))
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
    if attachment_type in ['image']:
        return True, dict(message_text='')
    else:
        return False, dict(message_text='Please take a photo to proceed')