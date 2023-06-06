from django.contrib import admin
from .models import (Page,
MetaTagCompany,
MetaTag,

)
# Register your models here.
admin.site.register(Page)
admin.site.register(MetaTagCompany)
admin.site.register(MetaTag)