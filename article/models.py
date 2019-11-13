from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify
# Create your models here.

class ArticleColumn(models.Model):

    user = models.ForeignKey(User,related_name='article_column',on_delete=None)
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column

# class ArticleTag(models.Model):
#     author = models.ForeignKey(User,related_name="tag",on_delete=None)
#     tag = models.CharField(max_length=500)
#
#     def __str__(self):
#         return self.tag

class ArticlePost(models.Model):
    author = models.ForeignKey(User,related_name="article",on_delete=None)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn,related_name="article_column",on_delete=None)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(default=timezone.now())
    # users_like = models.ManyToManyField(User,related_name="article_like",blank=True)
    # article_tag = models.ManyToManyField(ArticleTag,related_name="article_tag",blank=True)

    class Meta:
        ordering = ("-updated",)
        index_together = (('id','slug',),)

    def __str__(self):
            return self.title

        #重写save方法
    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        return reverse("article:article_detail",args=[self.id,self.slug])

        # def get_url_path(self):
        #     return reverse("article:article_content",args=[self.id,self.slug])
