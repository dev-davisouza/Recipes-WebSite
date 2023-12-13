from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(blank=True, unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def _generate_unique_slug(self):
        """
        Generate an unique slug, adding a number in the end if necessary.
        """
        slug = slugify(self.title)
        counter = 1

        while Recipe.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{slug}-{counter}"
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        elif Recipe.objects.filter(slug=self.slug).exclude(id=self.id).exists():  # noqa
            # Se o slug já existe em outro objeto
            # (excluindo o próprio objeto sendo salvo),
            # precisamos gerar um novo slug único.
            self.slug = self._generate_unique_slug()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
