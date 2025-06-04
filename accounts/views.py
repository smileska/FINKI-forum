from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forum.models import Post, Reply
from accounts.models import Profile

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        messages.success(request, f'Account created for {username}! You can now log in.')
        return redirect('/accounts/login/')

    return render(request, 'accounts/register.html')


@login_required
def profile(request):
    try:
        user_posts = Post.objects.filter(author=request.user).select_related('category').order_by('-created_date')[:10]
        user_replies = Reply.objects.filter(author=request.user).select_related('post').order_by('-created_date')[:10]
        posts_count = Post.objects.filter(author=request.user).count()
        replies_count = Reply.objects.filter(author=request.user).count()
    except:
        user_posts = []
        user_replies = []
        posts_count = 0
        replies_count = 0

    context = {
        'user_posts': user_posts,
        'user_replies': user_replies,
        'posts_count': posts_count,
        'replies_count': replies_count,
    }
    return render(request, 'accounts/profile.html', context)


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    try:
        user_posts = Post.objects.filter(author=profile_user).select_related('category').order_by('-created_date')[:10]
        user_replies = Reply.objects.filter(author=profile_user).select_related('post').order_by('-created_date')[:10]
        posts_count = Post.objects.filter(author=profile_user).count()
        replies_count = Reply.objects.filter(author=profile_user).count()
    except:
        user_posts = []
        user_replies = []
        posts_count = 0
        replies_count = 0

    context = {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'user_replies': user_replies,
        'posts_count': posts_count,
        'replies_count': replies_count,
        'is_own_profile': request.user == profile_user,
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        try:
            if hasattr(request.user, 'profile'):
                request.user.profile.bio = request.POST.get('bio', '')
                request.user.profile.year = int(request.POST.get('year', 1))
                request.user.profile.faculty = request.POST.get('faculty', 'KN')
                request.user.profile.student_id = request.POST.get('student_id', '')
                request.user.profile.save()
            else:
                Profile.objects.create(
                    user=request.user,
                    bio=request.POST.get('bio', ''),
                    year=int(request.POST.get('year', 1)),
                    faculty=request.POST.get('faculty', 'KN'),
                    student_id=request.POST.get('student_id', '')
                )
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('accounts:profile')

    return render(request, 'accounts/edit_profile.html')