class Filter:
    def as_sql(self):
        raise NotImplementedError()


class ExactFieldFilter(Filter):
    def __init__(self, field):
        self.field = field

    def as_sql(self):
        return f"{self.field.name} = {self.field.value_as_sql_repr()}"
