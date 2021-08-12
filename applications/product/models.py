import uuid

from django.db import models, DatabaseError
from mptt.fields import TreeForeignKey

from src import project_model_base
from django.utils.translation import gettext_lazy as _


class ProductCategory(project_model_base.ProjectAbstractCategoryBase):
    parent = TreeForeignKey(
        'ProductCategory',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.PROTECT
    )


class ProductBrand(project_model_base.ProjectAbstractCategoryBase):
    parent = TreeForeignKey(
        'ProductBrand',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.PROTECT
    )


class Product(project_model_base.ProjectAbstractModelBase):
    id = models.UUIDField(_('UUID'), default=uuid.uuid4, editable=False, primary_key=True)
    slug = models.SlugField(_('slug'), unique=True, allow_unicode=True, blank=True)
    title = models.CharField(_('title'), max_length=50, blank=False)
    wight = models.FloatField(_('wight'), null=True, blank=True)
    cost = models.DecimalField(_('cost'), decimal_places=0, max_digits=12, default=0)
    deleted = models.BooleanField(_('deleted'), default=False)
    image = models.ImageField(
        _('image'),
        upload_to='products/',
        null=True,
        blank=True,
    )
    description = models.CharField(
        _('description'),
        max_length=400,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.PROTECT,
    )

    brand = models.ForeignKey(
        'ProductBrand',
        on_delete=models.PROTECT,
    )

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # create slug
        self.slug = f'{self.id.__str__()}'
        # set default description
        if not self.description or self.description == "":
            self.description = f'{self.title} you can pay for it {self.cost.__str__()}$'
        if self.category.is_root:
            raise DatabaseError("Product can not belong to a root category")
        # deploy changes if product deleted
        self.deploy_deleted_settings()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title
