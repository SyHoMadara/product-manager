import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from account.models import User


class ProductCategory(MPTTModel):
    name = models.CharField(max_length=200)
    id = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, primary_key=True)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    is_root = models.BooleanField(default=False)
    parent = TreeForeignKey(
        'ProductCategory',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('name', 'parent')
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        # create slug with self.name and parents names recursively
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        self.slug = '_'.join(list(map(slugify, full_path[::-1])))  # digital-and-tools/laptop
        # check that doesn't exist with this name and user name
        for category in ProductCategory.objects.all():
            if category.slug == self.slug:
                self.id = category.id
        # set is_root value
        self.is_root = not bool(self.parent)
        super().save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' / '.join(full_path[::-1])  # Digital and Tools/Laptop


class Product(models.Model):
    id = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, editable=False, primary_key=True)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    title = models.CharField(max_length=50, blank=False)
    cost = models.DecimalField(decimal_places=0, max_digits=12, default=0)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name='Image',
        upload_to='products/',
        null=True,
        blank=True,
    )
    description = models.CharField(
        max_length=400,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'ProductCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # create slug
        self.slug = f'{self.id.__str__()}'
        # set default description
        if not self.description or self.description == "":
            self.description = f'{self.title} you can pay for it {self.cost.__str__()}$'
        # set default category
        if not self.category:
            self.category = ProductCategory.objects.get(slug='another')

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title
