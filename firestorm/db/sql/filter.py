class Filter:
    def as_sql(self):
        raise NotImplementedError()


class ExactFieldFilter(Filter):
    def __init__(self, field, value=None):
        self.field = field
        self.value = value
        if value is None:
            self.value = field.value

    def as_sql(self):
        return f"{self.field.name} = {self.field.to_sql_repr(self.value)}"
