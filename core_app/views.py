from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.contrib import messages

from rest_framework import generics
from .serializers import AdSerializer
from rest_framework.permissions import AllowAny 


from .models import Ad, Category, Favorite, Review
from .forms import UserRegisterForm, AdForm, ReviewForm

def ad_list_view(request):
    vip_ads = Ad.objects.filter(is_moderated=True, vip_requested=True).order_by('-created_at')
    ads = Ad.objects.filter(is_moderated=True, vip_requested=False).order_by('-created_at')
    
    q = request.GET.get('q')
    if q:
        query = Q(title__icontains=q) | Q(description__icontains=q)
        ads = ads.filter(query)
        vip_ads = vip_ads.filter(query)
    
    category_slug = request.GET.get('category')
    if category_slug:
        ads = ads.filter(category__slug=category_slug)
        vip_ads = vip_ads.filter(category__slug=category_slug)

    paginator = Paginator(ads, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'ad_list.html', {
        'vip_ads': vip_ads,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'current_category': category_slug,
    })

def ad_detail_view(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    reviews = ad.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, ad=ad).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ad = ad
            review.author = request.user
            review.save()
            messages.success(request, "Отзыв успешно добавлен!")
            return redirect('ad_detail', uuid=ad.uuid)
    else:
        form = ReviewForm()
        
    return render(request, 'ad_detail.html', {
        'ad': ad, 
        'is_favorite': is_favorite,
        'reviews': reviews,
        'form': form,
        'avg_rating': round(avg_rating, 1)
    })

@login_required
def toggle_favorite(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    fav, created = Favorite.objects.get_or_create(user=request.user, ad=ad)
    if not created:
        fav.delete()
    return redirect(request.META.get('HTTP_REFERER', 'ad_list'))

@login_required
def favorites_list_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('ad')
    favorite_ads = [fav.ad for fav in favorites]
    return render(request, 'favorites.html', {'favorite_ads': favorite_ads})

@login_required
def ad_create_view(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save() 
            return redirect('profile')
    else:
        form = AdForm()
    return render(request, 'ad_form.html', {'form': form})

@login_required
def ad_update_view(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid, author=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', uuid=ad.uuid)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ad_form.html', {'form': form, 'ad': ad})

@login_required
def ad_delete_view(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid, author=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('profile')
    return render(request, 'ad_confirm_delete.html', {'ad': ad})

@login_required
def profile_view(request):
    my_ads = Ad.objects.filter(author=request.user).order_by('-created_at')
    favorites = Favorite.objects.filter(user=request.user).select_related('ad')
    return render(request, 'profile.html', {'my_ads': my_ads, 'favorites': favorites})

@login_required
def toggle_vip(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid, author=request.user)
    ad.vip_requested = not ad.vip_requested
    ad.save()
    return redirect(request.META.get('HTTP_REFERER', 'ad_list'))

def register_view(request):
    if request.user.is_authenticated: return redirect('ad_list')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')
    else: form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated: return redirect('profile')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else: form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('ad_list')

class AdListAPIView(generics.ListCreateAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated else None)