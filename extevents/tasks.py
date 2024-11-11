from elk.celery_app import app as celery_app
from extevents.models import GoogleCalendar


@celery_app.task
def update_google_calendars():
    for calendar in GoogleCalendar.objects.active():
        calendar.poll()
        calendar.update()
