from django.shortcuts import render, redirect
from app.models import PostModel

# Create your views here.


def index(request):
    posts = PostModel.objects.all()
    context = {"posts": posts}
    return render(request, "index.html", context)


def post_list(request):
    posts = PostModel.objects.all()
    context = {"posts": posts}
    return render(request, "post_list.html", context)


def post_create(request):
    if request.method == "GET":
        return render(request, "post_create.html")
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        viewer = request.POST.get("viewer")
        image = request.FILES.get("image")

        post = PostModel.objects.create(
            title=title, description=description, viewer=viewer, image=image
        )
        post.save()
        return redirect("/post/list/")


def post_update(request, pk):
    post = PostModel.objects.get(id=pk)
    context = {"post": post}
    if request.method == "GET":
        return render(request, "post_update.html", context)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        viewer = request.POST.get("viewer")
        image = request.FILES.get("image")

        post.title = title
        post.description = description
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
    context = {"post": post}
    return render(request, "post_detail.html", context)
