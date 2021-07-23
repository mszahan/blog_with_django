from ablog.forms import CommentForm, EmailPostForm
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import *
from blog.settings import EMAIL_HOST_USER
from taggit.models import Tag
from django.db.models import Count, Q
# from django.db.models.signals import post_save

def post_list(request, tag_slug=None, search_q=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    

    if request.GET.get('search'):
        search_q = request.GET.get('search')
        print('this is the search query please check it out', search_q)
        print(type(search_q))
        object_list = Post.objects.filter(Q(title__icontains=search_q))
        print(object_list.count())


    # print(object_list)
    # print(len(object_list))
    # print(type(object_list))
    paginator = Paginator(object_list, 1) #three posts in each page
    page = request.GET.get('page')
    
    # print(paginator.num_pages)
    # print(type(paginator.num_pages))
    
    
    
    # p_range = paginator.get_elided_page_range()



    # print(type(page_i))
    # print(page_i)

    # print('Object_list',object_list)
    # print('paginator', paginator)
    # print('page', page)
    # print(paginator.page_range)
    # print(type(paginator.page_range))
    # print(paginator.page_range[0:1])
    try:
        posts = paginator.page(page)
        


        

        
        # for pos in posts.paginator.page_range:
        #     print('post', pos)
        # print('posts', posts)
        # print(type(posts))
    except PageNotAnInteger:
        #If page is not an integer deliver the first page
        page =1
        posts= paginator.page(page)

    except EmptyPage:
        # if page is out of range deliver last of results
        page = paginator.num_pages
        posts = paginator.page(page)

    # hf_range = 1
    # page_i = int(page)
    
    # if page_i < hf_range:
    #     page_i = hf_range
    # lst_range = page_i + hf_range
    # if lst_range >= paginator.num_pages:
    #     lst_range = paginator.num_pages

    # pg_range = paginator.page_range[page_i-hf_range:lst_range]



    # print(pg_range)
    # print(paginator.page_range)
    # print(type(pg_range))
    print(posts)
    print(type(posts))
    return render(request, 'ablog/list.html', {'posts':posts, 'page':page, 'tag':tag,
    'search_q':search_q, 'search_results':object_list})


# def post_detail(request, post):
#     # get post object
#     post = get_object_or_404(Post, slug=post)
#     # list of active parent comments
#     comments = post.comments.filter(active=True, parent__isnull=True)
#     if request.method == 'POST':
#         # comment has been added
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             parent_obj = None
#             # get parent comment id from hidden input
#             try:
#                 # id integer e.g. 15
#                 parent_id = int(request.POST.get('parent_id'))
#             except:
#                 parent_id = None
#             # if parent_id has been submitted get parent_obj id
#             if parent_id:
#                 parent_obj = Comment.objects.get(id=parent_id)
#                 # if parent object exist
#                 if parent_obj:
#                     # create replay comment object
#                     replay_comment = comment_form.save(commit=False)
#                     # assign parent_obj to replay comment
#                     replay_comment.parent = parent_obj
#             # normal comment
#             # create comment object but do not save to database
#             new_comment = comment_form.save(commit=False)
#             # assign ship to the comment
#             new_comment.post = post
#             # save
#             new_comment.save()
#             return redirect(post)
#     else:
#         comment_form = CommentForm()
#         return render(request,
#                     'core/detail.html',
#                     {'post': post,
#                     'comments': comments,
#                     'comment_form': comment_form})


def post_detail(request, slug, pk, tag_slug=None):
    post = get_object_or_404(Post, slug=slug, pk=pk, status='published')

    comments = post.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post = post
            # save
            new_comment.save()
            return redirect(post)
    else:
        comment_form = CommentForm()





    # comments = post.comments.filter(active=True)
    # if request.method =="POST":
    #     # a comment was posted
    #     comment_form = CommentForm(request.POST)
        
    #     if comment_form.is_valid():
    #     #create comment object but don't save to database yet
    #         new_comment = comment_form.save(commit=False)

    #         #assign the current post the the commment 
    #         new_comment.post = post

    #         #save the comment to the database
    #         new_comment.save()
    #         return redirect(post)
    # else:
    #     comment_form = CommentForm()

    # to find out the similar posts based on tags
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('same_tags', '-publish')[:3]

        
    return render(request, 'ablog/detail.html', {'post':post, 'comment_form':comment_form, 
    'comments':comments, 'similar_posts':similar_posts})



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'ablog/cat_list.html', {'cats':categories})



def category_detail(request, cat):
    category = get_object_or_404(Category, name=cat)
    posts = Post.objects.filter(category=category)
    return render(request, 'ablog/category_detail.html', {'posts':posts, 'category':cat})




def post_share(request, pk):
    #retrive post by id
    post = get_object_or_404(Post, pk=pk, status='published')
    sent = False
    

    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #form field passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{ cd['name']}, ({cd['email']}) recommends you reading '{post.title}'. "
            message = f"Read {post.title} at this link {post_url} comment: { cd['comments']}"
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent =True
    else:
        form = EmailPostForm()
    context = {'post':post, 'form':form, 'sent':sent}
    return render(request, 'ablog/share.html', context)


# def search_view(request):
#     # whatever user write in search box we get in query
#     query = request.GET['query']
#     products=models.Product.objects.all().filter(name__icontains=query)
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0

#     # word variable will be shown in html when user click on search button
#     word="Searched Result :"

#     if request.user.is_authenticated:
#         return render(request,'ecom/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
#     return render(request,'ecom/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})

def search_blog(request):
    if request.GET.get('search'):
        print('yes we got the search content that is ')
    query = request.GET.get('search')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))


    return render(request, 'ablog/search_blog.html',{'posts':posts, 'query':query})


