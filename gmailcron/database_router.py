class CeleryDatabaseRouter:
    """
    A router to control all database operations on models in the
    django_celery_beat and django_celery_results applications.
    """

    route_app_labels = {"django_celery_beat", "django_celery_results"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read django_celery_beat and django_celery_results models go to celery.
        """
        if model._meta.app_label in self.route_app_labels:
            return "celery"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write django_celery_beat and django_celery_results models go to celery.
        """
        if model._meta.app_label in self.route_app_labels:
            return "celery"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the django_celery_beat or django_celery_results apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the django_celery_results and django_celery_beat apps only appear in the
        'celery' database.
        """
        if app_label in self.route_app_labels:
            return db == "celery"
        return None

