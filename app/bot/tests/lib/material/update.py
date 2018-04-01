from django.test import TestCase


class UpdateMaterialTestCase(TestCase):
    def setUp(self):
        from bot.lib.maker import create_maker
        from bot.lib.material import create_material
        self.sender_id = '1'
        create_maker(sender_id=self.sender_id)
        self.material_url = 'http://via.placeholder.com/350x150'
        self.material_type = 'image'
        self.tags = ['1', '2', '3']

        material = create_material(sender_id=self.sender_id, url=self.material_url, file_type=self.material_type)
        self.material_id = str(material.id)

    def test_update_nothing(self):
        from bot.lib.material import update_material
        from bot.models import Material, MaterialFile, MaterialTag
        update_material(sender_id=self.sender_id, material_id=self.material_id)
        self.assertEqual(Material.objects.filter(maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(MaterialFile.objects.filter(material__maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(MaterialTag.objects.filter(material__maker__sender_id=self.sender_id).count(), 0)

    def test_add_image(self):
        from bot.lib.material import update_material
        from bot.models import Material, MaterialFile
        update_material(
            sender_id=self.sender_id,
            material_id=self.material_id,
            file=dict(
                url='http://via.placeholder.com/350x350',
                file_type=self.material_type
            )
        )
        self.assertEqual(Material.objects.filter(maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(MaterialFile.objects.filter(material__maker__sender_id=self.sender_id).count(), 2)

    def test_add_tags(self):
        from bot.lib.material import update_material
        from bot.models import Material, MaterialTag
        update_material(
            sender_id=self.sender_id,
            material_id=self.material_id,
            tags=self.tags
        )
        self.assertEqual(Material.objects.filter(maker__sender_id=self.sender_id).count(), 1)
        self.assertEqual(MaterialTag.objects.filter(material__maker__sender_id=self.sender_id).count(), 3)
