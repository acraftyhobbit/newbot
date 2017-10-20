def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.material import create_material
    from bot.lib.pattern import create_pattern

    if context['type'] == 'material':
        supply = create_material(sender_id=sender_id, url=attachment_url, file_type=attachment_type)
    else:
        supply = create_pattern(sender_id=sender_id, url=attachment_url, file_type=attachment_type)

    new_context = {'type':context['type'], '{0}_id'.format(context['type']) : str(supply.id)}
    conversation = dict(name='create_supplies', stage='add_context')
    response = dict(message_text = "Awesome! That's all I need. Or you can upload another photo or add some hashtags")
    return response, new_context, conversation


def validate(message_text, attachment_type, postback, quick_reply):
    if attachment_type in ['image']:
        return True, dict(message_text='')
    else:
        return False, dict(message_text='Please take a photo to proceed')