import re, hashlib, binascii, random
from django.db import models
from django.db.models.signals import pre_save


# class ShortBase(models.Model):
#     url_prefix = models.URLField(primary_key=True)
#     pub_date = models.DateTimeField(auto_now=True)
#     purpose = models.CharField(max_length=252, blank=True)
#
#     def __str__(self):
#         return self.url_prefix

def random_5digits():
    return random.randint(10000, 99999)


class Link(models.Model):
    # @TODO consider ?? moving all of these hard-coded lists/choices over into settings.py
    BASE_CHOICES = (
        ("http://2s.pe/","2s.pe"),
        ("http://4s.pe/","4s.pe"),
        ("http://go.spe.org/","GO.spe.org"),
        ("http://www.spe.org/go/","www.SPE.org/go"),
        ("http://go.iptcnet.org/","GO.IPTCnet.org"),
        ("http://www.iptcnet.org/go/","www.IPTCnet.org/go"),
        ("http://go.otcnet.org/","GO.OTCnet.org"),
        ("http://www.otcnet.org/go/","www.OTCnet.org/go"),
        ("http://go.otcbrasil.org/","GO.OTCBrasil.org"),
        ("http://www.otcbrasil.org/go/","www.OTCBrasil.org/go"),
        ("http://go.otcasia.org/","GO.OTCAsia.org"),
        ("http://www.otcasia.org/go/","www.OTCAsia.org/go"),
    )
    BASE_DEFAULT = 'http://www.spe.org/go/'

    PROPERTY_IDS = (
        ("spe.org","UA-39288943-2"),
        ("iptcnet.org","xUA-IPTC"),
        ("otcnet.org","xUA-OTC"),
        ("otcbrasil.org","xUA-OTCB"),
        ("otcasia.org","xUA-OTCA"),
        ("2s.pe","xUA-2"),
        ("4s.pe","xUA-4"),
    )

    MEDIUM_CHOICES = (
        ("s", "Server-side"),
        ("c", "Client-side"),
        ("n", "No tracking"),
    )
    SOURCE_CHOICES = (
        ("s", "Server-side"),
        ("c", "Client-side"),
        ("n", "No tracking"),
    )

    TRACKING_CHOICES = (
        ("s", "Server-side"),
        ("c", "Client-side"),
        ("n", "No tracking"),
    )
    TRACKING_DEFAULT = 'c'

    # ensure uniqueness at the proper level: a composite, effectively Link.short_url()
    class Meta:
        unique_together = (('short_base', 'short_code'),)

    short_base = models.URLField(help_text="Please select which prefix to use for your short URL", max_length=28, choices=BASE_CHOICES, default=BASE_DEFAULT, db_index=True)
    short_code = models.SlugField(help_text="Please choose the suffix for your short URL", max_length=18, db_index=True)
    short_url_hash = models.SlugField(max_length=96, primary_key=True, editable=False)
    canonical_url = models.URLField(help_text="Please provide the standard (canonical) version of your long URL", verbose_name='Canonical URL')
    accounting_code = models.CharField(help_text="Optional: the accounting code to associate with this short URL, for time and expenses, e.g., EZLabor code", max_length=18, blank=True)
    tracking_string = models.CharField(max_length=252, blank=True)
    tracking_type = models.CharField(help_text="Please select how to track the usage of your short URL", max_length=1, choices=TRACKING_CHOICES, default=TRACKING_DEFAULT)
    pub_date = models.DateTimeField(help_text="When this short URL was (last) published", auto_now=True, verbose_name='Published')
    pub_user = models.CharField(help_text="Who (last) published this short URL", max_length=90, blank=True, verbose_name='Published By')
    purpose = models.CharField(help_text="Please specify the reason you are creating this short URL", max_length=252, blank=True)
    end_date = models.DateTimeField(help_text="When this campaign will end and this short URL will no longer be needed", blank=True, verbose_name='End Date')
    hit_count = models.IntegerField(help_text="How many times this short URL has already been used", default=0, editable=False)
    testing_date = models.DateTimeField(help_text="Only put a date and time here if this short URL is for testing purposes", blank=True, null=True, default=None, verbose_name='Timestamp if Testing')

    # generate a simple SHA256 hash of the short URL -- unsalted so client side could easily make the same hash if necessary
    # (this is for conflict-resistant slug purposes, not for security purposes)
    def hash_the_short_url(self):
        return binascii.hexlify(hashlib.sha256(str(self.short_url())).digest())

    # for any short URL, the short base is the URL prefix and the short code is the suffix
    def short_url(self):
        b = self.short_base is not None and self.short_base or ''
        c = self.short_code is not None and self.short_code or ''
        return b + c

    # return the number of characters (that someone would have to type) for a given short URL
    def short_url_chars(self):
        return len(re.sub('^http://','',self.short_url()))

    # return the long URL, i.e., what would show up in a redirection response "Location" header
    def long_url(self):
        if '#' in self.canonical_url:
            c = re.sub(r'#.*$', '', self.canonical_url.strip())
            f = "#" + re.sub(r'^.*#', '', self.canonical_url.strip())
        else:
            c = self.canonical_url.strip()
            f = ''

# TODO: only merge in the tracking_string here if the tracking_type is "c" for client-side tracking (do nothing for "s" or "n")
        if self.tracking_string == '':
            t = ''
        else:
            if '?' in c:
                tsep = '&'
            else:
                tsep = '?'
            t = tsep + self.tracking_string

        return c + t + f

    # determine whether or not the short base is one that integrates with EVA, automatically supporting an official event code as short code
    # def is_autohandling_event_codes(self):
    #     return (str(self.short_url()))

    # 61207 - not sure this is still needed...
    def redirect_target_url(self):
        # TODO: if the tracking_type is "s" for server-side tracking to fire, then make a request now
        return self.long_url()

    # override this model's save() method in order to build the primary key -- unsalted SHA256 of the whole short URL
    def save(self, *args, **kwargs):
        self.short_url_hash = self.hash_the_short_url()
        super(Link, self).save(*args, **kwargs)

    # use the whole short URL -- always unique, easily human-readable
    def __str__(self):
        return self.short_url()


# def build_composite_link_id(sender, instance, using):
#     instance.short_url_hash = instance.hash_the_short_url()
#
# pre_save.connect(build_composite_link_id, sender=Link)
