from django.test import TestCase


class ValidateAddPatterCreateProjectConversationTestCase(TestCase):
    def setUp(self):
        pass

    def test_image(self):
        from bot.conversations.create_project.add_pattern import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='image',
            postback=None,
            quick_reply=None
        )
        self.assertTrue(valid)

    def test_add_video(self):
        from bot.conversations.create_project.add_pattern import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='video',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_add_string(self):
        from bot.conversations.create_project.add_pattern import validate
        valid, message = validate(
            sender_id='1',
            message_text='this should fail',
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)
