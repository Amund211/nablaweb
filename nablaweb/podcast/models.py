# -*- coding: utf-8 -*-

from django.db import models
from image_cropping.fields import ImageRatioField
from django.core.urlresolvers import reverse


def get_season_count():
    return Season.objects.count()


class Season(models.Model):
    number = models.IntegerField(
        verbose_name="Sesongnummer",
        unique=True,
    )

    banner = models.ImageField(
        upload_to="podcast/images",
        null=True,
        blank=True,
        verbose_name="Banner",
        help_text="Sesongbanner."
    )

    logo = models.ImageField(
        upload_to="podcast/images",
        null=True,
        blank=True,
        verbose_name="Logo",
        help_text="Podcastlogo."
    )

    def name(self):
        return "Sesong " + str(self.number)

    def get_absolute_url(self):
        return reverse('season_view', kwargs={'number': int(self.number)})

    def get_next(self):
        try:
            return Season.objects.get(number=int(self.number) + 1)
        except Season.DoesNotExist:
            return None

    def get_previous(self):
        try:
            return Season.objects.get(number=int(self.number) - 1)
        except Season.DoesNotExist:
            return None

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Sesong'
        verbose_name_plural = 'Sesonger'


class Podcast(models.Model):

    # Bildeopplasting med resizing og cropping
    image = models.ImageField(
        upload_to="news_pictures",
        null=True,
        blank=True,
        verbose_name="Bilde",
        help_text="Bilder som er større enn 300x300 px ser best ut. Du kan beskjære bildet etter opplasting.")
    cropping = ImageRatioField(
        'image',
        '300x300',
        allow_fullsize=False,
        verbose_name="Beskjæring",
        help_text="Bildet vises i full form på detaljsiden."
    )

    title = models.CharField(
        verbose_name='tittel',
        max_length=200,
        blank=False
    )
    description = models.TextField(
        verbose_name='beskrivelse',
        help_text='Tekst. Man kan her bruke <a href="http://en.wikipedis.org/wiki/Markdown\"target=\"_blank\">markdown</a> for å formatere teksten.',
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='publisert',
        auto_now_add=True,
        blank=False,
        null=True,
    )
    file = models.FileField(
        upload_to='podcast',
        blank=False,
        verbose_name='lydfil',
        help_text='Filformat: MP3'
    )

    view_counter = models.IntegerField(
        editable=False,
        default=0
    )

    is_clip = models.BooleanField(
        default=False,
        verbose_name="Er lydklipp",
        help_text="Lydklipp blir ikke vist sammen med episodene."
    )

    season = models.ForeignKey(
        'Season',
        verbose_name="Sesong",
        null=True,
        blank=True
    )

    def add_view(self):
        self.view_counter += 1
        self.save()

    def get_absolute_url(self):
        return reverse('podcast_detail', kwargs={'podcast_id': self.id})

    def get_short_description(self):
        description = str(self.description)
        if description.__len__() > 280:
            description = description[:280] + "..."
        return description

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcast'
        ordering = ["-pub_date"]
