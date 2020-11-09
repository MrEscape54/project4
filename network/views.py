import json
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import UserEditForm, ProfileEditForm, PostForm
from .models import Profile, User, Post
from django.urls import reverse_lazy
from itertools import chain


def index(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    active = 'index'

    if request.method == 'POST':
        if request.user.is_authenticated:
            post_form = PostForm(data=request.POST)
            if post_form.is_valid():
                post_form = post_form.save(commit=False)
                post_form.author = request.user.profile
                post_form.save()
                return redirect('index')
        else:
            return redirect('login')
    else:
        post_form = PostForm()
    return render(request, "network/index.html", {'posts': posts, 'post_form': post_form, 'active': active, 'page_obj': page_obj})


def posts(request):
    posts = Post.objects.all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


@login_required
def following(request):
    profile = Profile.objects.get(user=request.user)
    following = [user for user in profile.following.all()]
    posts = []
    active = 'following'  # CSS menu flag
    qs = None
    message = None
    for u in following:
        p = Profile.objects.get(user=u)
        p_posts = p.posts.all()
        posts.append(p_posts)
    if len(posts) > 0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None
        message = "You are not following any user"

    return render(request, 'network/following.html', {'posts': qs, 'active': active, 'page_obj': page_obj, 'message': message})


""" def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


    def logout_view(request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


    def register(request):
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "network/register.html", {
                    "message": "Passwords must match."
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                Profile.objects.create(user=user)
            except IntegrityError:
                return render(request, "network/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/register.html") """


class CustomUserCreationForm(UserCreationForm):
    # Función para modificar los campos que queremos sean obligatorios o viceversa
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # En caso de requerir cambiar alguna propiedad de algún campo
        self.fields['username'].error_messages['invalid'] = _(
            'Enter a valid username')
        self.fields['email'].required = True
        self.fields['email'].help_text = 'Required'
        self.fields['first_name'].required = True
        self.fields['first_name'].help_text = 'Required'
        self.fields['first_name'].label = 'Display Name'

    class Meta(UserCreationForm.Meta):
        model = User
        # In case of needing other fields than default
        fields = ['username', 'first_name', 'email']


class UserCreationView(CreateView):
    # Clase para crear al usuario
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


@login_required
def edit_profile(request):
    # Get posts by the logged user
    posts = request.user.profile.posts.all()

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Profile updated successfully'))
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    user_form.fields['first_name'].label = 'Display Name'
    user_form.fields['first_name'].required = True
    user_form.fields['first_name'].help_text = 'Required'
    user_form.fields['email'].required = True
    user_form.fields['email'].help_text = 'Required'
    return render(request, 'network/profile.html', {'posts': posts, 'user_form': user_form, 'profile_form': profile_form})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'network/profile_detail.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        follow = False
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        context["follow"] = follow
        posts = view_profile.posts.all()
        context["posts"] = posts
        return context


@login_required
def follow_unfollow(request):

    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile_detail')


@login_required
def likes(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    if request.method == 'PUT':
        logged_user = Profile.objects.get(user=request.user)
        if logged_user in post.likes.all():
            post.likes.remove(logged_user)
        else:
            post.likes.add(logged_user)
        return HttpResponse(status=204)


@login_required
def edit_msg(request, post_id):

    if request.method != 'PUT':
        return JsonResponse({"error": "Only PUT method id allowed"}, status=404)

    post = get_object_or_404(Post, pk=post_id)

    data = json.loads(request.body)
    post.message = data['message']
    post.save()
    return HttpResponse(status=204)
