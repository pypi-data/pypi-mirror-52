import json
from datetime import date
from datetime import datetime

from dateutil import parser
from peewee import Model, Proxy, CharField, DateTimeField, TextField


class SyncManager(Model):
    app = CharField(max_length=256, primary_key=True)
    meta = TextField(default="{}")
    modified = DateTimeField(null=True)

    is_test_run = False

    @classmethod
    def init_db(cls, db):
        if not isinstance(cls.get_db(), Proxy):
            if db == cls.get_db():
                return
            raise Exception("Cannot re init_db with different db object")

        cls.get_db().initialize(db)

    @classmethod
    def set_async(cls):
        cls._meta.database.set_allow_sync(False)

    @classmethod
    def get_async_manager(cls):
        from peewee_async import Manager
        return Manager(cls._meta.database)

    @classmethod
    def get_db(cls):
        return cls._meta.database

    def get_meta(self):
        return json.loads(self.meta)

    def set_meta(self, meta):
        self.meta = json.dumps(meta)

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        return super(SyncManager, self).save(*args, **kwargs)

    def get_last_offset(self):

        meta = self.get_meta()
        value = meta.pop('value', None)
        value_type = meta.pop('type', None)
        offset = meta.pop('offset', None)

        if value_type == 'date':
            value = parser.parse(value)

        return {'value': value, 'offset': offset}

    def set_last_offset(self, value, offset=0):

        value_type = None

        if isinstance(value, datetime) or isinstance(value, date):
            value = value.isoformat()
            value_type = "date"

        self.set_meta({'value': value, "type": value_type, 'offset': offset})

    class Meta:
        table_name = "sync_manager"
        database = Proxy()

