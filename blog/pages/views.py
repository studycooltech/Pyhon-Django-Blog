from django.shortcuts import render, redirect,get_object_or_404, HttpResponseRedirect
from .models import Post, Category,Profile,Tags,Comment,SubComment,Join,Banner
from django.contrib.auth.models import User
from .forms import PostForm,ProfileForm
from django.views.generic import View ,FormView
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.http import JsonResponse
from django.db.models import Q
import json

# Create your views here.

def home(request):
    posts = Post.objects.filter(draft=False)
    show_slide = Banner.objects.all()
    categories = Category.objects.all()
    lt_posts = Post.objects.filter(draft=False).order_by('-published')[0:3]
    tags = Tags.objects.all()
    context = {'posts':posts,'category':categories,'latest_post':lt_posts,'tags':tags,'slides':show_slide}
    return render(request,'pages/home.html',context)

def contact(request):
    return render(request,'pages/contact.html')



def profile(request,id=None):
    try:
        profile = get_object_or_404(Profile, id=id)
        posts = Post.objects.filter(user__profile_name=profile.profile_name)
        context = {
            'profile': profile,
            'posts': posts,
            }
        template = 'pages/profile-view.html'
        return render(request, template, context)
    except:
        try:
            profile = Profile.objects.get(user=request.user)
            posts = Post.objects.filter(user__profile_name=profile.profile_name)
            context = {
                'profile': profile,
                'posts': posts,
            }
            template = 'pages/profile-view.html'
            return render(request, template, context)
        except:
            return redirect('profile-create')


def profile_create(request):
    form = ProfileForm()
    name = request.user.first_name + ' ' + request.user.last_name
    email = request.user.email
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.profile_name = name
            profile.email = email
            profile.save()
            return redirect('profile', id=profile.id)
    context = {
        'form': form,
        'name': name,
        'email': email,
        }
    template = 'pages/profile_create.html'
    return render(request, template, context)


def addPhoto(request):
    if request.method == 'POST':
        title= request.POST.get('title')
        ban_desc= request.POST.get('description')
        images = request.FILES.getlist('images')
        for image in images:
            photo = Banner.objects.create(
                user = request.user,
                title= title,
                description=ban_desc,
                slide=image,
            )
        
        return redirect('home')
    return render(request, 'pages/add-banner.html')

def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    posts = Post.objects.filter(user__profile_name=profile.profile_name)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile', profile.id)
    context = {
        'form': form,
        'posts': posts,
        }
    template = 'pages/profile_edit.html'
    return render(request, template, context)


@login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })

def user_reg(request):
    if request.method == 'POST'and request.is_ajax():
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password!=re_password:
            return JsonResponse({'error':'1','msg':'password does not matched'}, status=200)

        elif User.objects.filter(email=email).exists():
            return JsonResponse({'error':'1','msg':'email is already exists'}, status=200)
        elif User.objects.filter(username=uname).exists():
            return JsonResponse({'error':'1','msg':'username is already exists'}, status=200)
        else:
            user = User.objects.create_user(username=uname,email=email,password=password)
            user.save()
            return JsonResponse({'error':'0','msg':'user has been registerd successfully'}, status=200)
    return JsonResponse({'error':'1','msg':'somthing went wrong'}, status=400)


def user_login(request):
    if request.method == 'POST'and request.is_ajax():
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        user = authenticate(request,username=User.objects.get(email=uname), password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return JsonResponse({'error':'0','msg':'login successfully'}, status=200)
            else:
                return JsonResponse({'error':'1','msg':'in-active'}, status=200)
        else:
            return JsonResponse({'error':'1','msg':'username and password is wrong.'},status=200)

    return JsonResponse({'error':'1','msg':'somthing went wrong'}, status=400)


def single_post(request,slug,id):
    post_detail = Post.objects.get(id=id)
    post_detail.post_views = post_detail.post_views + 1
    post_detail.save()
    categories = Category.objects.all()
    show_slide = Banner.objects.all()
    lt_posts = Post.objects.filter(draft=False).order_by('-published')[0:3]
    tags = Tags.objects.all()
    total_comt = SubComment.objects.filter(post =post_detail ).count()
    if request.method == 'POST':
        msg_body = request.POST.get('msg_body')
        comm_id = request.POST.get('comm_id') #None
        # post = Post.objects.get(id=comm_id)

        if comm_id:
            SubComment(post=post_detail,
                    user = request.user,
                    comm = msg_body,
                    comment = Comment.objects.get(id=int(comm_id))
                ).save()
        else:
            Comment(post=post_detail, user=request.user, comm=msg_body).save()


    comments = []
    for c in Comment.objects.filter(post=post_detail):
        comments.append([c, SubComment.objects.filter(comment=c)])

    context = {'comments':comments,'posts':post_detail,'category':categories,'latest_post':lt_posts,'tags':tags,'total_cmt':total_comt,'slides':show_slide}
    return render(request,'pages/single-post.html',context)


def post_publish(request):
    """Creating Posts using model form"""
    profile = Profile.objects.get(user = request.user)
    posts = Post.objects.filter(user__profile_name = profile.user_id)
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = profile
        instance.save()
        return redirect('home')
    context = {
        'form': form,
        'posts': posts,
    }
    template = 'pages/post_create.html'
    return render(request, template, context)


@login_required
def posts_update(request, id=None):
    """Updating individual item"""
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None,
                    instance=instance)
    if request.user.username == instance.user.user.username:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.draft = True
            instance.save()
            messages.success(request, 'Updated Successfully ! Pending For Admin Approval...', extra_tags='html_safe')
            return redirect('single_post', instance.id,instance.slug)
    else:
        raise Http404
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    template = 'pages/post_update.html'
    return render(request, template, context)


@login_required
def posts_delete(request, id=None):
    """Deleting individual item"""
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Deleted Successfully !', extra_tags='html_safe')
    return redirect('home')


def search(request):
    q = request.GET.get('postSearch')
    posts = Post.objects.filter(
        Q(title__icontains = q) |
        Q(content__icontains = q)
        ).distinct()
    context = {
        'posts':posts,
        
        }

    return render(request, 'pages/home.html', context)


 
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Join.objects.filter(email=email).exists():
            return JsonResponse({'error':'1','msg':'You have already subscribed'}, status=200)
        join_sub = Join(email =email).save()
        return JsonResponse({'error':'0','msg':'Subscribe successfully'}, status=200)
    return JsonResponse({'error':'1','msg':'method not allowed'}, status=200)


   

def user_logout(request):
    logout(request)
    return redirect('home')




'''
class HomeView(FormView):
    template_name = 'pages/home.html'
    form_class = JoinForm
'''


