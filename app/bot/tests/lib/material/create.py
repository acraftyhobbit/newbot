from django.test import TestCase


class CreateMaterialTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)
        self.material_url = 'http://craftybot.com/test_material_image.jpg'
        self.material_type = 'image'

    def test_create_new_material(self):
        from bot.lib.material import create_material
        from bot.models import Material, MaterialFile
        create_material(sender_id=self.sender_id, url=self.material_url, file_type=self.material_type)
        self.assertEqual(Material.objects.filter(maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(MaterialFile.objects.filter(material__maker__sender_id=self.sender_id).count(), 1)
