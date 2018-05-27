from django.db import models
from django.utils import timezone
from hashids import Hashids
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class HashKeyBuilderMixin(object):
    hashid_builder = Hashids(salt='short salt', min_length=settings.SHORT_CODE_LENGTH)

    @staticmethod
    def decode_hashkey_to_id(hash_key):
        ids = HashKeyBuilderMixin.hashid_builder.decode(hash_key)
        return ids[0] if ids else None

    @property
    def hashkey(self):
        return HashKeyBuilderMixin.encode_id_to_hashkey(self.id)

    @staticmethod
    def encode_id_to_hashkey(id):
        return HashKeyBuilderMixin.hashid_builder.encode(id)


class TimeBaseModel(models.Model):
    created = models.DateTimeField(verbose_name=_(u'created_time'),
                                   default=timezone.now)

    updated = models.DateTimeField(verbose_name=_(u'updated_time'),
                                   auto_now=True)

    def updated_timestamp(self):
        return int(self.updated.strftime("%s")) if self.updated else 0

    def created_timestamp(self):
        return int(self.created.strftime("%s")) if self.created else 0

    class Meta:
        abstract = True


class ShortUrl(HashKeyBuilderMixin, TimeBaseModel):
    custom_url = models.CharField(max_length=32, verbose_name=u'custom_url', db_index=True)
    access_count = models.IntegerField(default=0, verbose_name=u'access_count')
    long_url = models.CharField(max_length=200, verbose_name=u'long_url')

    objects = models.Manager()

    class Meta:
        verbose_name = u'short_url'
        ordering = ('-created',)

