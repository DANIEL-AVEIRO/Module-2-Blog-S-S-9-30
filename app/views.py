from django.shortcuts import render, redirect
from app.models import PostModel, CategoryModel, CommentModel
from django.db.models import Q  # 1
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    search = request.GET.get("search")
    posts = PostModel.objects.all()
    if search:
        posts = posts.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(category__name__icontains=search)
        )
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"posts": page_obj}
    return render(request, "index.html", context)


def post_list(request):
    posts = PostModel.objects.all()
    context = {"posts": posts}
    return render(request, "post_list.html", context)


def post_create(request):
    if request.method == "GET":
        categories = CategoryModel.objects.all()  # 1
        context = {"categories": categories}  # 2
        return render(request, "post_create.html", context)  # 3
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        viewer = request.POST.get("viewer")
        image = request.FILES.get("image")
        category = request.POST.get("category")  # 4

        post = PostModel.objects.create(
            title=title,
            description=description,
            viewer=viewer,
            image=image,
            category_id=category,  # 5
        )
        post.save()
        return redirect("/post/list/")


def post_update(request, pk):
    post = PostModel.objects.get(id=pk)
    categories = CategoryModel.objects.all()  # 1
    context = {"post": post, "categories": categories}
    if request.method == "GET":
        return render(request, "post_update.html", context)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        viewer = request.POST.get("viewer")
        image = request.FILES.get("image")
        category = request.POST.get("category")

        post.title = title
        post.description = description
        post.category_id = category
        if image:
            if post.image:
                post.image.delete()
            post.image = image
        post.viewer = viewer
        post.save()
        return redirect("/post/list/")


def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    context = {"post": post}
    if request.method == "GET":
        return render(request, "post_delete.html", context)

    if request.method == "POST":
        if post.image:
            post.image.delete()
        post.delete()
        return redirect("/post/list/")


def post_detail(request, pk):
    post = PostModel.objects.get(id=pk)
    comments = CommentModel.objects.filter(post_id=post.id).order_by("-created_at")
    context = {"post": post, "comments": comments}
    return render(request, "post_detail.html", context)


@login_required(login_url="/login/")
def category_list(request):
    categories = CategoryModel.objects.all()
    context = {"categories": categories}
    return render(request, "category_list.html", context)


@login_required(login_url="/login/")
def category_create(request):
    if request.method == "GET":
        return render(request, "category_create.html")
    if request.method == "POST":
        name = request.POST.get("name")

        category = CategoryModel.objects.create(
            name=name,
        )
        category.save()
        return redirect("/category/list/")


def category_update(request, pk):
    category = CategoryModel.objects.get(id=pk)
    context = {"category": category}
    if request.method == "GET":
        return render(request, "category_update.html", context)

    if request.method == "POST":
        name = request.POST.get("name")

        category.name = name
        category.save()
        return redirect("/category/list/")


def category_delete(request, pk):
    category = CategoryModel.objects.get(id=pk)
    context = {"category": category}
    if request.method == "GET":
        return render(request, "category_delete.html", context)

    if request.method == "POST":
        category.delete()
        return redirect("/category/list/")


from django.contrib import messages


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            messages.warning(request, "You are currently login")
            return redirect("/")
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        # if user is not None:
        if user:
            login(request, user)
            messages.success(request, "Login successfully")
        else:
            messages.error(request, "Invalid credential")
            return redirect("/login/")
        return redirect("/")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        existing_user = User.objects.filter(username=username)

        if existing_user:
            messages.warning(request, "Username already exists")
            return redirect("/register/")

        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        user.save()
        return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/login/")


def comment_create(request, post_pk):
    post = PostModel.objects.get(id=post_pk)
    if request.method == "POST":
        comment = CommentModel.objects.create(
            message=request.POST.get("message"),
            author_id=request.user.id,
            post_id=post.id,
        )
        comment.save()
        messages.success(request, "Comment successfully")
        return redirect(f"/post/detail/{post.id}/")


def profile(request):
    return render(request, "profile.html")
