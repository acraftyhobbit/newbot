def respond(sender_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    from bot.lib.project import create_project
    from bot.models import Material
    from bot.lib.maker import get_maker_id
    from .utilities import format_supply_carousel, send_materials
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
