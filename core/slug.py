from django.utils.text import slugify


def generate_unique_slug(model_class, source_text, slug_field='slug', instance=None):
    """Generate a unique slug for a model instance."""
    base_slug = slugify(source_text) or 'item'
    slug = base_slug
    counter = 1

    while True:
        qs = model_class.objects.filter(**{slug_field: slug})
        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)
        if not qs.exists():
            return slug
        slug = f'{base_slug}-{counter}'
        counter += 1
