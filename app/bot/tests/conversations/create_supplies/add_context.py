from django.test import TestCase


class AddMaterialSupplyContextTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.material import create_material
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)
        self.material_url = 'http://via.placeholder.com/350x150'
        self.material_url_2 = 'http://via.placeholder.com/350x350'
        self.material_type = 'image'
        self.tags = ['1', '2', '3']

        material = create_material(sender_id=self.sender_id, url=self.material_url, file_type=self.material_type)
        self.material_id = str(material.id)

    def test_add_tags_material(self):
        from bot.conversations.create_supplies import add_context
        from bot.models import Material
        response, new_context, conversation = add_context.respond(
            sender_id=self.sender_id,
            message_text='#dogs #pugs',
            attachment_type=None,
            attachment_url=None,
            postback=None,
            quick_reply=None,
            context=dict(type='material', material_id=self.material_id)
        )
        self.assertDictEqual(conversation, dict(name='menu', stage='menu'))
        self.assertEqual(Material.objects.get(id=self.material_id).tags.all().count(), 2)

    def test_add_image_material(self):
        from bot.models import Material
        from bot.conversations.create_supplies import add_context
        response, new_context, conversation = add_context.respond(
            sender_id=self.sender_id,
            message_text=None,
            attachment_type=self.material_type,
            attachment_url=self.material_url_2,
            postback=None,
            quick_reply=None,
            context=dict(type='material', material_id=self.material_id)
        )
        self.assertEqual(Material.objects.get(id=self.material_id).files.all().count(), 2)


class AddPatternContextTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.pattern import create_pattern
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)
        self.pattern_url = 'http://via.placeholder.com/350x150'
        self.pattern_url_2 = 'http://via.placeholder.com/350x350'
        self.pattern_type = 'image'
        self.tags = ['1', '2', '3']

        pattern = create_pattern(sender_id=self.sender_id, url=self.pattern_url, file_type=self.pattern_type)
        self.pattern_id = str(pattern.id)

    def test_add_tags_material(self):
        from bot.conversations.create_supplies import add_context
        from bot.models import Pattern
        response, new_context, conversation = add_context.respond(
            sender_id=self.sender_id,
            message_text='#dogs #pugs',
            attachment_type=None,
            attachment_url=None,
            postback=None,
            quick_reply=None,
            context=dict(type='pattern', pattern_id=self.pattern_id)
        )
        self.assertDictEqual(conversation, dict(name='menu', stage='menu'))
        self.assertEqual(Pattern.objects.get(id=self.pattern_id).tags.all().count(), 2)

    def test_add_image_material(self):
        from bot.models import Pattern
        from bot.conversations.create_supplies import add_context
        response, new_context, conversation = add_context.respond(
            sender_id=self.sender_id,
            message_text=None,
            attachment_type=self.pattern_type,
            attachment_url=self.pattern_url_2,
            postback=None,
            quick_reply=None,
            context=dict(type='pattern', pattern_id=self.pattern_id)
        )
        self.assertEqual(Pattern.objects.get(id=self.pattern_id).files.all().count(), 2)


class ValidateAddContextTestCase(TestCase):
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

    def test_valid_file(self):
        from bot.conversations.create_supplies.add_context import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='image',
            postback=None,
            quick_reply=None
        )
        self.assertTrue(valid)
