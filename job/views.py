from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Category, Bid, Skill
from django.views.generic.base import View, TemplateResponseMixin
from django.db.models import Q, Avg, Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, FormView, DeleteView
from django.views import generic
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from .forms import BidForm, ContactForm, JobCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from itertools import chain
import json



class HomeView(ListView):
    model = Job
    template_name = 'pages/home.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            "recent_tasks": Job.objects.all().order_by('-date_created')[:4],
            'categories': Category.objects.all()
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
        context['object_list'] = User.objects.annotate(rating=(Avg('profile__freelancer_review__rating')\
            +Avg('profile__employer_review__rating'))/2)
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


class HomeSearch(TemplateResponseMixin, View):
    paginate_by = 3
    bids = None
    skills = None
    template_name = 'job/freelancers.html'

    def post(self, request, *args, **kwargs):
        #data = json.loads(request.body)
        categories = request.POST.get('categories',"")
        search = request.POST.get("search", "")
        categories = categories.split(",")
        search = search.split()
        
        if len(search) > 1:
            
            search_query = list([word + "+" for word in search if word != search[len(search)-1]])
            search_query.append(search[len(search)-1])
            prepared_statement = "".join(q for q in search_query) 
        else:
            prepared_statement = search
        
        
        search_vector = SearchVector('job__description', weight='B') + SearchVector('job__title', weight='A')
        query = SearchQuery(prepared_statement, search_type='websearch')
        matched_bids = Bid.objects.annotate(rank = SearchRank(search_vector, query)).filter(rank__gte=0.2 ).order_by('-rank')
        matched_bids = matched_bids.annotate(rating=(Avg('reviews__rating')))
        HomeSearch.matched_length = len(matched_bids)
        
        
        
        categories_id = Category.objects.filter(title__in=categories)
        matched_categories = Bid.objects.filter(job__job_category__in=categories_id).exclude(user__in=matched_bids.values_list('user', flat=True)).distinct()
        matched_categories = matched_categories.annotate(rating=(Avg('reviews__rating')))
        
        

        #make this available in the get statement
        HomeSearch.bids = list(chain(matched_bids, matched_categories ))
        paginator = Paginator(HomeSearch.bids, per_page=3).page(1)
        
        
        HomeSearch.skills = Skill.objects.filter(id__in=(matched_bids.values_list("job__skill__id")))
            
        return self.render_to_response({
            "bids":HomeSearch.bids[:self.paginate_by],
            "skills":HomeSearch.skills,
            "matched_length": HomeSearch.matched_length,
            "search":True,
            "page_obj":paginator
        })

    def get(self, request, *args, **kwargs):
        #bids = request.GET.get('bids')
        #bids = self.request.session.get("bids")
        paginator = Paginator(HomeSearch.bids, per_page=self.paginate_by)
        
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        return self.render_to_response({
            "search":True,
            "bids":page_obj,
            "skills":HomeSearch.skills,
            "page_obj":page_obj
        })

