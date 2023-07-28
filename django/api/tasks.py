from django_rq import job


@job('default', timeout=3600)
def send_activation_email(msg):
    print('did you get the email yet?')
    msg.send()
