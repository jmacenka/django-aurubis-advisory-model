from django import forms
from .models import Material, Charge, Ingredient, Measurement

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
        fields = '__all__'

class ChargeForm(BaseForm):
    class Meta:
        model = Charge
        fields = '__all__'

class NewChargeForm(BaseForm):
    class Meta:
        model = Charge
        fields = ['number', 'start_time']

class IngredientForm(BaseForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

class MeasurementForm(BaseForm):
    class Meta:
        model = Measurement
        fields = '__all__'

    timestamp = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'datetimepicker'}),
        required=True
    )