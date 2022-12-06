from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Category, Bid, Skill
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, FormView
from .forms import BidForm, ContactForm



class HomeView(ListView):
    model = Job
    template_name = 'pages/home.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            "recent_tasks": Job.objects.all().order_by('-date_created')[:4]
        })
        return context




class JobCreateView(CreateView):
    model = Job
    fields = [ 'title', 'job_type', 'job_category', 'cost',  'skill', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class JobListView(ListView):
    model = Job
    template_name = 'job/job_list.html'
    paginate_by = 5
    

    def get_queryset(self):
        qs = Job.objects.all()
        category = self.request.GET.get('category', None)
        if category:
            qs = qs.filter(Q(job_category__slug=category))
        return qs


    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context.update({
            "categories": Category.objects.all,
            
        })
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
 

class ContactPageView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm



# class ProductDetailView(generic.DetailView):
#     template_name = "products/product.html"
#     queryset = Product.objects.all()
#     context_object_name = "product"

#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(**kwargs)
#         product = self.get_object()
#         has_access = False
#         if self.request.user.is_authenticated:
#             if product in self.request.user.userlibrary.products.all():
#                 has_access = True
#         context.update({
#             "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
#             "has_access": has_access
#         })
#         return context