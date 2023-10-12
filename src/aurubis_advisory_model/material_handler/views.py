from .models import Charge, Ingredient, Measurement, Material
from .forms import ChargeForm, NewChargeForm, IngredientForm, MeasurementForm, MaterialForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum

display_count = 8

# Charge views
def charge_list(request, page_to_display:int=1):

    # Calculate pagination elements to display
    from_element = (page_to_display - 1) * max(display_count,1)
    to_element = page_to_display * display_count

    # Annotate charges with the total tonnage of their ingredients
    charges = Charge.objects.annotate(
        total_tonnage=Sum('ingredient__tonnage')
    ).order_by('-start_time')[from_element:to_element]

    context = {
        'current_page': page_to_display,
        'next_page': page_to_display + 1,
        'previous_page': max(page_to_display - 1, 1),
        'charges': charges
    }
    return render(request, 'charge_list.html', context)

def add_charge(request):
    if request.method == 'POST':
        form = ChargeForm(request.POST)
        if form.is_valid():
            charge = form.save(commit=False)
            charge.created_by = request.user
            charge.modified_by = request.user
            charge.save()
            return redirect('charge_list')
    else:
        # Try to get the latest charge
        latest_charge = Charge.objects.order_by('-start_time').first()
        
        # If we find a charge, get its number, increment it by one and set it as initial value
        if latest_charge:
            initial_number = latest_charge.number + 1
        else:
            # You can set a default value if there's no charge in the database yet.
            # Here, I'm assuming it's 1, but adjust as needed.
            initial_number = 1

        initial_form_data = {
            'start_time': timezone.now(),#.strftime(TIMESTAMP_FORMAT),
            'number': initial_number,
        }
        form = NewChargeForm(initial=initial_form_data)

    return render(request, 'charge_form.html', {'form': form})

def update_charge(request, charge_id):
    charge = get_object_or_404(Charge, id=charge_id)
    if request.method == 'POST':
        form = ChargeForm(request.POST, instance=charge)
        if form.is_valid():
            charge = form.save(commit=False)
            charge.modified_by = request.user
            charge.save()
            return redirect('charge_list')
    else:
        form = ChargeForm(instance=charge)
    return render(request, 'charge_form.html', {'form': form})

def delete_charge(request, charge_id):
    charge = get_object_or_404(Charge, id=charge_id)
    if request.method == 'POST':
        charge.delete()
        return redirect('charge_list')

    context = {
        'object': charge,
        'title': 'Delete Charge',
        'redirect_url': 'charge_list',
    }
    return render(request, 'delete_confirm.html', context)

def recent_charges(request):
    charges = Charge.objects.all().order_by('-start_time')[:5]  # Getting the 5 most recent charges
    context = {
        'charges': charges
    }
    return render(request, 'recent_charges.html', context)

# Material views
def material_list(request):
    materials = Material.objects.all()
    context = {
        'materials': materials,
        'title': 'Material List'
    }
    return render(request, 'material_list.html', context)

def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.created_by = request.user  # Set the current user as creator
            if material.pk:  # If the object already exists in the database
                material.modified_by = request.user  # Set the current user as the last person who modified
            material.save()
            return redirect('material_list')
    else:
        form = MaterialForm()

    context = {
        'form': form,
        'title': 'Add Material',
        'button_label': 'Add'
    }
    return render(request, 'form_template.html', context)

