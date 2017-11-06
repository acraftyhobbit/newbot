from django.test import TestCase


class AddImageTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.project import create_project, update_project
        from bot.lib.material import create_material
        from bot.lib.pattern import create_pattern
        self.sender_id = '1'
        self.pattern_url = 'http://craftybot.com/test_pattern_image.jpg'
        self.pattern_type = 'image'
        self.material_url = 'http://craftybot.com/test_material_image.jpg'
        self.material_type = 'image'
        self.project_name = 'test_project'
        self.due_date = '2017-01-01'
        self.tags = ['1', '2', '3']
        self.update_url = 'http://craftybot.com/test_status_image.jpg'
        self.update_type = 'image'
        create_maker(sender_id=self.sender_id)
        project, created = create_project(sender_id=self.sender_id, name=self.project_name)
        self.project = project
        self.material = create_material(sender_id=self.sender_id, url=self.material_url, file_type=self.material_type)
        self.pattern = create_pattern(sender_id=self.sender_id, url=self.pattern_url, file_type=self.pattern_type)
        self.update_url_2 = 'http://craftybot.com/test_status_image_2.jpg'
        update_project(
            sender_id=self.sender_id,
            project_id=str(self.project.id),
            date_string=self.due_date,
            material_id=str(self.material.id),
            pattern_id=str(self.pattern.id),
            tags=self.tags
        )

    def test_add_image(self):
        from bot.conversations.update_project_status import add_image
        from bot.models import ProjectStatus

        response, new_context, conversation = add_image.respond(
            sender_id=self.sender_id,
            message_text=None,
            attachment_type=self.update_type,
            attachment_url=self.update_url,
            postback=None,
            quick_reply=None,
            context=dict(project_id=str(self.project.id))
        )
        self.assertEqual(ProjectStatus.objects.filter(project_id=self.project.id).count(), 1)
        
class ValidateAddImageUpdateConversationTestCase(TestCase):
    def setUp(self):
        pass

    def test_image(self):
        from bot.conversations.update_project_status.add_image import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='image',
            postback=None,
            quick_reply=None
        )
        self.assertTrue(valid)

    def test_add_video(self):
        from bot.conversations.update_project_status.add_image import validate
        valid, message = validate(
            sender_id='1',
            message_text=None,
            attachment_type='video',
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)

    def test_add_string(self):
        from bot.conversations.update_project_status.add_image import validate
        valid, message = validate(
            sender_id='1',
            message_text='this should fail',
            attachment_type=None,
            postback=None,
            quick_reply=None
        )
        self.assertFalse(valid)