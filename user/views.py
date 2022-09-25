from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from job.models import Job

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            Firstname = form.cleaned_data.get('firstname')
            messages.success(request, f'Account created for {Firstname}!')
            return redirect('login')
    form = UserRegistrationForm
    return render(request, 'user/register.html', {'form': form})

def dashboard(request):
    return render(request, 'user/dashboardprofile.html')


def dashboard_favourites(request):
    return render(request, 'user/favourites.html')

def reviews(request):
    return render(request, 'user/reviews.html')

def dashboard_task(request):
    user = request.user
    job = Job.objects.filter(author=user)
    context={
        "tasks":job,
    }
    return render(request, 'user/task_list.html', context)


@login_required
def profile(request):
    return render(request, 'user/profile.html')


@login_required
def profileUpdate(request):
    if request.method == 'POST':
        u_form = UserRegistrationForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserRegistrationForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'user/profile_update.html', context)
