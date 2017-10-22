def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.material import update_material
    from bot.lib.pattern import update_pattern
    tags = None
    
    if message_text:
        tags = [i.strip() for i in message_text.split('#')]
    file = None
    if attachment_url and attachment_type:
        file = dict(url=attachment_url, file_type=attachment_type)
    
    if context['type'] == 'material':
        supply = update_material(sender_id=sender_id, material_id=context['material_id'], file=file, tags=tags)
    
    else:
        supply = update_pattern(sender_id=sender_id, pattern_id=context['pattern_id'], file=file, tags=tags)
    
    new_context = {'type':context['type'], '{0}_id'.format(context['type']) : str(supply.id)}
    
    if tags:
        response = dict(message_text = "You're all done! Head back to the menu to continue.")
        conversation = dict(name='menu', stage='menu')
    else:
        response = dict(message_text = "Great. Do you want to add any tags? If not, head back to the menu to continue.")
        conversation = dict(name='create_supplies', stage='add_context')
    return response, new_context, conversation


def validate(message_text, attachment_type, postback, quick_reply):
    if attachment_type in ['image'] or message_text:
        return True, dict()
    else:
        return False, dict(message_text='Want to add more photos or tag this material?')