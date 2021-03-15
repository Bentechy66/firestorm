from firestorm.db.sql.filter import ExactFieldFilter
from firestorm.session import current_session


class QuerySet:
    def __init__(self, model, filters=None):
        if filters is None:
            filters = []
        self.model = model
        self.filters = filters

    def filter(self, **kwargs):
        new_filters = []
        for kwarg in kwargs:
            new_filters.append(ExactFieldFilter(self.model.table.get_field(kwarg), value=kwargs[kwarg]))
        return QuerySet(self.model, filters=self.filters + new_filters)

    def _sql_to_model(self, data):
        model = self.model(**data)
        model.table.refresh_field_cache()
        return model

    def as_sql(self):
        sql = f"SELECT * FROM {self.model.name}"
        if self.filters:
            sql += " WHERE "
            sql += ' AND '.join([sql_filter.as_sql() for sql_filter in self.filters])
        sql += ";"
        return sql

    def all(self):
        return [self._sql_to_model(data) for data in current_session.retrieve_records(self.as_sql())]
