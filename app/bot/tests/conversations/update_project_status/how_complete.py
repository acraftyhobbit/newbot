from django.test import TestCase


class HowCompleteTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.project import create_project, update_project
        from bot.lib.material import create_material
        from bot.lib.pattern import create_pattern
        from bot.lib.project_status import create_project_status
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
        self.project_status = create_project_status(
            sender_id=self.sender_id,
            project_id=str(self.project.id),
            url=self.update_url,
            file_type=self.update_type
        )

    def test_how_complete(self):
        from bot.conversations.update_project_status import how_complete
        from bot.models import ProjectStatusCompletion

        response, new_context, conversation = how_complete.respond(
            sender_id=self.sender_id,
            message_text='80',
            attachment_type=None,
            attachment_url=None,
            postback=None,
            quick_reply=None,
            context=dict(project_status_id=str(self.project_status.id))
        )
        self.assertEqual(ProjectStatusCompletion.objects.get(project_status=self.project_status).percentage, 80)
