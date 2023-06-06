from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class MetaTagCompany(models.Model):
    company_name = models.CharField(max_length=255)
    meta_tag_name = models.CharField(_("Nome"), max_length=255)
    meta_tag_property = models.CharField(_("Property"), max_length=255, default="property")
    meta_tag_content = models.CharField(_("Content"), max_length=255, default="content")
    
    def __str__(self):
        return f"{self.company_name}"


class MetaTag(models.Model):
    name = models.ForeignKey(MetaTagCompany, on_delete=models.CASCADE)
    content = models.CharField(_("Conteúdo"), max_length=255)

    class Meta:
        verbose_name = _("Meta tag")
        verbose_name_plural = _("Meta tags")

    def __str__(self):
        return self.content


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=500,unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_tags = models.ManyToManyField(MetaTag, blank=True)



    @property
    def metatags(self):
        return len(self.meta_tags.all())
    

    @property
    def views(self):
        if "_views" in dir(self):
            return len(self._views.all())
        return 0
    


    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title + f"{self.pk} |{self.metatags}"

    def get_absolute_url(self):
        return reverse('page_detail', args=[str(self.slug)])


from django.contrib.auth.models import User

class PageView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="_views")

