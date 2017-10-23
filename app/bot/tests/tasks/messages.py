from django.test import TestCase


class RouteMenuTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)

    def test_add_project(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_PROJECT_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        self.assertNotEqual(
            Maker.objects.get(sender_id=self.sender_id).conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )

    def test_update_project(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='UPDATE_PROJECT_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        self.assertNotEqual(
            Maker.objects.get(sender_id=self.sender_id).conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )

    def test_add_pattern(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_PATTERN_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        maker = Maker.objects.get(sender_id=self.sender_id)
        self.assertNotEqual(
            maker.conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )
        self.assertEqual(maker.context['type'], 'pattern')

    def test_add_material(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_MATERIAL_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        maker = Maker.objects.get(sender_id=self.sender_id)
        self.assertNotEqual(
            maker.conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )
        self.assertEqual(maker.context['type'], 'material')


class RouteMessageTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.tasks import route_message
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)

    def test_attachment(self):
        from bot.tasks import route_message
        from bot.models import File
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
            attachment_url='http://craftybot.com/image_1.jpg'
        )
        self.assertEqual(File.objects.all().count(), 1)


class RouteNewUserTestCase(TestCase):
    def setUp(self):
        self.sender_id = '1'

    def test_new_user(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='start',
            attachment_type=None,
            attachment_url=None
        )
        self.assertEqual(
            Maker.objects.get(sender_id=self.sender_id).conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )
