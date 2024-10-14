from wagtail.admin.panels import FieldPanel

class CustomDynamicDropdownPanel(FieldPanel):
    def __init__(self, field_name, dynamic_choices, *args, **kwargs):
        self.dynamic_choices = dynamic_choices
        super().__init__(field_name, *args, **kwargs)

    def on_instance_bound(self):
        # Call the dynamic choices method on the instance
        if callable(self.dynamic_choices):
            self.bound_field.field.choices = self.dynamic_choices(self.instance)