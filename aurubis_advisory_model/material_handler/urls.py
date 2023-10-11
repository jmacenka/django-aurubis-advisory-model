from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_material, name='material_handler_home'),
    path('material_list/', views.material_list, name='material_list'),
    path('add_material/', views.add_material, name='add_material'),
]
