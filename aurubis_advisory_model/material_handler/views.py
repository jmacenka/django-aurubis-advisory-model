from django.shortcuts import render, redirect
from .forms import MaterialForm

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

