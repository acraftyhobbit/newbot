from bot.models import Maker
from bot.conversations.create_project.utilities import format_supply_carousel
from bot.lib.maker import update_maker
from bot.lib.conversation import get_conversation_stage_id
maker = Maker.objects.first()

update_maker(sender_id=maker.sender_id, context=maker.context, conversation=dict(name='create_project', stage='add_material'))


from common.facebook import send_message
from app.settings import DOMAIN

r = send_message(sender_id=maker.sender_id, 
)
buttons=[
            
        ]
    )
