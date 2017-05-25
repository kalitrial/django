from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, \
  PageNotAnInteger
# from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag

#aggregation function of the Django ORM. allows aggregated counts
from django.db.models import Count
from haystack.query import SearchQuerySet



# A Django view is just a Python function that receives a web request and returns a web response. Inside view goes all
# the logic to return the desired response
"""
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'

"""
def post_list(request, tag_slug=None):

    tag = None
    object_list = Post.published.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 4)  # 4 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of active comments for this post
    comments = post.comments.filter(active=True)

    #list of similar posts

    #retrieve a python list of id's for the tags of the current post.
    #The `values_list()` queryset returns tuples with the values for the given fields. We are passing  `flat=True` to get
    #a flat list like [1, 2, 3, ..]

    post_tags_ids = post.tags.values_list('id', flat=True)

    #we use `Count` aggregation to generate a calculated field `same_tags` that contains the number of tags shared with all
    #tags queried
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                    .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags'))\
                                    .order_by('-same_tags', '-publish')[:4]

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            #Create comment object but dont save to database
            new_comment = comment_form.save(commit=False)

            #Assign the current post to the comment- by doing so, we are specifying that the new comment belongs to a given post
            new_comment.post = post
            #save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})

# render() is a shortcut provided by Django to render the list of posts with the given template.
# It takes in a request object as parameter, the template path and the variable to render the given template
# It returns an HttpResponse object with the rendered text(normally HTML code)


def post_share(request, post_id):
    #Retrieves post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted

        #creating form instance using submitted data contained in request.POST
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field passed validation
            cd = form.cleaned_data
            # ...Send email

            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])

            send_mail(subject, message, 'admin@email.com', [cd['to']])

            sent = True


    else:
            # we create a new form instance that will be used to display the empty form in the template
            form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                        'form':form,
                                                        'sent': sent})

def post_search(request):
    form = SearchForm()
    cd = None
    results =None
    total_results = None

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data

            # load_all() -> loads all related Post objects from the database at once
            results = SearchQuerySet().models(Post)\
                                    .filter(content=cd['query']).load_all()

            #count total results
            total_results = results.count()
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'cd': cd,
                   'results': results,
                   'total_results': total_results})