def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import create_project
    from bot.models import Material
    from bot.lib.maker import get_maker_id
    from .utilities import format_supply_carousel, send_materials
    """Takes in ``sender_id``, ``message_text``= add or select, ``quick_reply`` = add or select
    ``context``= project id and updates project and sends a reponse.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str quick_reply: an automatic reply
    :param str message_text: Any text written in the chat interface
    :param dict context: attributes sent between conversations
    :param str attachment_type: dentifies attachment type i.e photo (optional, defaults to None)
    :param str attachment_url: The location of the attachment (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)

    :returns: ``reponse``a dict with the next message to move the conversation
    ``new_context`` context project id, and ``coverstation`` dict containing
    the next stage and task for the the bot
    """

    action = 'add'
    if (quick_reply and 'select' in quick_reply.lower()) or (message_text and 'select' in message_text.lower()):
        action = 'select'

    conversation = dict(name='create_project', stage='{0}_material'.format(action))

    new_context = context

    if action == 'select':
        maker_id = get_maker_id(sender_id=sender_id)
        materials = Material.objects.filter(maker_id=maker_id)
        if materials.count() <= 2:
            response = dict(attachment=format_supply_carousel(
                supply_query_set=materials))
        elif materials.count() > 2:
            response = send_materials(sender_id=sender_id)
    else:
        response = dict(message_text='Take a photo of your material')
    return response, new_context, conversation


def validate(sender_id, message_text, attachment_type, postback, quick_reply):
    """Boolean takes in ``message_text``= add or select or ``postback`` == add or select 
    and determines if the message type and text is valid.

    :param str sender_id: The unique id created by facebook and the current facebook's sender's ID
    :param str quick_reply: an automatic reply
    :param str message_text: Any text written in the chat interface (optional, defaults to None)
    :param str attachment_type: Identifies attachment type i.e photo (optional, defaults to None)
    :param str postback: a reponse sent from the user clicking a button (optional, defaults to None)

    :returns: Booleen and a dict with message text  and quick replies if the message is not valid """

    if quick_reply and quick_reply.lower() in ['add_material', 'select_material']:
        return True, dict()
    elif message_text and ('add' in message_text.lower() or 'select' in message_text.lower()) and 'material' in message_text.lower():
        return True, dict()
    else:
        return False, dict(message_text="I'm sorry, did you want to add a new material or select an existing one?", quick_replies=[
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
