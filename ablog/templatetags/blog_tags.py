from django import template
from django.db.models import Count

register = template.Library()

from ablog.models import Post

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('ablog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}



@register.inclusion_tag('ablog/popular_posts.html')
def get_most_popular_posts(count=5):
    popular_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'popular_posts':popular_posts}

