from celery import shared_task


@shared_task()
def download_file(url):
    # TODO Resize images to thumbnail versions
    import requests
    from bot.models import File
    from common.file_management import store_file
    from common.utilities import generate_unique_key
    response = requests.get(url=url)
    file_id = generate_unique_key(url)
    store_file(key='{0}.jpg'.format(str(file_id).replace('-', '/')), obj=response.content)
    file = File.objects.filter(id=file_id).update(downloaded=True)
    return str(file.id)
