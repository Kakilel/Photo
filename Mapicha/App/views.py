from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, PhotoForm
from .models import Photo, Category,Like,Comment


def home(request):
    photos = Photo.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'home.html', {'photos': photos, 'categories': categories})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created. Head to Login")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gallery')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def gallery_view(request):
    photos = Photo.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'gallery.html', {'photos': photos, 'categories': categories})


def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    photos = Photo.objects.filter(category=category).order_by('-created_at')
    return render(request, 'category.html', {'category': category, 'photos': photos})


@login_required
def upload_view(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user  # ✅ fixed field
            photo.save()
            messages.success(request, "Photo Uploaded Successfully")
            return redirect('gallery')
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    comments = photo.comments.all().order_by('-created_at')
    
    if request.method == "POST":
        if request.user.is_authenticated:
            text = request.POST.get("comment")
            if text:
                Comment.objects.create(user=request.user, photo=photo, content=text)
                messages.success(request, "Comment added!")
                return redirect("photo_detail", pk=pk)
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect("login")

    return render(request, 'detail.html', {
        'photo': photo,
        'comments': comments,
        'likes_count': photo.likes.count(),
        'is_liked': request.user.is_authenticated and photo.likes.filter(user=request.user).exists()
    })

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, photo=photo)
    if not created:
        like.delete()  # toggle unlike
        messages.info(request, "You unliked this photo.")
    else:
        messages.success(request, "You liked this photo.")
    return redirect("photo_detail", pk=pk)


@login_required
def add_comment(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == "POST":
        text = request.POST.get("text")
        if text.strip():
            Comment.objects.create(photo=photo, user=request.user, text=text)
    return redirect("photo_detail", pk=photo_id)


@login_required
def my_photos(request):
    photos = Photo.objects.filter(uploaded_by=request.user).order_by('-created_at')
    return render(request, 'mine.html', {'photos': photos})


def profile_view(request, username):
    photos = Photo.objects.filter(uploaded_by__username=username).order_by('-created_at')
    return render(request, 'profile.html', {'photos': photos, 'username': username})
