from django.test import TestCase


class AddImageSuppliesConversationTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)

    def test_add_image_material(self):
        from bot.conversations.create_supplies import add_image
        from bot.models import Maker
        context = dict(type='material')
        response, new_context, conversation = add_image.respond(
            sender_id=self.sender_id, message_text=None,
            attachment_type='image',
            attachment_url='http://via.placeholder.com/350x150',
            postback=None,
            quick_reply=None,
            context=context
        )
        self.assertIsNotNone(response)
        self.assertEqual(Maker.objects.get(sender_id='1').materials.count(), 1)

    def test_add_image_pattern(self):
        from bot.conversations.create_supplies import add_image
        from bot.models import Maker
        context = dict(type='pattern')
        response, new_context, conversation = add_image.respond(
            sender_id=self.sender_id, message_text=None,
            attachment_type='image',
            attachment_url='http://via.placeholder.com/350x150',
            postback=None,
            quick_reply=None,
            context=context
        )
        self.assertIsNotNone(response)
        self.assertEqual(Maker.objects.get(sender_id='1').patterns.count(), 1)


class ValidateAddImageSupplyConversationTestCase(TestCase):
    def setUp(self):
        pass

    def test_image(self):
        from bot.conversations.create_supplies.add_image import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='image',
            postback=None,
            quick_reply=None
        )
        self.assertTrue(valid)

    def test_add_video(self):
        from bot.conversations.create_supplies.add_image import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='video',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_add_string(self):
        from bot.conversations.create_supplies.add_image import validate
        valid, message = validate(
            sender_id='1',
            message_text='this should fail',
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)
