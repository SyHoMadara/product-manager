import uuid

from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
    models records cannot be deleted.
"""


class ProjectAbstractModelBase(models.Model):
    deleted = models.BooleanField(_('deleted'), default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        raise NotImplementedError

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        raise NotImplementedError


"""
    each slug of objects is uniq if not you'll get error.
"""


class ProjectAbstractCategoryBase(MPTTModel):
    name = models.CharField(max_length=200, unique=True)
    id = models.UUIDField(_('UUID'), default=uuid.uuid4, primary_key=True)
    slug = models.SlugField(_('slug'), unique=True, allow_unicode=True, blank=True)
    is_root = models.BooleanField(_('is root'), default=False)
    deleted = models.BooleanField(_('deleted'), default=False)

    """
    class_name = str(type(self).__name__)
    self.parent = TreeForeignKey(
        class_name,
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )
    """

    class Meta:
        abstract = True

    # setting up dynamic fields.
    def __init__(self, *args, **kwargs):

        # setting class Meta
        self.Meta.unique_together = ('name', 'parent')

        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # create slug with self.name and parents names recursively
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        self.slug = '_'.join(list(map(slugify, full_path[::-1])))  # digital-and-tools_laptop
        # check that doesn't exist with this name and user name
        for obj in self.objects.all():
            if obj.slug == self.slug and obj.id != self.id:
                raise ValueError("there is another %s object with same parent / name" % type(self).__name__)
        # set is_root value
        self.is_root = not bool(self.parent)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' / '.join(full_path[::-1])  # Huawei / Xiaomi
