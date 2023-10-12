from django.db import models
from django.conf import settings

IngredientPhaseChoices = [
    ('Kalteinsatz', 'Kalteinsatz'),
    ('Nachgesetzt_Oxidieren', 'Nachgesetzt während Oxidieren'),
    ('Nachgesetzt_Reduzieren_u_Gießen', 'Nachgesetzt während Reduzieren und Gießen'),
    ('other', 'Andere nicht aufgelistete'),
]

MeasurementChoices = [
    ('KRS_Fluss_sehr_fett', 'KRS-Fluss sehr fett'),
    ('KRS_Fluss_normal', 'KRS-Fluss normal'),
    ('TBRC_Fluss_normal', 'TBRC-Fluss normal'),
    ('TBRC_Fluss_CuNi', 'TBRC-Fluss CuNi'),
    ('WHO2_Fluss_Normal', 'WHO2-Fluss Normal'),
    ('WHO2_Fluss_CuNi', 'WHO2-Fluss CuNi'),
    ('other', 'Andere nicht aufgelistete'),
]

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='%(app_label)s_%(class)s_created_by', on_delete=models.SET_NULL)
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_modified_by', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

class Charge(BaseModel):
    number = models.IntegerField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'({self.number}) {self.start_time.date()}' if self.start_time else f"({self.number})"

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

    def __str__(self):
        return f'({self.number}) {self.name}'

class Ingredient(BaseModel):
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE)
    PHASE_CHOICES = IngredientPhaseChoices
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    tonnage = models.IntegerField()

    def __str__(self):
        return f'({self.charge}) {self.phase} {self.tonnage}kg {self.material}'

class Measurement(BaseModel):
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE)
    SOURCE_CHOICES = MeasurementChoices
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    timestamp = models.DateTimeField(null=True, blank=True)
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

    def __str__(self):
        return f'({self.charge}) {self.timestamp.strftime("%Y-%m-%d %H:%M")} {self.source}'