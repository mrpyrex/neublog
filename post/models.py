from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


class PostCategory(models.Model):
    cat_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    cat_desc = models.TextField()

    class Meta:
        verbose_name = 'postcategory'
        verbose_name_plural = 'postcategories'

    def __str__(self):
        return self.cat_title

    def get_absolute_url(self):
        return reverse('post:category', args=[self.slug])


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumb = models.ImageField(blank=True, null=True, upload_to='images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    category = models.ForeignKey(
        PostCategory, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.content[0:120] + '...'

    def get_absolute_url(self):
        return reverse('post:post-detail', kwargs={'slug': self.slug})

    tags = TaggableManager()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug
