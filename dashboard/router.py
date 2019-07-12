class DashboardRouter(object):
    def db_for_read(self, model, **hints):
        "Point all operations on dashboard models to 'default'"
        if model._meta.app_label == 'dashboard':
            return 'default'
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all operations on dashboard models to 'default'"
        if model._meta.app_label == 'dashboard':
            return 'default'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in dashboard app"
        if obj1._meta.app_label == 'dashboard' and obj2._meta.app_label == 'dashboard':
            return True
        # Allow if neither is chinook app
        elif 'dashboard' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_syncdb(self, db, model):
        if db == 'default' or model._meta.app_label == "dashboard":
            return False  # we're not using syncdb on our legacy database
        else:  # but all other models/databases are fine
            return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'users_db'
        database.
        """
        if app_label == 'dashboard':
            return db == 'dashboard'
        return None