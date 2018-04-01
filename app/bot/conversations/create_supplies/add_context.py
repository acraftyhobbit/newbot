def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.material import update_material
    from bot.lib.pattern import update_pattern
    """Takes in ``sender_id``, ``message_text``= #keywords,``context``= project id
    updates supply and sends a reponse.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param dict context: attributes sent between conversations
    :param str attachment_type: dentifies attachment type i.e photo (optional, defaults to None)
    :param str attachment_url: The location of the attachment (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic reply (optional, defaults to None)

    :returns: ``reponse``a dict with the next message to move the conversation
    ``new_context`` dict supply type and id, and ``coverstation`` dict containing
    the next stage and task for the the bot
    """

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

    new_context = {'type': context['type'], '{0}_id'.format(context['type']): str(supply.id)}

    if tags:
        response = dict(message_text="You're all done! Head back to the menu to continue.")
        conversation = dict(name='menu', stage='menu')
    else:
        response = dict(message_text="Great. Do you want to add any tags? If not, head back to the menu to continue.")
        conversation = dict(name='create_supplies', stage='add_tags')
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    """Takes in ``message_text``= text
    and determines if the message type is valid.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param str attachment_type: Identifies attachment type i.e photo (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic (optional, defaults to None)

    :returns: Booleen and a dict with message text if the message is not valid """

    if attachment_type in ['image'] or message_text:
        return True, dict()
    else:
        return False, dict(message_text='Want to add another photo or some tags?')
