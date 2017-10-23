from django.test import TestCase


class SelectProjectTestCase(TestCase):
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
        self.due_date = '2018-01-01'
        self.tags = ['1', '2', '3']
        self.update_url = 'http://craftybot.com/test_status_image.jpg'
        self.update_type = 'image'
        create_maker(sender_id=self.sender_id)
        project, created = create_project(sender_id=self.sender_id, name=self.project_name)
        self.project = project
        self.material = create_material(sender_id=self.sender_id, url=self.material_url, file_type=self.material_type)
        self.pattern = create_pattern(sender_id=self.sender_id, url=self.pattern_url, file_type=self.pattern_type)

        update_project(
            sender_id=self.sender_id,
            project_id=str(self.project.id),
            date_string=self.due_date,
            material_id=str(self.material.id),
            pattern_id=str(self.pattern.id),
            tags=self.tags
        )

    def test_select_project(self):
        from bot.conversations.update_project_status import project_selection

        response, new_context, conversation = project_selection.respond(
            sender_id=self.sender_id,
            message_text=None,
            attachment_type=None,
            attachment_url=None,
            postback=str(self.project.id),
            quick_reply=None,
            context=None)
        self.assertEqual(new_context["project_id"], str(self.project.id))
