from django.test import TestCase


class CreatePatternTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)
        self.pattern_url = 'http://via.placeholder.com/350x150'
        self.pattern_type = 'image'

    def test_create_new_pattern(self):
        from bot.lib.pattern import create_pattern
        from bot.models import Pattern, PatternFile
        create_pattern(sender_id=self.sender_id, url=self.pattern_url, file_type=self.pattern_type)
        self.assertEqual(Pattern.objects.filter(maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(PatternFile.objects.filter(pattern__maker__sender_id=self.sender_id).count(), 1)
