from django.test import TestCase, RequestFactory

#TODO select a existing pattern/material and due date

class NewProjectTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.tasks import route_message
        self.factory = RequestFactory()
        self.sender_id = '108886223055545'
        create_maker(sender_id=self.sender_id)

    def test_create_project(self):
        from bot.tasks import route_message
        from bot.models import Maker
        from bot.lib.conversation import get_conversation_stage_id
        from bot.views import post_date
        # Menu
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback='ADD_PROJECT_PAYLOAD',
            attachment_type=None,
            attachment_url=None
        )
        # Name Project
        route_message(
            sender_id=self.sender_id,
            message_text="project name",
            quick_reply=None,
            postback=None,
            attachment_type=None,
            attachment_url=None
        )
        # Select Add Pattern
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply='ADD_PATTERN',
            postback=None,
            attachment_type=None,
            attachment_url=None
        )
        # Add a pattern image
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback=None,
            attachment_type='image',
            attachment_url='http://craftybot.com/image_1.jpg'
        )
        # Select add  material
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply='ADD_MATERIAL',
            postback=None,
            attachment_type=None,
            attachment_url=None
        )
        # add a material Image
        route_message(
            sender_id=self.sender_id,
            message_text=None,
            quick_reply=None,
            postback=None,
            attachment_type='image',
            attachment_url='http://craftybot.com/image_2.jpg'
        )
        
        request = self.factory.post('bot/post_date', data=dict(sender_id=self.sender_id, date='2200-10-30'))
        r=post_date(request)
        self.assertEqual(r.status_code, 200)
        
        route_message(
            sender_id=self.sender_id,
            message_text="#pug #dogs",
            quick_reply=None,
            postback=None,
            attachment_type=None,
            attachment_url=None
        )
        maker = Maker.objects.get(sender_id=self.sender_id)
        self.assertEqual(maker.projects.count(), 1)
        self.assertEqual(maker.projects.filter(complete=True).count(), 1)
        project = maker.projects.first()
        self.assertEqual(project.materials.count(), 1)
        self.assertEqual(project.patterns.count(), 1)
        self.assertEqual(project.patterns.first().files.count(), 1)
        self.assertEqual(project.materials.first().files.count(), 1)
        self.assertEqual(project.tags.count(), 2)
