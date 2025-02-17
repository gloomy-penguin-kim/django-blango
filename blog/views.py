from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from django.utils import timezone
from blog.models import Post 

import logging 

logger = logging.getLogger(__name__)

def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, "blog/index.html", {"posts": posts})


from django.shortcuts import redirect
from blog.forms import CommentForm
def post_detail(request, slug):  
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None

    #return render(request, "blog/post-detail.html", {"post": post})
    return render(
        request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )


# # request. One major security flaw you could introduce is if you decided to
# # # cache any page whose content depends on the logged-in user.
@cache_page(300)
#@vary_on_headers("Cookie") 
@vary_on_cookie
def index(request):
    # existing view code
    from django.http import HttpResponse
    #return HttpResponse(str(request.user).encode("ascii"))
    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})