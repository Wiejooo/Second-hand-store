from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


class Clothes(models.Model):
    SIZE = [
        (0, "XS"),
        (1, "S"),
        (2, "M"),
        (3, "L"),
        (4, "XL"),
        (5, "XXL"),
    ]
    GEN = [
        (0, "Kobieta"),
        (1, "Mężczyzna"),
        (2, "Dziecko"),
    ]
    CATEGORY = [
        ("S", "Shirt"),
        ("SW", "Sport wear"),
        ("OW", "Outwear"),
    ]
    LABEL = [
        ("P", "primary"),
        ("S", "secondary"),
        ("D", "danger"),
    ]

    name = models.CharField(max_length=64)
    category = models.CharField(choices=CATEGORY, max_length=2)
    label = models.CharField(choices=LABEL, max_length=1)
    size = models.PositiveSmallIntegerField(choices=SIZE)
    price = models.IntegerField()
    description = models.CharField(max_length=264, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GEN)
    img = models.ImageField(upload_to="imgs", null=True, blank=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    item = models.ForeignKey(Clothes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
