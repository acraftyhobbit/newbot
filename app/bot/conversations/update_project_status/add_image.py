def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project_status import create_project_status
    """Takes in ``sender_id``, ``attachment_type``= photo,``attachment_url``= url,
     ``context`` = supply id and creates supply and sends a reponse.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str attachment_type: dentifies attachment type i.e photo
    :param str attachment_url: The location of the attachment
    :param dict context: attributes sent between conversation in the case project_id
    :param str message_text: Any text written in the chat interface (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic reply (optional, defaults to None)

    :returns: ``reponse``a dict with the next message to move the conversation
    ``new_context`` dict with project id, and ``coverstation`` dict containing
    the next stage and task for the the bot
    """

    project_status = create_project_status(sender_id=sender_id, project_id=context['project_id'], url=attachment_url,
                                           file_type=attachment_type)
    new_context = dict(project_status_id=str(project_status.id))
    conversation = dict(name='update_project_status', stage='how_complete')
    response = dict(message_text="Awesome! Now tell me what pecentage between 1 - 100 complete are you?")
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    """Takes in ``attachment_type``= photo
    and determines if the message type is valid.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str attachment_type: Identifies attachment type i.e photo
    :param str message_text: Any text written in the chat interface(optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic (optional, defaults to None)

    :returns: Booleen and a dict with message text if the message is not valid """

    if attachment_type in ['image']:
        return True, dict(message_text='')
    else:
        return False, dict(message_text='Please take a photo to update your project')
