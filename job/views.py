from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Category, Bid, Skill
from user.models import Testimonial
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, FormView, DeleteView
from django.views import generic
from .forms import BidForm, ContactForm, JobCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from notifications.signals import notify



class HomeView(ListView):
    model = Job
    template_name = 'pages/home.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            "recent_tasks": Job.objects.all().order_by('-date_created')[:4],
            "testimonials": Testimonial.objects.all()
        })
        return context

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobCreationForm
    template_name = 'job/job_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class JobUpdateView(UserPassesTestMixin,JobCreateView,UpdateView):
    success_url = reverse_lazy('dashboard-task')

    def test_func(self):
        job = self.get_object()
        if self.request.user == job.author:
            return True
        return False


class JobListView(ListView):
    model = Job
    template_name = 'job/job_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = Job.objects.all().order_by('-date_created')
        category = self.request.GET.get('category', None)
        if category:
            qs = qs.filter(job_category__slug=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context.update({
            "categories": Category.objects.all,
            
        })
        return context

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Job
    success_url = reverse_lazy('dashboard-task')

    def test_func(self):
        job = self.get_object()
        if self.request.user == job.author:
            return True
        return False

@login_required
def JobDetail(request, pk):
    task = Job.objects.get(pk=pk)
    bid = Bid.objects.filter(job=task)
    user_bid = Bid.objects.filter(user=request.user)
    b_form = BidForm()
    if request.method == 'POST':
        user = request.user
        data = request.POST
        action = data.get('bookmark')
        if action == 'bookmark':
            task.favourite.add(user)
            task.save()
            return redirect('job:job-detail', pk)
        elif action == 'bookmarked':
            task.favourite.remove(user)
            task.save()
            return redirect('job:job-detail', pk)
        b_form = BidForm(request.POST)
        if b_form.is_valid():
            b_form.instance.job = task
            b_form.instance.user = request.user
            b_form.save()
            notify.send(sender=request.user, recipient=task.author, verb="application for bid", description=task.title)
            return redirect('job:job-detail', pk)
        else:
            b_form = BidForm()
            
    
    context = {
        'task':task,
        'bids':bid,
        'b_form':b_form,
        'user_bid':user_bid
    }
    return render(request,'job/job_detail.html', context)


class UserListView(ListView):
    model = User
    template_name = 'job/freelancers.html'
    ordering = ['-date_joined']
    paginate_by = 5
    
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
 

class ContactPageView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm



