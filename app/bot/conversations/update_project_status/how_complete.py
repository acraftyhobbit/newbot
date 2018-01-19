def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project_status import update_project_status
    """Takes in ``sender_id``, ``message_text``= text, ``context``= project id
    updates project and sends a reponse.

    : param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    : param str message_text: Any text written by the send in the chat interface
    : param dict context: attributes sent between conversations
    : param str attachment_type: dentifies attachment type i.e photo(optional, defaults to None)
    : param str attachment_url: The location of the attachment(optional, defaults to None)
    : param str postback: a reponse sent from the user clicking a button(optional, defaults to None)
    : param str quick_reply: an automatic reply(optional, defaults to None)

    : returns: ``reponse``a dict with the next message to move the conversation,
    ``new_context``, and ``coverstation`` dict containing
    the next stage and task for the the bot
    """

    completion_percentage = int(message_text.strip())
    new_context = dict()
    project_status = update_project_status(sender_id=sender_id, project_status_id=context['project_status_id'], completion_percentage=completion_percentage)

    if completion_percentage == 100:
        response = dict(message_text = "Congrats on finishing your project! You now have room to start a new project. Use the main menu to do so")
    
    else:
        response = dict(message_text = "your project has be saved as {0} complete reminder it to due on {1}. Use the menu below if you need anything else".format(completion_percentage, project_status.project.project_due_date.due_date.date))
    conversation = dict(name='menu', stage='menu')
    return response, new_context, conversation

def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    """Takes in ``message_text``= text should be number
    and determines if the message type is valid.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param str attachment_type: Identifies attachment type i.e photo (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic (optional, defaults to None)

    :returns: Booleen and a dict with message text if the message is not valid """
    
    try:
        value = int(message_text.strip())
    except AttributeError:
        value = None
    except ValueError:
        value = None
    else:
        if 1 <= value <=100:
            value = value
        else:
            value = None
    if value:
        return True, dict()
    else:
        return False, dict(message_text='Please give me a number from 1 - 100 for the precentage complete')
