from django.test import TestCase


class RouteMenuTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)

    def test_add_project(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_PROJECT_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        self.assertNotEqual(
            Maker.objects.get(sender_id=self.sender_id).conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )

    def test_update_project_no_projects(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='UPDATE_PROJECT_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        self.assertEqual(
            Maker.objects.get(sender_id=self.sender_id).conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )

    def test_update_project_with_projects(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        from bot.lib.maker import create_maker
        from bot.lib.project import create_project, update_project
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
        self.update_url = 'http://via.placeholder.com/350x150'
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
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='UPDATE_PROJECT_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        self.assertNotEqual(
            Maker.objects.get(sender_id=self.sender_id).conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )

    def test_add_pattern(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_PATTERN_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        maker = Maker.objects.get(sender_id=self.sender_id)
        self.assertNotEqual(
            maker.conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )
        self.assertEqual(maker.context['type'], 'pattern')

    def test_add_material(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_MATERIAL_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        maker = Maker.objects.get(sender_id=self.sender_id)
        self.assertNotEqual(
            maker.conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )
        self.assertEqual(maker.context['type'], 'material')


class RouteMessageTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)

    def test_attachment(self):
        from bot.tasks import route_message
        from bot.models import File
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_PATTERN_PAYLOAD',
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
        self.assertEqual(File.objects.all().count(), 1)


class RouteNewUserTestCase(TestCase):
    def setUp(self):
        self.sender_id = '1'

    def test_new_user(self):
        from bot.tasks import route_message
        from bot.lib.conversation import get_conversation_stage_id
        from bot.models import Maker
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='start',
            attachment_type=None,
            attachment_url=None
        )
        self.assertEqual(
            Maker.objects.get(sender_id=self.sender_id).conversation_stage_id,
            get_conversation_stage_id(conversation_name='menu', stage_name='menu')
        )
