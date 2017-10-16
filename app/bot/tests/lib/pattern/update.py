from django.test import TestCase


class UpdatePatternTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.pattern import create_pattern
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)
        self.pattern_url = 'http://craftybot.com/test_pattern_image.jpg'
        self.pattern_type = 'image'
        self.tags = ['1', '2', '3']

        pattern = create_pattern(sender_id=self.sender_id, url=self.pattern_url, file_type=self.pattern_type)
        self.pattern_id = str(pattern.id)

    def test_update_nothing(self):
        from bot.lib.pattern import update_pattern
        from bot.models import Pattern, PatternFile, PatternTag
        update_pattern(sender_id=self.sender_id, pattern_id=self.pattern_id)
        self.assertEqual(Pattern.objects.filter(maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(PatternFile.objects.filter(pattern__maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(PatternTag.objects.filter(pattern__maker__sender_id=self.sender_id).count(), 0)

    def test_add_image(self):
        from bot.lib.pattern import update_pattern
        from bot.models import Pattern, PatternFile
        update_pattern(
            sender_id=self.sender_id,
            pattern_id=self.pattern_id,
            file=dict(
                url='http://craftybot.com/test_pattern_image_2.jpg',
                file_type=self.pattern_type
            )
        )
        self.assertEqual(Pattern.objects.filter(maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(PatternFile.objects.filter(pattern__maker__sender_id=self.sender_id).count(), 2)

    def test_add_tags(self):
        from bot.lib.pattern import update_pattern
        from bot.models import Pattern, PatternTag
        update_pattern(
            sender_id=self.sender_id,
            pattern_id=self.pattern_id,
            tags=self.tags
        )
        self.assertEqual(Pattern.objects.filter(maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(PatternTag.objects.filter(pattern__maker__sender_id=self.sender_id).count(), 3)
