import markdown
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.


class Tags(models.Model):
    tag = models.SlugField(max_length=100)

    def __str__(self):
        return self.tag

    def get_absoulute_url(self):
        return reverse('blog:tag-detailview', kwargs={'slug':self.tag})

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_image', blank=True)
    profile_name = models.CharField(blank=True, max_length=50)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.profile_name


class Banner(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.TextField()
    slide = models.ImageField(null=False, blank=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post')
    content = RichTextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    draft = models.BooleanField(default=True)
    read_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    published = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    image = models.ImageField(null=True, blank=True, upload_to='image')
    tags = models.ManyToManyField('Tags')
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    post_views = models.IntegerField(default=0,null=True,blank=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("details", kwargs={"id": self.id})



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mob = models.CharField(max_length=12)
    mess = models.TextField()
    time = models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comm = models.TextField()

class SubComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    sub_com_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comm = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class Join(models.Model):
    """Email for subscribing confirmation"""
    email = models.EmailField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email








