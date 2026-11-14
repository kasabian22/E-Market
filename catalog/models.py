from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.utils import CUSTOM_SLUG_ERROR, TITLE_SLUG_ERROR, generate_unique_slug, get_slug_base
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if not self.slug and self.name:
            self.slug = generate_unique_slug(
                Category, title=self.name, exclude_pk=self.pk
            )

        if not self.slug or not self.slug.strip():
            raise ValidationError(
                {'slug': 'Integrity guard: Category slug cannot be empty.'}
            )

        try:
            get_slug_base(self.name, self.slug)
        except ValidationError as error:
            message = error.messages[0] if error.messages else CUSTOM_SLUG_ERROR
            raise ValidationError(
                {'name' if message == TITLE_SLUG_ERROR else 'slug': message}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('category', 'name')
        ordering = ['name']
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_non_negative'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, title=self.name, exclude_pk=self.pk)

        if not self.slug or not self.slug.strip():
            raise ValidationError("Integrity guard: Product slug cannot be empty.")

        super().save(*args, **kwargs)