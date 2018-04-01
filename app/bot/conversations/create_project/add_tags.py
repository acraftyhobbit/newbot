def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import update_project
    """Takes in ``sender_id``, ``message_text``= #keywords,``context``= project id
    updates project and sends a reponse.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param dict context: attributes sent between conversations
    :param str attachment_type: dentifies attachment type i.e photo (optional, defaults to None)
    :param str attachment_url: The location of the attachment (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic reply (optional, defaults to None)

    :returns: ``reponse``a dict with the next message to move the conversation
    ``new_context`` empty dict, and ``coverstation`` dict containing
    the next stage and task for the the bot
    """

    tags = [i.strip() for i in message_text.split('#')]
    update_project(sender_id=sender_id, project_id=context['project_id'], tags=tags)
    new_context = dict()

    response = dict(message_text="You're all done! Head back to the menu if you want to do anything else")
    conversation = dict(name='menu', stage='menu')
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    """Boolean takes in ``message_text``= text
    and determines if the message type is valid.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param str attachment_type: Identifies attachment type i.e photo (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic (optional, defaults to None)

    :returns: Booleen and a dict with message text if the message is not valid """

    if message_text:
        return True, dict()
    else:
        return False, dict(message_text='Want to add some tags?')
