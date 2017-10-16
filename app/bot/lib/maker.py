def get_maker_id(sender_id):
    from common.utilities import generate_unique_key
    key = generate_unique_key(sender_id)
    return key


def create_maker(sender_id):
    from bot.models import Maker
    from bot.tasks import get_maker_profile
    maker, created = Maker.objects.get_or_create(id=get_maker_id(sender_id=sender_id),
                                                 defaults=dict(sender_id=sender_id))

    if created:
        get_maker_profile.delay(sender_id=sender_id)
    return maker, created


def update_maker(sender_id, conversation_stage, models=None):
    from bot.models import Maker
    maker = Maker.objects.get(id=get_maker_id(sender_id=sender_id))
    if models:
        pass
