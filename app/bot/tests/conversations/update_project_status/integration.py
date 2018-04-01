from django.test import TestCase


class UpdateProjectTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.pattern import create_pattern
        from bot.lib.material import create_material
        from bot.lib.project import create_project, update_project

        self.sender_id = '108886223055545'
        create_maker(sender_id=self.sender_id)
        project, created = create_project(sender_id=self.sender_id, name='Test_project')
        self.pattern = create_pattern(sender_id=self.sender_id, url='http://via.placeholder.com/350x150',
                                      file_type='image')
        self.material = create_material(
            sender_id=self.sender_id, url='http://via.placeholder.com/350x150', file_type='image')

        update_project(sender_id=self.sender_id, project_id=str(project.id), material_id=str(self.material.id),
                       pattern_id=str(self.pattern.id), date_string='2300-10-30')
        self.project = project
        project_2, created = create_project(sender_id=self.sender_id, name='Test_project_2')

    def test_project_selection(self):
        from bot.tasks import route_message
        from bot.models import Maker

        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback="UPDATE_PROJECT_PAYLOAD",
            attachment_type=None,
            attachment_url=None
        )
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback=str(self.project.id),
            attachment_type=None,
            attachment_url=None
        )
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback=None,
            attachment_type='image',
            attachment_url='http://via.placeholder.com/350x150'
        )

        route_message(
            sender_id=self.sender_id,
            message_text="25",
            quick_reply=None,
            postback=None,
            attachment_type=None,
            attachment_url=None
        )
        maker = Maker.objects.get(sender_id=self.sender_id)
        project = maker.projects.filter(id=self.project.id)
        self.assertEqual(maker.project_statuses.count(), 1)
        self.assertTrue(maker.project_statuses.first().complete)
        self.assertFalse(maker.project_statuses.first().project.finished)
        self.assertEqual(project.first().statuses.first(), maker.project_statuses.first())
