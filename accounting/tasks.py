from accounting.models import Event as AccEvent
from elk.celery_app import app as celery_app
from elk.logging import logger
from timeline.models import Entry as TimelineEntry


@celery_app.task
def bill_timeline_entries():
    for entry in TimelineEntry.objects.to_be_marked_as_finished().filter(taken_slots__gte=1):
        entry.is_finished = True
        entry.save()

        if not AccEvent.objects.by_originator(entry).count():
            ev = AccEvent(
                teacher=entry.teacher,
                originator=entry,
                event_type='class',
            )
            ev.save()
        else:
            logger.warning('Tried to bill already billed timeline entry')
