"""
Models for album app
"""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

from mptt.models import MPTTModel, TreeForeignKey

from content.models import TimeStamped, BaseImageModel


class AlbumImage(BaseImageModel):
    """
    An album image.

    Each album image is associated with a single album
    """

    description = models.TextField(
        verbose_name="Bildetekst",
        blank=True,
        null=True
    )

    album = models.ForeignKey(
        'album.Album',
        verbose_name="Album",
        related_name="images",
        null=True,
        on_delete=models.CASCADE
    )

    num = models.PositiveIntegerField(
        verbose_name="Nummer",
        blank=True,
        null=True,
        editable=False
    )

    is_display_image = models.BooleanField(
        verbose_name="Er visningbilde",
        help_text="Bildet som vises i listen over album",
        default=False,
    )

    def get_absolute_url(self):
        """Get canonical url for image"""
        return reverse('album_image',
                       kwargs={"pk": self.album.id, "num": self.num+1})

    @property
    def is_published(self):
        """Check is parent album is hidden (meaning unpublished)"""
        return self.album.visibility != 'h'

    class Meta:
        verbose_name = "Albumbilde"
        verbose_name_plural = "Albumbilder"
        db_table = "content_albumimage"


class Album(MPTTModel, TimeStamped):
    """
    Model representing an album which is a collection of images.
    """
    title = models.CharField(
        max_length=100,
        verbose_name="Albumtittel",
        blank=False,
        null=True
    )

    VISIBILITY_OPTIONS = (
        ('p', 'public'),
        ('u', 'users'),
        ('h', 'hidden')
    )

    visibility = models.CharField(
        max_length=1,
        verbose_name="Synlighet",
        choices=VISIBILITY_OPTIONS,
        default='h',
        blank=False
    )

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Album"
        db_table = "content_album"

    def get_absolute_url(self):
        """Return canonical url for album"""
        return reverse('album', kwargs={'pk': self.pk})

    def is_visible(self, user=AnonymousUser()):
        """
        Return whether this album is visible for the supplied user.

        If visibility is 'p' then all users can see the album.
        If visibility is 'u' all logged in users can see the album.
        All logged in users with the permission to change albums can see the album.
        """
        return (self.visibility == 'p'
                or self.visibility == 'u' and user.is_authenticated
                or user.has_perm('content.change_album'))

    @property
    def first(self):
        """Get the image which is considered to be the first in the album"""
        return self.images.order_by('-is_display_image', 'num').first()

    def __str__(self):
        return self.title
