from django.test import TestCase


class GetMakerTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)

    def test_create_existing_maker(self):
        from bot.models import Maker
        from bot.lib.maker import create_maker
        create_maker(sender_id=self.sender_id)
        self.assertEqual(Maker.objects.filter(sender_id=self.sender_id).count(), 1)

    def test_create_new_maker(self):
        from bot.lib.maker import create_maker
        from bot.models import Maker
        new_sender_id = '2'
        create_maker(sender_id=new_sender_id)
        self.assertEqual(Maker.objects.filter(sender_id=new_sender_id).count(), 1)
