from django.db import models
from django.utils import timezone
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from PIL import Image
from django.dispatch import receiver
import math



class Updates(models.Model):
    title = models.CharField(max_length=32)
    subtitle = models.CharField(max_length=128)
    short_title = models.CharField(max_length=16)
    shord_desc = models.CharField(max_length=64)
    context = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


    @property
    def datetime(self):
        return f'publicado {self.data} e editado as {self.updated}'


    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        return super().save(*args, **kwargs)






class  Post(models.Model):
    CATEGORY_CHOICES = (
        ("1", "Programming/Technology"),
        ("2", "Health/Fitness"),
        ("3", "Personal"),
        ("4", "Fashion"),
        ("5", "Food"),
        ("6", "Travel"),
        ("7", "Business"),
        ("8", "Art"),
        ("9", "Other"),
    )

    category = models.CharField(
        max_length = 20,
        choices = CATEGORY_CHOICES,
        default = '1',
        blank=True,
        null=True
        )
    slug = models.SlugField(max_length=200, unique=False, editable=False, blank=True, null=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank= True)
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=255)
    short_title = models.CharField(max_length=32)
    short_desc = models.CharField(max_length=128)
    context = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    read_count = models.IntegerField(default=0, editable=False)
    read_time = models.IntegerField(default=0, editable=False)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    #tags = models.ManyToManyField(TagDict, blank=True)

    @property
    def datetime(self):
        return f'publicado {self.data} e editado as {self.updated}'

    def to_dict(self):
        post_dict = {
            'category': self.category,
            'slug': self.slug,
            'author': str(self.author),
            'title': self.title,
            'subtitle': self.subtitle,
            'short_title': self.short_title,
            'short_desc': self.short_desc,
            'context': self.context,
            'created_on': self.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_on': self.updated_on.strftime('%Y-%m-%d %H:%M:%S'),
            'read_count': self.read_count,
            'read_time': self.read_time,
            'likes': [str(user) for user in self.likes.all()],
            'image': str(self.image),
        }
        return post_dict

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('blog:post', kwargs={"slug":self.slug})

    def get_like_url(self):
        return reverse('blog:post', kwargs={"slug":self.slug})

    def get_api_like_url(self):
        return reverse('blog:post', kwargs={"slug":self.slug})

def count_words(s):
    return len(s.split(" "))

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)
    return int(read_time_min)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance.context:
        instance.read_time = get_read_time(instance.context)

pre_save.connect(pre_save_post_receiver, sender=Post)


class Analize(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="analizes")


    def __str__(self):
        return f"analize da publicação '{self.post}' "


class FavouritePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_image = models.ImageField(default='default.jpeg', upload_to ='profile_pics', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)