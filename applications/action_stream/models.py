from django.db import models
from django.utils import timezone
from applications.account.models import User
from applications.product.models import Product
from django.utils.translation import gettext_lazy as _


class Action(models.Model):
    description = models.CharField(max_length=400, blank=False)
    date = models.DateTimeField(_('date action'), default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __init__(self, user: User, product: Product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        self.user = user
        self.date = timezone.now()
