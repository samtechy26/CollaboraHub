from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Category, Bid, Skill
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import BidForm



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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

@login_required
def JobDetail(request, pk):
    task = Job.objects.get(pk=pk)
    bid = Bid.objects.filter(job=task)
    b_form = BidForm()
    if request.method == 'POST':
        user = request.user
        data = request.POST
        action = data.get('bookmark')
        if action == 'bookmark':
            task.favourite.add(user)
            task.save()
            return redirect('job-detail', pk)
        elif action == 'bookmarked':
            task.favourite.remove(user)
            task.save()
            return redirect('job-detail', pk)
        b_form = BidForm(request.POST)
        if b_form.is_valid():
            b_form.instance.job = task
            b_form.instance.user = request.user
            b_form.save()
            return redirect('job-detail', pk)
        else:
            b_form = BidForm()
            
    
    context = {
        'task':task,
        'bids':bid,
        'b_form':b_form
    }
    return render(request,'job/job_detail.html', context)


class UserListView(ListView):
    model = User
    template_name = 'job/freelancers.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['skills'] = Skill.objects.all()
        return context

def dashboard_favourites(request):
    task = Job.objects.all()
    users = User.objects.all()
    context = {
        'tasks':task,
        'users':users
    }
    return render(request, 'job/favourites.html', context)
 
def contact(request):
    return render(request, 'job/contact.html')


class CategoryView(ListView):
    def get(self, request, slug):
        category = Category.objects.all()
        tasks = Job.objects.filter(job_category__slug = slug)

        context = {
            'categories': category,
            'tasks':tasks,
         }
        return render(request, 'job/category.html', context)


