from django.urls import path
from .views import (
    material_list, add_material, update_material, delete_material, 
    measurement_list, add_measurement, update_measurement, delete_measurement,
    ingredient_list, add_ingredient, update_ingredient, delete_ingredient,
    charge_list, add_charge, update_charge, delete_charge, recent_charges,
)

urlpatterns = [
    # Home
    path('', material_list, name='material_handler_home'),
    # Charge
    path('charge/', charge_list, name='charge_list'),
    path('charge/<int:page_to_display>/', charge_list, name='charge_list_page'),
    path('charge/add/', add_charge, name='add_charge'),
    path('charge/update/<int:charge_id>/', update_charge, name='update_charge'),
    path('charge/delete/<int:charge_id>/', delete_charge, name='delete_charge'),
    path('charge/recent/', recent_charges, name='recent_charges'),
    # Material
    path('material/', material_list, name='material_list'),
    path('material/add/', add_material, name='add_material'),
    path('material/update/<int:material_id>/', update_material, name='update_material'),
    path('material/delete/<int:material_id>/', delete_material, name='delete_material'),
    # Measurement
    path('measurement/', measurement_list, name='measurement_list'),
    path('measurement/add/', add_measurement, name='add_measurement'),
    path('measurement/update/<int:measurement_id>/', update_measurement, name='update_measurement'),
    path('measurement/delete/<int:measurement_id>/', delete_measurement, name='delete_measurement'),
    # Ingredient
    path('ingredient/', ingredient_list, name='ingredient_list'),
    path('ingredient/add/', add_ingredient, name='add_ingredient'),
    path('ingredient/update/<int:ingredient_id>/', update_ingredient, name='update_ingredient'),
    path('ingredient/delete/<int:ingredient_id>/', delete_ingredient, name='delete_ingredient'),
]
