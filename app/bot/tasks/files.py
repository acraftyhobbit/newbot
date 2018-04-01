from celery import shared_task


@shared_task()
def download_file(url):
    # TODO Resize images to thumbnail versions
    import requests
    from bot.models import File
    from common.utilities import generate_unique_key, store_obj_on_s3
    response = requests.get(url=url)
    file_id = generate_unique_key(url)
    store_obj_on_s3(key='static/user/{0}'.format(str(file_id).replace('-', '/')), obj=response.content)
    File.objects.filter(id=file_id).update(downloaded=True)
    return str(file_id)
