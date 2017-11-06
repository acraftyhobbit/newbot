from django.test import TestCase

class ValidateSelectMaterialCreateProjectTestCase(TestCase):
    def setUp(self):
        from bot.lib.material import create_material
        from bot.lib.maker import create_maker
        maker, created = create_maker(sender_id='1')
        material = create_material(sender_id=maker.sender_id, url="testing.com/image", file_type='image')
        material_2 = create_material(sender_id=maker.sender_id, url='testing.com/image_2', file_type='image')
        self.material = material
    
    def test_empty_message(self):
        from bot.conversations.create_project.select_material import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_image(self):
        from bot.conversations.create_project.select_material import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='image',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_valid_project(self):
        from bot.conversations.create_project.select_material import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type=None,
            postback=str(self.material.id),
            quick_reply=None
        )
        self.assertTrue(valid)

    def test_text(self):
        from bot.conversations.create_project.select_material import validate
        valid, message = validate(
            sender_id='1',
            message_text='hello',
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)