from celery import shared_task


@shared_task()
def download_file(url):
    import requests
    from bot.models import File
    from common.file_management import store_file
    from common.utilities import generate_unique_key
    response = requests.get(url=url)
    file_id = generate_unique_key(url)
    store_file(key='user/{0}.jpg'.format(str(file_id).replace('-', '/')), obj=response.content)
    file = File.objects.filter(id=file_id).update(downloaded=True)
    return str(file.id)


@shared_task()
def get_maker_profile(sender_id):
    from app.settings import FACEBOOK_TOKEN
    from bot.models import MakerProfile
    from bot.lib.utilities import create_file
    from bot.lib.maker import get_maker_id
    import requests
    import json
    r = requests.get(
        "https://graph.facebook.com/v2.6/{0}".format(sender_id),
        params=dict(
            fields=['first_name', 'last_name', 'profile_pic'],
            access_token=FACEBOOK_TOKEN
        )
    )
    profile_data = json.loads(r.content)
    profile_picture = None
    if profile_data.get('profile_pic'):
        profile_picture = create_file(url=profile_data['profile_pic'], file_type='image')
    maker_profile, new = MakerProfile.objects.update_or_create(
        maker_id=get_maker_id(sender_id=sender_id),
        defaults=dict(
            first_name=profile_data.get('first_name'),
            last_name=profile_data.get('last_name'),
            timezone=profile_data.get('timezone'),
            gender=profile_data.get('gender'),
            locale=profile_data.get('locale'),
            profile_picture=profile_picture
        )
    )
    return sender_id
