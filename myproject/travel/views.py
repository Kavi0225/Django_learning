from django.shortcuts import render, get_object_or_404, redirect
from .models import Destination, DestinationDetail, Comments
from .forms import *
from django.contrib.auth.decorators import login_required

def index(request):
    dest = Destination.objects.all()
    return render(request, "index.html", {'dest': dest, 'is_authenticated' : request.user.is_authenticated})

@login_required
def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    details = DestinationDetail.objects.filter(destination=destination)
    comments = Comments.objects.filter(DestinationDetail__destination=destination, parent=None)  

    form = CommentForm()  # Initialize the form before the if statement

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.DestinationDetail = details.first()

            parent_id = request.POST.get("parent_id")
            
            if parent_id:
                parent_comment = Comments.objects.get(id=parent_id)
                comment.parent = parent_comment
            comment.save()

            return redirect('destination_detail', destination_id=destination.id)

    return render(request, 'destination_detail.html', {
        'destination': destination,
        'details': details,
        'comments': comments,
        'form': form
    })

def like_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    comment.likes += 1
    comment.save()
    return JsonResponse({'likes': comment.likes, 'dislikes': comment.dislikes})

def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    comment.dislikes += 1
    comment.save()
    return JsonResponse({'likes': comment.likes, 'dislikes': comment.dislikes})