from django.db import models
from django.conf import settings

IngredientPhaseChoices = [
    ('Kalteinsatz', 'Kalteinsatz'),
    ('Nachgesetzt_Oxidieren', 'Nachgesetzt_Oxidieren'),
    ('Nachgesetzt_Reduzieren_u_Gießen', 'Nachgesetzt_Reduzieren_u_Gießen'),
]

MeasurementChoices = [
    ('Source1', 'Source1'),
    ('Source2', 'Source2'),
]

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_created_by', on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_modified_by', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Charge(BaseModel):
    number = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Material(BaseModel):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    Cu = models.DecimalField(max_digits=5, decimal_places=2)
    Sn = models.DecimalField(max_digits=5, decimal_places=2)
    Pb = models.DecimalField(max_digits=5, decimal_places=2)
    Ni = models.DecimalField(max_digits=5, decimal_places=2)
    Sb = models.DecimalField(max_digits=5, decimal_places=2)
    As = models.DecimalField(max_digits=5, decimal_places=2)
    S = models.DecimalField(max_digits=5, decimal_places=2)
    Bi = models.DecimalField(max_digits=5, decimal_places=2)
    Zn = models.DecimalField(max_digits=5, decimal_places=2)
    Fe = models.DecimalField(max_digits=5, decimal_places=2)

class Ingredient(BaseModel):
    PHASE_CHOICES = IngredientPhaseChoices
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    tonnage = models.DecimalField(max_digits=8, decimal_places=2)
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES)
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE)

class Measurement(BaseModel):
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE)
    SOURCE_CHOICES = MeasurementChoices
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    timestamp = models.DateTimeField()
    Cu = models.DecimalField(max_digits=5, decimal_places=2)
    Sn = models.DecimalField(max_digits=5, decimal_places=2)
    Pb = models.DecimalField(max_digits=5, decimal_places=2)
    Ni = models.DecimalField(max_digits=5, decimal_places=2)
    Sb = models.DecimalField(max_digits=5, decimal_places=2)
    As = models.DecimalField(max_digits=5, decimal_places=2)
    S = models.DecimalField(max_digits=5, decimal_places=2)
    Bi = models.DecimalField(max_digits=5, decimal_places=2)
    Zn = models.DecimalField(max_digits=5, decimal_places=2)
    Fe = models.DecimalField(max_digits=5, decimal_places=2)
