import os

from django.core.wsgi import get_wsgi_application

from libraries import send_whatsapp_msg

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    application = get_wsgi_application()
    from api.models import Match

    try:
        matches = Match.objects.all()
        message = "QPL 2016 FIXTURE "
        send_whatsapp_msg(message=message)
        for match in matches:
            send_whatsapp_msg(message=str(match))

    except Exception as e:
        print e.message
