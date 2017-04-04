from django.contrib import admin
# from app_purly.models import ShortBase, Link
from app_purly.models import Link


# class ShortBaseAdmin(admin.ModelAdmin):
#     list_display = ('url_prefix', 'pub_date', 'purpose')
#     ordering = ('-pub_date',)
#
# admin.site.register(ShortBase, ShortBaseAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('pub_date','short_base','short_code','canonical_url','pub_user','purpose','hit_count','tracking_type')
    ordering = ('-pub_date',)

    # def save(self, *args, **kwargs):
    #     if not self.subject_init:
    #         self.subject_init = self.subject_initials()
    #     super(Subject, self).save(*args, **kwargs)

admin.site.register(Link, LinkAdmin)
