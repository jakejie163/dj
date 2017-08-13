from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/show_months.html')
def show_months_of_date():
    months_of_date = Post.published.datetimes('publish', 'month', 'DESC')
    return {'months_of_date': months_of_date}


@register.inclusion_tag('blog/post/side_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'side_posts': latest_posts}

@register.inclusion_tag('blog/post/side_posts.html')
def get_most_commented_posts(count=5):
    most_commented_posts = Post.published.annotate(
                total_comments=Count('comments')
                ).order_by('-total_comments')[:count]
    return {'side_posts': most_commented_posts}

@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
