class ProtectedFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.should_show_protected_fields():
            self.make_protected_fields_write_only()

    def should_show_protected_fields(
        self,
    ):
        return False

    def make_protected_fields_write_only(
        self,
    ):
        if not hasattr(
            self.Meta,
            "protected_fields",
        ):
            return
        for field_name in self.Meta.protected_fields:
            self.fields[field_name].write_only = True
