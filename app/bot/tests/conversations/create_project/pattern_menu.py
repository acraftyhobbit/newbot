from django.test import TestCase


class ValidatePatternMenuCreateProjectTestCase(TestCase):
    def test_empty_message(self):
        from bot.conversations.create_project.pattern_menu import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_image(self):
        from bot.conversations.create_project.pattern_menu import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='image',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_valid_text(self):
        from bot.conversations.create_project.pattern_menu import validate
        valid, message = validate(
            sender_id='1',
            message_text='add_pattern',
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertTrue(valid)

    def test_valid_quick_reply(self):
        from bot.conversations.create_project.pattern_menu import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type=None,
            postback=None,
            quick_reply='select_pattern'
        )
        self.assertTrue(valid)
