from distutils.log import error
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
def profile(request, id):
    users = User.objects.get(id=id)
    if request.method == 'POST':
        current_user = request.user
        data = request.POST
        action = data.get('bookmark')
        if action == 'bookmark':
            current_user.profile.favourite.add(users)
        elif action == 'bookmarked':
            current_user.profile.favourite.remove(users)
        current_user.save()
        return redirect('profile', id)
    context={
        'users':users
    }
    return render(request, 'user/profile.html', context)


@login_required
def profileUpdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'user/profile_update.html', context)
