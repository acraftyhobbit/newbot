def generate_date_stamped_filename(filename=str(), folder=str()):
    from django.utils.timezone import now
    from common.utilities import create_unique_hash
    import uuid
    date = now().strftime("%Y/%m/%d")
    if filename:
        filename = '/' + filename
    if folder:
        folder += '/'
    return str(
        create_unique_hash(
            dict(
                date=date
            )
        )
    ) + '/' + folder + '{0}/{1}'.format(
        date,
        str(
            uuid.uuid4()
        )
    ) + filename
