from django.test import TestCase


class UpdateProjectTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.project import create_project
        from bot.lib.material import create_material
        from bot.lib.pattern import create_pattern

        self.sender_id = '1'
        self.pattern_url = 'http://via.placeholder.com/350x150'
        self.pattern_type = 'image'
        self.material_url = 'http://via.placeholder.com/350x150'
        self.material_type = 'image'
        self.project_name = 'test_project'
        self.due_date = '2017-01-01'
        self.tags = ['1', '2', '3']

        create_maker(sender_id=self.sender_id)
        project, created = create_project(sender_id=self.sender_id, name=self.project_name)
        self.project = project
        self.material = create_material(sender_id=self.sender_id, url=self.material_url, file_type=self.material_type)
        self.pattern = create_pattern(sender_id=self.sender_id, url=self.pattern_url, file_type=self.pattern_type)

    def test_add_material(self):
        from bot.lib.project import update_project
        from bot.models import ProjectMaterial
        update_project(sender_id=self.sender_id, project_id=str(self.project.id), material_id=str(self.material.id))
        self.assertEqual(ProjectMaterial.objects.filter(project=self.project).filter(material=self.material).count(), 1)

    def test_add_pattern(self):
        from bot.lib.project import update_project
        from bot.models import ProjectPattern
        update_project(sender_id=self.sender_id, project_id=str(self.project.id), pattern_id=str(self.pattern.id))
        self.assertEqual(ProjectPattern.objects.filter(project=self.project).filter(pattern=self.pattern).count(), 1)

    def test_add_due_date(self):
        from bot.lib.project import update_project
        from bot.models import ProjectDueDate, Project

        update_project(sender_id=self.sender_id, project_id=str(self.project.id), date_string=self.due_date)
        self.assertEqual(ProjectDueDate.objects.filter(project=self.project).count(), 1)
        self.assertTrue(Project.objects.get(id=str(self.project.id)).complete)

    def test_add_tags(self):
        from bot.lib.project import update_project
        from bot.models import ProjectTag

        update_project(sender_id=self.sender_id, project_id=str(self.project.id), tags=self.tags)
        self.assertEqual(ProjectTag.objects.filter(project=self.project).count(), 3)
