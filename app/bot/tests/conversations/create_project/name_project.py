from django.test import TestCase


class ValidateNameProjectTestCase(TestCase):
    def test_empty_message(self):
        from bot.conversations.create_project.name_project import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_video(self):
        from bot.conversations.create_project.name_project import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='video',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_valid_name(self):
        from bot.conversations.create_project.name_project import validate
        valid, message = validate(
            sender_id='1',
            message_text='test project',
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertTrue(valid)

    def test_image(self):
        from bot.conversations.create_project.name_project import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='image',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)
