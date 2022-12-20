import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from job.models import Job, Bid
from job.forms import BidForm
from django.conf import settings
from django.views import generic
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from .models import Review, Profile





class UserDashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'user/userdashboard.html'


class UserTaskList(LoginRequiredMixin, generic.ListView):
    template_name = 'user/task_list.html'

    def get_queryset(self):
        return Job.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
       context =  super(UserTaskList, self).get_context_data(**kwargs)
       job = Job.objects.filter(author = self.request.user)
       count = job.count()
       context.update({
            "count":count
       })

       return context

class UserFavourites(LoginRequiredMixin, generic.ListView):
    template_name = 'user/favourites.html'
    context_object_name = "tasks"
    
    def get_queryset(self):
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context =  super(UserFavourites, self).get_context_data(**kwargs)
        users = User.objects.all()
        context.update({
            'users':users
        })
        return context
        


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



@login_required
def dashboard_bidders(request, id):
    
    jobs = Job.objects.filter(id=id)
    job = Job.objects.get(id=id)
    bids = Bid.objects.filter(job__in=jobs)
    bid_count = bids.count()
    
    context = {
        'job':job,
        'bids':bids,
        'bid_count':bid_count,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'user/manage_bidders.html', context)

@login_required
def dashboard_mybids(request):
    current_user = request.user
    bids = Bid.objects.filter(user=current_user)
    
    form = BidForm()
    
    
    context = {
        'bids':bids,
        'form':form
    }
    return render(request, 'user/my_bids.html', context)

@login_required
def bid_update(request, id):
    current_user = request.user
    bid = Bid.objects.get(id=id)
    
    form = BidForm(instance=bid)
    
    if request.method == 'POST':
        form = BidForm(request.POST, instance=bid)
        if form.is_valid():
            form.save()
            return redirect('my_bids')
    context = {
        'bid':bid,
        'form':form
    }
    return render(request, 'user/bid_update.html', context)


@login_required
def manage_offer(request, id):
    bid = Bid.objects.get(id=id)
    
    context = {
        'bid':bid,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'user/manage_offer.html', context)


class BidPaymentView(LoginRequiredMixin, generic.DetailView):
    model = Bid
    template_name = 'user/bid_payment.html'
    context_object_name = 'bid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })

        return context


class UserLibraryView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'user/task_library.html'
   


@login_required
def reviews(request):
    if request.method == 'POST':
        comment = request.POST.get("message")
        rating = request.POST.get('rating')
        employer_id = request.POST.get('employer', '')
        user_id = request.POST.get('user','')
        freelancer_id = request.POST.get('freelancer', '')
        bid_id = request.POST.get('bid','')
        project_id = request.POST.get('project','')
        edit_review = request.POST.get("editreview")
        review_id = request.POST.get("reviewid")
        on_budget = request.POST.get("radio")
        timely = request.POST.get('radio2')
 
        updated_values = {
            'timely':timely,
            'on_budget':on_budget,
            'rating':rating,
            'comment':comment
        }

        if edit_review == "True":
            updated_review = Review.objects.get(id=review_id)
            updated_review.comment = comment
            updated_review.rating = rating
            updated_review.timely = timely
            updated_review.on_budget = on_budget
            updated_review.save()

        else:
            employer =  None if employer_id == "" else Profile.objects.get(id=int(employer_id)) 
            freelancer = None if freelancer_id == "" else Profile.objects.get(id=int(freelancer_id))    
            user = None if user_id == ""  else User.objects.get(id=int(user_id))    
            bid =  None if bid_id == "" else Bid.objects.get(id=int(bid_id))    
            project = None  if project_id =="" else Job.objects.get(id=int(project_id))   

            obj, created = Review.objects.update_or_create(employer=employer, freelancer=freelancer, user=user, \
                bid=bid, project=project,active=True, defaults=updated_values)
            obj.clean()

        messages.success(request, "review successfully added! ")
        return HttpResponseRedirect(request.path_info)

    elif request.method == 'GET':
        employers_reviews = Review.objects.filter(active=True, freelancer__isnull = True, employer__isnull=False)
        jobs_lists = Job.objects.exclude(reviews__in =employers_reviews)
        job = list(chain(employers_reviews, jobs_lists))

        freelancer_reviews = Review.objects.filter(active=True, employer__isnull = True, freelancer__isnull = False)
        bid_lists = Bid.objects.exclude(reviews__in = freelancer_reviews)
        bid = list(chain(freelancer_reviews, bid_lists))

        employer_paginator = Paginator(job, per_page=2)
        freelancer_paginator = Paginator(bid, per_page=2)
        page = request.GET.get('page')
        try:
            jobs = employer_paginator.page(page)
            bids = freelancer_paginator.page(page)
        except PageNotAnInteger:
            jobs = employer_paginator.page(1)
            bids = freelancer_paginator.page(1)
        except EmptyPage:
            jobs = employer_paginator.page(employer_paginator.num_pages)
            bids = freelancer_paginator.page(freelancer_paginator.num_pages)

        
        return render(request, 'user/reviews.html',{
            'bids':bids,
            'jobs':jobs
        })

def review(request, review_id):       
    if request.method == "DELETE":
        data = json.loads(request.body)
        review_id = data.get("review_id")
        review = Review.objects.get(id=int(review_id))
        review.active = False
        review.save()
        return JsonResponse({
            "message":"reveiw deleted!"
        })