def update_material(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            updated_material = form.save(commit=False)
            updated_material.modified_by = request.user  # Set the current user as the last person who modified
            updated_material.save()
            return redirect('material_list')
    else:
        form = MaterialForm(instance=material)

    context = {
        'form': form,
        'title': 'Update Material',
        'button_label': 'Update'
    }
    return render(request, 'form_template.html', context)

def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        material.delete()
        return redirect('material_list')

    context = {
        'object': material,
        'title': 'Delete Material',
        'redirect_url': 'material_list',
    }
    return render(request, 'delete_confirm.html', context)

# Measurement Views
def measurement_list(request):
    charge_filter = request.GET.get('charge_filter', '')

    # Filter measurements by charge if specified
    if charge_filter:
        measurements = Measurement.objects.all().filter(charge__number=charge_filter)
    else:
        measurements = Measurement.objects.all()

    # Handle form submission for new measurement creation
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            new_measurement = form.save(commit=False)
            new_measurement.created_by = request.user
            new_measurement.save()
            return redirect('update_measurement', measurement_id=new_measurement.id)
    else:
        initial_form_data = {
            'timestamp': timezone.now(),#.strftime(TIMESTAMP_FORMAT),
            'charge': charge_filter
        }
        form = MeasurementForm(initial=initial_form_data)

    context = {
        'measurements': measurements,
        'form': form,
        'charges': Charge.objects.all().order_by('-start_time'),  # For the dropdown
        'charge_filter': charge_filter,
        'title': 'Measurement List'
    }
    return render(request, 'measurement_list.html', context)

def add_measurement(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.created_by = request.user
            measurement.save()
            return redirect('measurement_list')
    else:
        initial_form_data = {
            'timestamp': timezone.now(),#.strftime(TIMESTAMP_FORMAT)
        }
        form = MeasurementForm(initial=initial_form_data)

    context = {
        'form': form,
        'title': 'Add Measurement',
        'button_label': 'Add'
    }
    return render(request, 'form_template.html', context)

def update_measurement(request, measurement_id):
    measurement = get_object_or_404(Measurement, pk=measurement_id)
    
    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            updated_measurement = form.save(commit=False)
            updated_measurement.modified_by = request.user
            updated_measurement.save()
            return redirect('measurement_list')
    else:
        form = MeasurementForm(instance=measurement)

    context = {
        'form': form,
        'title': 'Update Measurement',
        'button_label': 'Update'
    }
    return render(request, 'form_template.html', context)

def delete_measurement(request, measurement_id):
    measurement = get_object_or_404(Measurement, pk=measurement_id)
    
    if request.method == 'POST':
        measurement.delete()
        return redirect('measurement_list')

    context = {
        'object': measurement,
        'title': 'Delete Measurement',
        'redirect_url': 'measurement_list',
    }
    return render(request, 'delete_confirm.html', context)

# Ingeredient views
def ingredient_list(request):
    charge_filter = request.GET.get('charge_filter', '')

    # Filter ingredients by ingredient if specified
    if charge_filter:
        ingredients = Ingredient.objects.all().filter(charge__number=charge_filter)
    else:
        ingredients = Ingredient.objects.all()

    # Handle form submission for new ingredient creation
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            new_ingredient = form.save(commit=False)
            new_ingredient.created_by = request.user
            new_ingredient.save()
            # Return the response and preserve the charge_filter parameter
            response = redirect('ingredient_list')
            response['Location'] += f'?charge_filter={charge_filter}'
            return response
    else:
        initial_form_data = {
            'charge': charge_filter,
        }
        form = IngredientForm(initial=initial_form_data)

    context = {
        'ingredients': ingredients,
        'form': form,
        'charges': Charge.objects.all().order_by('-start_time'),  # For the dropdown,
        'charge_filter': charge_filter,
        'title': 'Ingredient List',
    }
    return render(request, 'ingredient_list.html', context)


def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.created_by = request.user
            ingredient.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm()

    context = {
        'form': form,
        'title': 'Add Ingredient',
        'button_label': 'Add'
    }
    return render(request, 'form_template.html', context)

def update_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            updated_ingredient = form.save(commit=False)
            updated_ingredient.modified_by = request.user
            updated_ingredient.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm(instance=ingredient)

    context = {
        'form': form,
        'title': 'Update Ingredient',
        'button_label': 'Update',
        'return_view': 'ingredient_list',
    }
    return render(request, 'form_template.html', context)

def delete_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient_list')

    context = {
        'object': ingredient,
        'title': 'Delete Ingredient',
        'redirect_url': 'ingredient_list',
    }
    return render(request, 'delete_confirm.html', context)
