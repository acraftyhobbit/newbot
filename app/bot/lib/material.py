def create_material(sender_id, url, file_type):
    from django.utils.timezone import now
    from bot.models import Material, MaterialFile
    from common.utilities import generate_unique_key
    from .maker import get_maker_id
    from bot.lib.utilities import create_file

    maker_id = get_maker_id(sender_id=sender_id)

    file = create_file(url=url, file_type=file_type)
    material_id = generate_unique_key(maker_id, now())
    material_file_id = generate_unique_key(material_id, file.id)

    material = Material(id=material_id, maker_id=maker_id)
    material.save()

    material_file = MaterialFile(id=material_file_id, file=file, material=material)
    material_file.save()

    return material


def update_material(sender_id: str, material_id: str, file: dict = None, tags: list = None):
    from bot.models import Material
    from .utilities import add_tags, add_file
    from common.utilities import generate_unique_key

    maker_id = generate_unique_key(sender_id)
    material = Material.objects.get(id=material_id, maker_id=maker_id)

    if file:
        add_file(obj=material, url=file['url'], file_type=file['file_type'])

    if tags:
        add_tags(obj=material, tags=tags)
    return material
