def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.maker import get_maker_id
    from bot.lib.project import create_project
    from bot.models import Pattern
    """Takes in ``sender_id``, ``message_text``= text,``context``= project id
    updates project and sends a reponse.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str message_text: Any text written by the send in the chat interface
    :param dict context: attributes sent between conversations
    :param str attachment_type: dentifies attachment type i.e photo (optional, defaults to None)
    :param str attachment_url: The location of the attachment (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)
    :param str quick_reply: an automatic reply (optional, defaults to None)

    :returns: ``reponse``a dict with the next message to move the conversation,
    ``new_context``, and ``coverstation`` dict containing
    the next stage and task for the the bot
    """

    project, created = create_project(sender_id=sender_id, name=message_text)
    new_context = dict()
    
    if created:
        new_context = dict(project_id=str(project.id))
        response = dict(
            message_text = "That's a great name. So what are you making?", 
            quick_replies=[
                {
                    "content_type":"text",
                    "title":"New Pattern",
                    "payload":"ADD_PATTERN",
                }])
        if Pattern.objects.filter(maker_id=get_maker_id(sender_id=sender_id)).count() > 0:
            response['quick_replies'].append(
                {
                    "content_type": "text",
                    "title": "Select Pattern",
                    "payload": "SELECT_PATTERN",
                }
            )
        conversation = dict(name='create_project', stage='pattern_menu')
    else:
        response = dict(message_text = "It looks like you already have a project called {0}. What would you like to call this project?".format(message_text))
        conversation = dict(name='create_project', stage='name_project')
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

    if message_text:
        return True, dict()
    else:
        return False, dict(message_text='Please name your project first!')
