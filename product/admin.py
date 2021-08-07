from django.contrib import admin
from product.models import *

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
