# -*- coding: utf-8 -*-


from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from filebrowser.fields import FileBrowseField
from django_comments.models import Comment
from image_cropping.fields import ImageRatioField


class EditableMedia(models.Model):
    # Metadata
    created_date = models.DateTimeField(
        verbose_name="Publiseringsdato",
        auto_now_add=True,
        null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Opprettet av",
        related_name="%(class)s_created",
        editable=False,
        blank=True,
        null=True)
    last_changed_date = models.DateTimeField(
        verbose_name="Redigeringsdato",
        auto_now=True,
        null=True)
    last_changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Endret av",
        related_name="%(class)s_edited",
        editable=False,
        blank=True,
        null=True)

    class Meta:
        abstract = True


class Content(EditableMedia):

    # Bildeopplasting med resizing og cropping
    picture = models.ImageField(
        upload_to="news_pictures",
        null=True,
        blank=True,
        verbose_name="Bilde",
        help_text="Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.")
    cropping = ImageRatioField(
        'picture',
        '770x300',
        allow_fullsize=False,
        verbose_name="Beskjæring")

    # Slugs
    slug = models.SlugField(
        null=True,
        blank=True,
        help_text="Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres")

    allow_comments = models.BooleanField(
        blank=True,
        verbose_name="Tillat kommentarer",
        default=True,
        help_text="Hvorvidt kommentering er tillatt")

    # content_type is here so that we can know which subclass of Content/News this is. (Polymorphism)
    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    class Meta:
        abstract = True

    @models.permalink
    def get_absolute_url(self):
        """
        Finner URL ved å reversere navnet på viewen.
        Krever at navnet på viewet er gitt ved modellnavn_detail
        """
        return (self.content_type.model + "_detail", (), {
            'pk': self.pk,
            'slug': self.slug
        })

    def has_been_edited(self):
        return abs((self.last_changed_date - self.created_date).seconds) > 1

    def get_picture_url(self):
        return 'http://%s%s%s' % (Site.objects.get_current().domain, settings.MEDIA_URL, self.picture.name)

    def delete(self, *args, **kwargs):
        """
        Override default method, so related comments are also deleted
        """
        comments = Comment.objects.filter(object_pk=self.pk,
                                          content_type=self.content_type)
        comments.delete()
        super(Content, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Content, self).save(*args, **kwargs)


class AlbumImage(models.Model):
    file = FileBrowseField(
        max_length=100,
        verbose_name="Bildefil"
    )
    description = models.TextField(
        verbose_name="Bildetekst",
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return self.file.url

    def __str__(self):
        return self.file.url

    class Meta:
        verbose_name = "Albumbilde"
        verbose_name_plural = "Albumbilder"


class Album(EditableMedia):
    title = models.CharField(
        max_length=100,
        verbose_name="Albumtittel",
        blank=False,
        null=True
    )
    images = models.ManyToManyField(
        AlbumImage,
        verbose_name="Bilder",
    )

    VISIBILLITY_OPTIONS = (
        ('p', 'public'),
        ('u', 'users'),
        ('h', 'hidden')
    )

    visibillity = models.CharField(
        max_length=1,
        verbose_name="Synlighet",
        choices=VISIBILLITY_OPTIONS,
        default='h',
        blank=False
    )

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Album"

    def get_absolute_url(self):
        return reverse('album', kwargs={'pk': self.pk,'num': '0'})

    def is_visible(self, user=None):
        if self.visibillity != 'p':
            if self.visibillity != 'h' and user is not None:
                return user.is_authenticated()
            else:
                return False
        else:
            return True

    def __str__(self):
        return self.title
