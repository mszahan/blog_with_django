from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('cat_details', args= [self.name])



#need to figure out this thing as well
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    SATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True,null= True, related_name='post_cat')
    # body = models.TextField()
    # body = RichTextField(blank=True, null=True)
    body = RichTextUploadingField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=SATUS_CHOICES, default='draft')


#I don't understand........... now I understatand
    objects = models.Manager()
    published = PublishedManager()

    tags = TaggableManager()



    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', args= [self.pk, self.slug])
    




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=254)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"




# class Comment(models.Model):
#     post = models.ForeignKey(Post, related_name='comments')
#     name = models.CharField(max_length=80)
#     email = models.EmailField(max_length=200, blank=True)
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     # manually deactivate inappropriate comments from admin site
#     active = models.BooleanField(default=True)
#     parent = models.ForeignKey('self', null=True, blank=True, related_name='replies')

#     class Meta:
#         # sort comments in chronological order by default
#         ordering = ('created',)

#     def __str__(self):
#         return 'Comment by {}'.format(self.name)














