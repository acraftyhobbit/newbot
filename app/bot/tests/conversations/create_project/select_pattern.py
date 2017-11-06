from django.test import TestCase

class ValidatePatternCreateProjectTestCase(TestCase):
    def setUp(self):
        from bot.lib.pattern import create_pattern
        from bot.lib.maker import create_maker
        maker, created = create_maker(sender_id='1')
        pattern = create_pattern(sender_id=maker.sender_id, url="testing.com/image", file_type='image')
        pattern_2 = create_pattern(sender_id=maker.sender_id, url='testing.com/image_2', file_type='image')
        self.pattern = pattern
    
    def test_empty_message(self):
        from bot.conversations.create_project.select_pattern import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_image(self):
        from bot.conversations.create_project.select_pattern import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='image',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_valid_project(self):
        from bot.conversations.create_project.select_pattern import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type=None,
            postback=str(self.pattern.id),
            quick_reply=None
        )
        self.assertTrue(valid)

    def test_text(self):
        from bot.conversations.create_project.select_pattern import validate
        valid, message = validate(
            sender_id='1',
            message_text='hello',
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)