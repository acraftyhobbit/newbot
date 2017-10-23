def get_maker_id(sender_id):
    from common.utilities import generate_unique_key
    key = generate_unique_key(sender_id)
    return key


def create_maker(sender_id):
    from bot.models import Maker
    from bot.tasks import get_maker_profile
    from bot.lib.conversation import get_conversation_stage_id
    maker, created = Maker.objects.get_or_create(
        id=get_maker_id(sender_id=sender_id),
        defaults=dict(
            sender_id=sender_id,
            conversation_stage_id=get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )
    )

    if created:
        get_maker_profile.delay(sender_id=sender_id)
    return maker, created


def update_maker(sender_id, conversation, context=None):
    from bot.models import Maker
    from bot.lib.conversation import get_conversation_stage_id
    maker = Maker.objects.get(id=get_maker_id(sender_id=sender_id))
    maker.conversation_stage_id = get_conversation_stage_id(
        conversation_name=conversation['name'],
        stage_name=conversation['stage']
    )
    maker.context = context
    maker.save()
    return maker
