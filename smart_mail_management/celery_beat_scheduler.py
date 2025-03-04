# from django.conf import settings
from django.db import transaction, close_old_connections
from django.db.utils import DatabaseError, InterfaceError
from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.schedulers import DatabaseScheduler
from django.db import transaction, router
from celery.utils.log import get_logger
import logging

logger = get_logger(__name__)
debug, info, warning = logger.debug, logger.info, logger.warning


class DatabaseScheduler(DatabaseScheduler):

    def sync(self):
        
        if logger.isEnabledFor(logging.DEBUG):
            debug("Writing entries...")
        _tried = set()
        _failed = set()
        db = router.db_for_write(self.Model)
        try:
            close_old_connections()
            with transaction.atomic(using=db):
                while self._dirty:
                    try:
                        name = self._dirty.pop()
                        _tried.add(name)
                        self.schedule[name].save()
                    except (KeyError, ObjectDoesNotExist):
                        _failed.add(name)
        except DatabaseError as exc:
            logger.exception("Database error while sync: %r", exc)
        except InterfaceError:
            warning(
                "DatabaseScheduler: InterfaceError in sync(), "
                "waiting to retry in next call..."
            )
        finally:
            # retry later, only for the failed ones
            self._dirty |= _failed

    def schedule_changed(self):
        try:
            close_old_connections()
            db = router.db_for_write(self.Model)
            try:
                transaction.commit(using=db)
            except transaction.TransactionManagementError:
                pass  # not in transaction management.

            last, ts = self._last_timestamp, self.Changes.last_change()
        except DatabaseError as exc:
            logger.exception("Database gave error: %r", exc)
            return False

        except InterfaceError:
            warning(
                'DatabaseScheduler: InterfaceError in schedule_changed(), '
                'waiting to retry in next call...'
            )
            return False
        try:
            if ts and ts > (last if last else ts):
                return True
        finally:
            self._last_timestamp = ts
        return False
