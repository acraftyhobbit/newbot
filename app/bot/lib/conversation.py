def load_conversation(conversation_name, stage_name):
    import importlib
    conversation = importlib.import_module("bot.conversations.{0}.{1}".format(conversation_name, stage_name))
    return conversation


def get_conversation_id(name):
    from common.utilities import generate_unique_key
    key = generate_unique_key(name)
    return key


def get_conversation_stage_id(conversation_name, stage_name):
    from common.utilities import generate_unique_key
    key = generate_unique_key(conversation_name, stage_name)
    return key


def create_conversation(name):
    from bot.models import Conversation
    conversation, created = Conversation.objects.get_or_create(
        id=get_conversation_id(
            name=name
        ),
        defaults=dict(
            name=name
        )
    )
    return conversation


def create_conversation_stage(conversation_name, stage_name):
    from bot.models import ConversationStage

    conversation, created = ConversationStage.objects.get_or_create(
        id=get_conversation_stage_id(
            conversation_name=conversation_name,
            stage_name=stage_name
        ),
        defaults=dict(
            name=stage_name,
            conversation_id=get_conversation_id(name=conversation_name)
        )
    )
    return conversation
