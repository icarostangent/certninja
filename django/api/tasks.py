from django_rq import job


@job('default', timeout=3600)
def send_registration_email():
    pass