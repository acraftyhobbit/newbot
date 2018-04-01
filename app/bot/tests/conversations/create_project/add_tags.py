from django.test import TestCase


class ValidateAddtagsCreateProjectTestCase(TestCase):
    def test_empty_message(self):
        from bot.conversations.create_supplies.add_context import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_video(self):
        from bot.conversations.create_supplies.add_context import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='video',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_valid_tags(self):
        from bot.conversations.create_supplies.add_context import validate
        valid, message = validate(
            sender_id='1',
            message_text='#pugs #dogs',
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertTrue(valid)
