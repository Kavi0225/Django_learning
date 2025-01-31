from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Destination, DestinationDetail, Comments
from .forms import *
from django.contrib.auth.decorators import login_required

def index(request):
    dest = Destination.objects.all()
    request.session.setdefault("click_count", 0)  # Initialize click count if not set
    return render(request, "index.html", {'dest': dest, 'is_authenticated': request.user.is_authenticated})

def destination_detail(request, destination_id):
    # Allow unlimited clicks for logged-in users
    if not request.user.is_authenticated:
        click_count = request.session.get("click_count", 0)
        
        if click_count >= 2:  # Redirect to login after 2 clicks
            return redirect("login")
        
        request.session["click_count"] = click_count + 1  # Increment click count

    destination = get_object_or_404(Destination, pk=destination_id)
    details = DestinationDetail.objects.filter(destination=destination)

    # Avoid error if details list is empty
    first_detail = details.first()
    comments = Comments.objects.filter(DestinationDetail=first_detail, parent=None) if first_detail else Comments.objects.none()

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.DestinationDetail = first_detail  # Assign the first available detail
            
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

    comment = get_object_or_404(Comments, id=comment_id)
    comment.likes += 1
    comment.save()
    return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})

def dislike_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to dislike a comment."}, status=403)

    comment = get_object_or_404(Comments, id=comment_id)
    comment.dislikes += 1
    comment.save()
    return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})

@login_required
def reset_clicks_on_login(request):
    request.session["click_count"] = 0  # Reset click count after login
    return redirect("index")  # Redirect to homepage or another page
