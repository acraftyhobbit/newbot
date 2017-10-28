def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.material import update_material
    from bot.lib.pattern import update_pattern
    
    tags = [i.strip() for i in message_text.split('#')]
    file = None
    
    if context['type'] == 'material':
        supply = update_material(sender_id=sender_id, material_id=context['material_id'], file=file, tags=tags)
    
    else:
        supply = update_pattern(sender_id=sender_id, pattern_id=context['pattern_id'], file=file, tags=tags)
    
    new_context = {'type':context['type'], '{0}_id'.format(context['type']) : str(supply.id)}
    
    response = dict(message_text = "You're all done! Head back to the menu to continue.")
    conversation = dict(name='menu', stage='menu')
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    if message_text:
        return True, dict()
    else:
        return False, dict(message_text='Want to add some tags?')