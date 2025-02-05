from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Destination, DestinationDetail, Comments, ClickTracker
from .forms import *
from django.db.models import F

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def index(request):
    dest = Destination.objects.all()
    
    if not request.user.is_authenticated:
        ip_address = get_client_ip(request)
        click_record, _ = ClickTracker.objects.get_or_create(ip_address=ip_address)

        if click_record.count >= 2:
            return redirect(reverse("login"))

    return render(request, "index.html", {"dest": dest, "is_authenticated": request.user.is_authenticated})

def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    details = DestinationDetail.objects.filter(destination=destination)
    comments = Comments.objects.filter(destination_detail__destination=destination)
    form = CommentForm()

    if not request.user.is_authenticated:
        ip_address = get_client_ip(request)
        click_record, created = ClickTracker.objects.get_or_create(ip_address=ip_address)

        if click_record.count >= 2:
            return redirect(reverse("login"))

        ClickTracker.objects.filter(ip_address=ip_address).update(count=F("count") + 1)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.destination_detail = details.first()

            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent_comment = Comments.objects.filter(id=parent_id).first()
                if parent_comment:
                    comment.parent = parent_comment

            comment.save()
            return redirect("destination_detail", destination_id=destination.id)

    return render(request, "destination_detail.html", {
        "destination": destination,
        "details": details,
        "comments": comments,
        "form": form
    })

def like_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to like a comment."}, status=403)
        return redirect('login')
    comment = get_object_or_404(Comments, id=comment_id)
    comment.likes += 1
    comment.save()
    return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})

def dislike_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to dislike a comment."}, status=403)
        return redirect('login')
    comment = get_object_or_404(Comments, id=comment_id)
    comment.dislikes += 1
    comment.save()
    return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})

@login_required
def reset_clicks_on_login(request):
    ip_address = get_client_ip(request)
    ClickTracker.objects.filter(ip_address=ip_address).update(count=0)
    return redirect("index")
