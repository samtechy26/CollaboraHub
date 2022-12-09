import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from job.models import Job, Bid
from job.forms import BidForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views import generic
from django.contrib.auth.models import User
from .models import UserLibrary
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from .models import Review





class UserDashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'user/userdashboard.html'

class ReviewsPage(LoginRequiredMixin, generic.ListView):
    template_name = 'user/reviews.html'
    def get_queryset(self):
        job = Job.objects.filter(author=self.request.user)
        return Bid.objects.filter(job__in=job)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'reviews': Review.objects.all()
        })
        return context
    context_object_name = 'bids'

class Reviews(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        bid_id = request.GET.get('bid_id')
        bid = Bid.objects.get(id=bid_id)
        comment = request.GET.get('message2')
        rate = request.GET.get('rating')
        user = request.user
        Review(user=user, bid=bid, comment=comment, rate=rate).save()
        return redirect('reviews')

def reviews(request):
    #job_lists = Job.objects.all()
    review_lists = Review.objects.filter(active=True)
    job_lists = Job.objects.exclude(reviews__in =review_lists)
    lists = list(chain(review_lists, job_lists))
    paginator = Paginator(lists, per_page=2)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    
    return render(request, 'user/reviews.html',{
        'jobs':jobs
    })



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

    # def get_context_data(self, **kwargs):
    #     context = (UserFavourites, self).get_context_data(**kwargs)
    #     user = User.objects.all
    #     context['users'] = user
    #     return context




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
def add_review(request):

    
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = data.get('comment','')
        rating = data.get('rating','1')
        timely = False
        on_budget = False


        if data.get('timely') == "1":
            timely = True
        #project_id = data.get('project_id')
        if data.get('on_budget') == "1":
            on_budget = True
        
        freelancer = get_object_or_404(User, username = data.get('freelancer'))
        client = get_object_or_404(User, username = data.get('employer'))
        project = get_object_or_404(Job, id = int(data.get('project')))
        
        #project = get_object_or_404(Job, id = project_id)
        new_review = Review.objects.update_or_create(employer =client, freelancer = freelancer,project=project,\
             comment=comment, rating=rating, on_budget=on_budget, timely=timely)
        #ew_review.save()

        return JsonResponse({
                "message":"Your review has been sucessfully added! "
            },status=200)
       
            
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        comment = data.get('comment','')
        rating = data.get('rating','1')
        review_id = data.get('reveiw_id','')
        timely = False
        on_budget = False


        if data.get('timely') == "1":
            timely = True
        #project_id = data.get('project_id')
        if data.get('on_budget') == "1":
            on_budget = True
        
        try:
            review = Review.objects.get(id= int(review_id))
            review.comment = comment
            review.timely = timely
            review.on_budget = on_budget
            review.rating = rating
            review.save()
            return JsonResponse({
                "message":"Your review has been updated successfully!"
            }, status=200)
        except Review.DoesNotExist:
            return JsonResponse({
                "message":"No such review existed"
            }, status=400)


    elif request.method == 'DELETE':
        data = json.loads(request.body)
        review_id = data.get('review_id')
        try:
            review = Review.objects.get(id=review_id)
            review.active = False
            review.save()
            return JsonResponse({
                "message":"Your review has been sucessfully deleted!"
            }, status = 201)

        except Review.DoesNotExist:
            return JsonResponse({
                "message":"There is no such review"
            }, status=400 )

