from django import forms
from .models import Material

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        
        # Exclude fields for every form that inherits from BaseForm
        exclude_fields = ['created_by', 'date_created', 'date_modified', 'modified_by']
        for field in exclude_fields:
            if field in self.fields:
                del self.fields[field]

class MaterialForm(BaseForm):
    class Meta:
        model = Material
        fields = '__all__'  # This would include all fields, but the BaseForm will exclude the specified ones
