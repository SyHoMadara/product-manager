from django.contrib import admin
from applications.product.models import *

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
