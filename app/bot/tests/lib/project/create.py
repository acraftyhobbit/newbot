from django.test import TestCase


class CreateProjectTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.project import create_project

        self.sender_id = '1'
        self.project_name = 'test_project'
        create_maker(sender_id=self.sender_id)
        create_project(sender_id=self.sender_id, name=self.project_name)

    def test_create_new_project(self):
        from bot.lib.project import create_project
        from bot.models import Project
        new_project_name = 'new_project'

        create_project(sender_id=self.sender_id, name=new_project_name)
        self.assertEqual(Project.objects.filter(name=new_project_name).filter(maker__sender_id=self.sender_id).count(),
                         1)

    def test_create_existing_project(self):
        from bot.lib.project import create_project
        from bot.models import Project
        create_project(sender_id=self.sender_id, name=self.project_name)
        self.assertEqual(Project.objects.filter(name=self.project_name).filter(maker__sender_id=self.sender_id).count(),
                         1)
