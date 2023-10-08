from django.shortcuts import get_object_or_404, render, redirect
from .models import Article, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from myapp.models import UserProfile


@login_required
def home(request):
    user = request.user
    username = user.username
    user_type = user.userprofile.is_admin
    if user_type == True:
        user_type = "Admin User"
    else:
        user_type = "Normal User"

    context = {
        'username': username,
        'user_type': user_type,
    }
    return render(request, "home.html", context)


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')
        date_of_birth = request.POST.get('date_of_birth')
        bio = request.POST.get('bio')
        is_admin = request.POST.get('is_admin')
        password = request.POST.get('password')
        conform_password = request.POST.get('conform_password')

        if password != conform_password:
            messages.info(request, "password and confirm password are Not Same")
            return redirect('/signup')

        if first_name == last_name:
            messages.info(request, "First Name and Last Name are Not Same")
            return redirect('/signup')
        try:

            if User.objects.get(first_name=first_name):
                messages.warning(request, "User Name Already Exist")
                return redirect('/signup')
        except Exception as e:
            pass
        try:

            if User.objects.get(email=email):
                messages.warning(request, "Email Already Exist")
                return redirect('/signup')
        except Exception as e:
            pass

        new = User.objects.create(username=first_name + "_" + last_name, first_name=first_name, last_name=last_name,
                                  email=email, password=password)
        UserProfile.objects.create(user=new, profile_picture=profile_picture, date_of_birth=date_of_birth,
                                   bio=bio, is_admin=is_admin)
        messages.success(request, "User is Created Please Login")
        return redirect('/login')

    return render(request, "signup.html")


def handlelogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email, password=password).first()

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('/home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')

    return render(request, "login.html")


@login_required
def handlelogout(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/login')


@login_required
def article_page(request):
    articles = Article.objects.filter(is_public=True)
    comments = Comment.objects.all()
    context = {'articles': articles, 'comments': comments}
    return render(request, 'article_page.html', context)


@login_required
def user_article_page(request):
    articles = Article.objects.filter(author=request.user)
    comments = Comment.objects.all()
    context = {'articles': articles, 'comments': comments}
    return render(request, 'user_article_page.html', context)


@login_required
def add_comment(request, article_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        article = get_object_or_404(Article, pk=article_id)
        Comment.objects.create(article=article, author=request.user, content=content)
    return redirect('article_page')


@login_required
def hide_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.user == article.author:
        article.is_public = False
        article.save()

    return redirect('article_page')

@login_required
def unhide_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.user == article.author:
        article.is_public = True
        article.save()

    return redirect('user_article_page')


@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_public = request.POST.get('is_public')
        author = request.user
        Article.objects.create(title=title, content=content, is_public=is_public, author=author)
        return redirect('article_page')
    return render(request, 'add_article.html')


@login_required
def update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_public = request.POST.get('is_public')
        article.title = title
        article.content = content
        article.is_public = is_public
        article.save()
        return redirect('article_page')
    return render(request, 'update_article.html', {'article': article})


@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    user = request.user

    if user in article.likes.all():
        article.likes.remove(user)
    else:
        article.likes.add(user)
        article.dislikes.remove(user)

    return redirect('article_page')


@login_required
def dislike_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    user = request.user

    if user in article.dislikes.all():
        article.dislikes.remove(user)
    else:
        article.dislikes.add(user)
        article.likes.remove(user)

    return redirect('article_page')


@login_required
def user_list(request):
    if not request.user.is_authenticated or not request.user.userprofile.is_admin:
        return HttpResponseForbidden("You do not have permission to access this page.")

    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def remove_user(request, username):
    if not request.user.is_authenticated or not request.user.userprofile.is_admin:
        return HttpResponseForbidden("You do not have permission to remove users.")

    if request.method == 'POST':
        try:
            user_to_remove = User.objects.get(username=username)
            user_to_remove.delete()
        except User.DoesNotExist:
            pass
    return redirect('user_list')


@login_required
def delete_article(request, article_id):
    if request.method == 'POST':
        article = Article.objects.get(pk=article_id)
        if request.user.is_authenticated and request.user.userprofile.is_admin:
            article.delete()
    return HttpResponseRedirect(reverse('article_page'))
