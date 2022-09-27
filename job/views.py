from django.shortcuts import render, redirect
from .models import Job, Category, Bid
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView



def home(request):
    context = {
        'categories':Category.objects.all()
    }
    return render(request,'job/home.html', context)


class JobCreateView(CreateView):
    model = Job
    fields = [ 'title', 'job_type', 'job_category', 'cost',  'skill', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class JobListView(ListView):
    model = Job
    context_object_name = 'tasks'

def JobDetail(request, pk):
    task = Job.objects.get(pk=pk)
    bid = Bid.objects.filter(job=task)
    context = {
        'task':task,
        'bids':bid
    }
    return render(request,'job/job_detail.html', context)


class UserListView(ListView):
    model = User
    template_name = 'job/freelancers.html'
    context_object_name = 'users'