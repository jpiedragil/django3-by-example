from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

# This import is used in the function based post list view.
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

from .models import Post
from .forms import EmailPostform


# Create your views here.
class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


'''
This is the function-based view for the post list.
def post_list(request):

    object_list = Post.published.all()

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    print(paginator)
    try:

        posts = paginator.page(page)

    except PageNotAnInteger:

        # If page is not an integer deliver the first page.
        posts = paginator.page(1)

    except EmptyPage:

        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html',
                  {'page': page, 'posts': posts})
'''


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):

    sent = False
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')

    if request.method == 'POST':

        # Form was submitted
        form = EmailPostform(request.POST)

        if form.is_valid():
            print("Forma válida")
            # Form fields passed validation
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'javier.piedragil@gmail.com',
                      [cd['to']])
            sent = True

    else:
        print("Forma vacía")
        form = EmailPostform()

    return render(request, 'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})
