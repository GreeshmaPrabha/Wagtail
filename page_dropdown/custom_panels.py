from wagtail.admin.panels import FieldPanel
from django.utils.safestring import mark_safe

class DynamicDropdownPanel(FieldPanel):
    def __init__(self, field_name, *args, **kwargs):
        super().__init__(field_name, *args, **kwargs)

    def clone(self):
        return self.__class__(
            field_name=self.field_name,
            widget=self.widget if hasattr(self, 'widget') else None,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
        )

    class BoundPanel(FieldPanel.BoundPanel):
        def render_html(self, parent_context):
            html = super().render_html(parent_context)
            js = """
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const communitySelect = document.getElementById('id_community');
                    const projectSelect = document.getElementById('id_project');
                    const categorySelect = document.getElementById('id_category');
                    const subcategorySelect = document.getElementById('id_subcategory');

                    communitySelect.addEventListener('change', function() {
                        const communityId = this.value;
                        fetch(`/api/projects/?community=${communityId}`)
                            .then(response => response.json())
                            .then(data => {
                                projectSelect.innerHTML = '';
                                data.forEach(project => {
                                    const option = new Option(project.title, project.id);
                                    projectSelect.add(option);
                                });
                            });
                    });

                    categorySelect.addEventListener('change', function() {
                        const categoryId = this.value;
                        fetch(`/api/subcategories/?category=${categoryId}`)
                            .then(response => response.json())
                            .then(data => {
                                subcategorySelect.innerHTML = '';
                                data.forEach(subcategory => {
                                    const option = new Option(subcategory.name, subcategory.id);
                                    subcategorySelect.add(option);
                                });
                            });
                    });
                });
            </script>
            """
            return mark_safe(html + js)