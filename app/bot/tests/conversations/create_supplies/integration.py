from django.test import TestCase


class CreateSuppliesTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        self.sender_id = '108886223055545'
        create_maker(sender_id=self.sender_id)

    def test_create_pattern(self):
        from bot.tasks import route_message
        from bot.models import Maker
        from bot.lib.conversation import get_conversation_stage_id
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_PATTERN_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback=None,
            attachment_type='image',
            attachment_url='http://via.placeholder.com/350x150'
        )
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback=None,
            attachment_type='image',
            attachment_url='http://via.placeholder.com/350x350'
        )
        route_message(
            sender_id=self.sender_id,
            message_text="#pug #dogs",
            quick_reply=None,
            postback=None,
            attachment_type=None,
            attachment_url=None
        )
        maker = Maker.objects.get(sender_id=self.sender_id)
        self.assertEqual(maker.patterns.all().count(), 1)
        self.assertEqual(maker.patterns.first().files.all().count(), 2)
        self.assertEqual(maker.patterns.first().tags.all().count(), 2)
        self.assertEqual(
            maker.conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )

    def test_create_material(self):
        from bot.tasks import route_message
        from bot.models import Maker
        from bot.lib.conversation import get_conversation_stage_id
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_MATERIAL_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback=None,
            attachment_type='image',
            attachment_url='http://via.placeholder.com/350x150'
        )
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback=None,
            attachment_type='image',
            attachment_url='http://via.placeholder.com/350x350'
        )
        route_message(
            sender_id=self.sender_id,
            message_text="#pug #dogs",
            quick_reply=None,
            postback=None,
            attachment_type=None,
            attachment_url=None
        )
        maker = Maker.objects.get(sender_id=self.sender_id)
        self.assertEqual(maker.materials.all().count(), 1)
        self.assertEqual(maker.materials.first().files.all().count(), 2)
        self.assertEqual(maker.materials.first().tags.all().count(), 2)
        self.assertEqual(
            maker.conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )
