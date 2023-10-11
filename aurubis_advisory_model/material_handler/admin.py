from django.contrib import admin
from .models import Material, Charge, Ingredient, Measurement

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    pass

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    pass
