def create_file(url, file_type):
    from bot.models import File
    from bot.tasks import download_file
    from common.utilities import generate_unique_key

    file_id = generate_unique_key(url)
    file_type_id = generate_unique_key(file_type)

    file, new = File.objects.get_or_create(id=file_id, defaults=dict(type_id=file_type_id, url=url))
    if new and file_type == 'image':
        download_file.delay(url=url)

    return file


def create_tag(tag):
    from bot.models import Tag
    from common.utilities import generate_unique_key

    tag_id = generate_unique_key(tag)
    tag, new = Tag.objects.get_or_create(id=tag_id, defaults=dict(name=tag))

    return tag


def load_relationship_model(obj_1, obj_2):
    import string
    from importlib import import_module
    class_template = None

    class_name = string.capwords(
        "{0} {1}".format(obj_1._meta.verbose_name, obj_2._meta.verbose_name).replace('_', ' ')).replace(' ', '')
    module_name = 'bot.models'

    try:
        module = import_module(module_name)
        class_template = getattr(module, class_name)
    except AttributeError:
        print(obj_1._meta.model_name)
        print(obj_2._meta.model_name)
        print(class_name)
    return class_template


def get_file_url(file):
    from common.file_management import get_bucket

    if file.downloaded:
        key = 'user/{0}.jpg'.format(str(file.id).replace('-', '/'))
        bucket, key = get_bucket(key=key)
        return 'https://s3.amazonaws.com/{0}/{1}'.format(bucket, key)
    else:
        return file.url


def add_file(obj, url, file_type):
    from common.utilities import generate_unique_key
    file = create_file(url=url, file_type=file_type)
    obj_file_id = generate_unique_key(obj.id, file.id)

    obj_file_model = load_relationship_model(obj_1=obj, obj_2=file)
    obj_file_model.objects.get_or_create(id=obj_file_id,
                                         defaults={'file': file, obj._meta.verbose_name.replace(' ', '_'): obj})

    return file


def add_tags(obj, tags: list):
    from common.utilities import generate_unique_key
    tag_objects = list()
    for tag in [i for i in tags if isinstance(i, str) and i.strip()]:
        tag = tag.strip()
        tag_object = create_tag(tag=tag)
        tag_objects.append(tag_object)

        obj_tag_id = generate_unique_key(obj.id, tag_object.id)

        obj_tag_model = load_relationship_model(obj_1=obj, obj_2=tag_object)
        obj_tag_model.objects.get_or_create(id=obj_tag_id,
                                            defaults={'tag': tag_object, obj._meta.verbose_name.replace(' ', '_'): obj})
    return tag_objects
