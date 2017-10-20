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
        response, new_context, conversation = add_image.respond(sender_id=self.sender_id, message_text=None, attachment_type='image', attachment_url='http://craftybot.com/test_url_add_image.jpg', postback=None, quick_reply=None, context=context)
        self.assertIsNotNone(response)
        self.assertEqual(Maker.objects.get(sender_id='1').materials.count(), 1)
    
    def test_add_image_pattern(self):
        from bot.conversations.create_supplies import add_image
        from bot.models import Maker
        context = dict(type='pattern')
        response, new_context, conversation = add_image.respond(sender_id=self.sender_id, message_text=None, attachment_type='image', attachment_url='http://craftybot.com/test_url_add_image.jpg', postback=None, quick_reply=None, context=context)
        self.assertIsNotNone(response)
        self.assertEqual(Maker.objects.get(sender_id='1').patterns.count(), 1)