from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    info = models.CharField(max_length=100, blank=True)
    quote = models.CharField(max_length=200, verbose_name="sitat", blank=True)
    author = models.CharField(max_length=100, verbose_name="forfatter", blank=True)
    created_date = models.DateTimeField(verbose_name="publiseringsdato", auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name="lagt til av")
    approved = models.BooleanField(verbose_name="godkjent")

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "sitat"
        verbose_name_plural = "sitat"

    def __unicode__(self):
        return self.quote
