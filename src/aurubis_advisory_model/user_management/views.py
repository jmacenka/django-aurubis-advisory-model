from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

# Import and instanciate the dash-app
from dashboard import create_dash_app
app = create_dash_app()

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set is_active to False during registration
            user.save()
            messages.info(request, 'Thank you for registering! Please wait for your account to be approved by an administrator.')
            return redirect('login')
            #login(request, user)  # Log the user in.
            #messages.success(request, 'Registration successful. Please log in.')
            return redirect('home')
        else:
            print(form.errors)  # This will print errors to the console.
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Check if 'next' parameter is in the request
                    next_url = request.GET.get('next')
                    if next_url:  # if 'next' parameter exists, redirect to its value
                        return redirect(next_url)
                    else:
                        return redirect('home')  # if not, redirect to home
                else:
                    messages.error(request, 'Your registration is still pending. Please wait for administrator approval.')
                    return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect('home')

@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    if request.method == 'POST':
        user_id_to_activate = request.POST.get('activate_user')
        user_id_to_deactivate = request.POST.get('deactivate_user')
        user_id_to_promote = request.POST.get('promote_user')
        user_id_to_demote = request.POST.get('demote_user')
        user_id_to_delete = request.POST.get('delete_user')
        
        if user_id_to_activate:
            User.objects.filter(pk=user_id_to_activate).update(is_active=True)
            messages.success(request, 'Activated user.')

        elif user_id_to_deactivate:
            user_to_deactivate = User.objects.get(pk=user_id_to_deactivate)
            if user_to_deactivate == request.user:
                messages.warning(request, 'You cannot deactivate yourself.')
            elif user_to_deactivate.is_superuser:
                messages.warning(request, 'Superusers cannot be deactivated.')
            else:
                user_to_deactivate.is_active = False
                user_to_deactivate.save()
                messages.success(request, 'Deactivated user.')

        elif user_id_to_promote:
            User.objects.filter(pk=user_id_to_promote).update(is_staff=True)
            messages.success(request, 'Granted admin rights to user.')

        elif user_id_to_demote:
            User.objects.filter(pk=user_id_to_demote).update(is_staff=False)
            messages.success(request, 'Removed admin rights from user.')

        elif user_id_to_delete:
            User.objects.filter(pk=user_id_to_delete).delete()
            messages.success(request, 'Deleted user.')

        return redirect('manage_users')

    pending_users = User.objects.filter(is_active=False)
    
    # Exclude the current logged-in admin from the list
    active_users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    
    context = {
        'pending_users': pending_users,
        'active_users': active_users,
    }
    
    return render(request, 'manage_users.html', context)