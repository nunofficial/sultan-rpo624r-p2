import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from pytils.translit import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL иконки")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ad(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads', verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads', verbose_name="Категория")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ads', verbose_name="Город")
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(verbose_name="Цена (в тенге)", help_text="Укажите 0, если бесплатно")
    image = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL изображения товара")
    is_top = models.BooleanField(default=False, verbose_name="В топе")
    vip_requested = models.BooleanField(default=False, verbose_name="Заявка на VIP")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_moderated = models.BooleanField(default=False, verbose_name="Прошло модерацию")

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favorited_by')
    
    class Meta:
        unique_together = ('user', 'ad')

class Review(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='reviews', verbose_name="Объявление")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_left', verbose_name="Автор отзыва")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        verbose_name="Оценка (1-5)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.author} на {self.ad.title}"


class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField(max_length=500, verbose_name="URL баннера")
    link = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title