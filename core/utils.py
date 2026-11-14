import re
import uuid
from unidecode import unidecode
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

MIN_SLUG_CONTENT_LENGTH = 2
MAX_SLUG_BASE_LENGTH = 240
TITLE_SLUG_ERROR = f"The course title must contain at least {MIN_SLUG_CONTENT_LENGTH} letters or numbers."
CUSTOM_SLUG_ERROR = f"The slug must contain at least {MIN_SLUG_CONTENT_LENGTH} letters or numbers."


def contains_minimum_slug_content(value):
    """Return whether a title or normalized slug has enough letters/numbers."""
    return len(re.findall(r"[^\W_]", value or "")) >= MIN_SLUG_CONTENT_LENGTH


def normalize_custom_slug(value):
    """Convert a user-entered slug into the canonical ASCII URL form."""
    return slugify(unidecode((value or "").strip()))


def get_slug_base(title="", custom_slug=""):
    """Validate slug input and return its normalized base, before uniqueness suffixes."""
    if custom_slug and custom_slug.strip():
        base_slug = normalize_custom_slug(custom_slug)
        if not contains_minimum_slug_content(base_slug):
            raise ValidationError(CUSTOM_SLUG_ERROR)
        return base_slug

    if title and not contains_minimum_slug_content(title):
        raise ValidationError(TITLE_SLUG_ERROR)
    base_slug = extract_smart_base_slug(title)
    if title and not contains_minimum_slug_content(base_slug):
        raise ValidationError(TITLE_SLUG_ERROR)
    return base_slug

def extract_smart_base_slug(title):
    """
    Apply the 4 smart rules to generate a base slug from a course title:
    1. Pure English/ASCII -> standard slugify.
    2. Mixed Arabic + meaningful English phrase (2+ words of 2+ letters) -> English + numbers only.
    3. Pure Arabic / other languages -> transliterate everything via unidecode.
    4. Arabic + dependent numbers (e.g., Part 3) or short English letters (e.g., C, Ch 1) -> transliterate everything together.
    """
    if not title:
        return ""

    # Check if the title contains any non-ASCII characters (like Arabic)
    has_non_ascii = bool(re.search(r"[^\x00-\x7F]", title))

    if not has_non_ascii:
        # Pure English/ASCII title
        return slugify(title)

    # Extract meaningful English words (2 or more letters)
    meaningful_english_words = re.findall(r"[a-zA-Z]{2,}", title)

    if len(meaningful_english_words) >= 2:
        # Rule 1: Meaningful English phrase exists -> extract all English words and numbers only
        english_and_numbers = re.findall(r"[a-zA-Z0-9]+", title)
        base_slug = slugify(" ".join(english_and_numbers))
    else:
        # Rules 2, 3, 4: Pure Arabic, or Arabic with numbers/short dependent English tokens
        base_slug = slugify(unidecode(title))

    return base_slug


def generate_unique_slug(instance_or_model, title="", custom_slug="", exclude_pk=None, validated_base_slug=None):
    """
    Generate a guaranteed non-empty, unique slug for a Course.
    Prioritizes custom_slug if provided; otherwise derives it from title.
    """
    base_slug = validated_base_slug if validated_base_slug is not None else get_slug_base(title, custom_slug)

    # Ultimate fallback if input was only symbols like "???" generate random slug
    if not base_slug:
        base_slug = f"course-{uuid.uuid4().hex[:8]}"

    # Determine the Model class and the primary key to exclude (if he wants to update it)
    if isinstance(instance_or_model, models.Model):
        ModelClass = instance_or_model.__class__
        exclude_pk = instance_or_model.pk
    else:
        ModelClass = instance_or_model

    qs = ModelClass.objects.all()
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)


    # Leave room for a numeric uniqueness suffix within the model's 250 character limit.
    base_slug = base_slug[:MAX_SLUG_BASE_LENGTH].strip('-')
    

    # Fetch all matching slugs in one single SQL query
    existing_slugs = set(
        qs.filter(
            models.Q(slug=base_slug) | models.Q(slug__regex=rf'^{re.escape(base_slug)}-\d+$')
        ).values_list('slug', flat=True)
    )
    if base_slug not in existing_slugs:
        return base_slug
    
    counter = 1
    while f"{base_slug}-{counter}" in existing_slugs:
        counter += 1
    
    return f"{base_slug}-{counter}"

# =================================================================================================================== #

def paginate_queryset(request, queryset, per_page=9):
    """
    A helper function for paginating any QuerySet
    """
    # Initialize Paginator: Show 9 courses per page (3 rows x 3 columns)
    paginator = Paginator(queryset, per_page)

    # Get the requested page number from the URL query string (e.g., ?page=2)
    page_number = request.GET.get('page', 1)

    # get_page() safely handles invalid strings (like ?page=abc) or out-of-range numbers
    return paginator.get_page(page_number)



# =================================================================================================================== #


