class Modifier:
    applies_to = []

    def as_sql(self):
        raise NotImplementedError()


class NotNullModifier(Modifier):
    applies_to = ["CREATE"]

    def as_sql(self):
        return "NOT NULL"


class PrimaryKeyModifier(Modifier):
    applies_to = ["CREATE"]

    def as_sql(self):
        return "PRIMARY KEY"


class AutoIncrementModifier(Modifier):
    applies_to = ["CREATE"]

    def as_sql(self):
        return "AUTOINCREMENT"
