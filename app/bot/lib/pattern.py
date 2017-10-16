def create_pattern(sender_id, url, file_type):
    from django.utils.timezone import now
    from bot.models import Pattern, PatternFile
    from common.utilities import generate_unique_key
    from .maker import get_maker_id
    from bot.lib.utilities import create_file

    maker_id = get_maker_id(sender_id=sender_id)

    file = create_file(url=url, file_type=file_type)
    pattern_id = generate_unique_key(maker_id, now())
    pattern_file_id = generate_unique_key(pattern_id, file.id)

    pattern = Pattern(id=pattern_id, maker_id=maker_id)
    pattern.save()

    pattern_file = PatternFile(id=pattern_file_id, file=file, pattern=pattern)
    pattern_file.save()

    return pattern


def update_pattern(sender_id: str, pattern_id: str, file: dict = None, tags: list = None):
    from bot.models import Pattern
    from .utilities import add_tags, add_file
    from common.utilities import generate_unique_key

    maker_id = generate_unique_key(sender_id)
    pattern = Pattern.objects.get(id=pattern_id, maker_id=maker_id)

    if file:
        add_file(obj=pattern, url=file['url'], file_type=file['file_type'])

    if tags:
        add_tags(obj=pattern, tags=tags)
    return pattern
