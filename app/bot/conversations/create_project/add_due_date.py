def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import update_project
    """Takes in ``sender_id``, ``message_text``= due date,``context``= project id
    and sends a reponse.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param dict context: attributes sent between conversation in the case project_id
    :param str attachment_type: dentifies attachment type i.e photo (optional, defaults to None)
    :param str attachment_url: The location of the attachment (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic reply (optional, defaults to None)

    :returns: ``reponse``a dict with the next message to move the conversation
    ``new_context`` same context as before, and ``coverstation`` dict containing
    the next stage and task for the the bot
    """

    project = update_project(sender_id=sender_id, project_id=context['project_id'], date_string=message_text)
    new_context = context

    response = dict(message_text="Great. Do you want to add tags? or ... head back to the menu if you are done.")
    conversation = dict(name='create_project', stage='add_tags')
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    from datetime import datetime
    """Boolean takes in ``message_text``= due date for the project
    and determines if the message type is valid.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param str attachment_type: Identifies attachment type i.e photo (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic (optional, defaults to None)

    :returns: Booleen and a dict with message text if the message is not valid """

    try:
        date = datetime.strptime(message_text, '%Y-%m-%d')
    except ValueError:
        return False, dict(message_text='Sorry I need a date like YYYY-MM-DD')
    else:
        if date > datetime.now():
            return True, dict()
        else:
            return False, dict(
                message_text='Woah a time traveler. Seriously though, when do you want to finish this... in the future.')
