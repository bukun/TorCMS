# import markdown
# from django.db import models
# from django.contrib.auth import get_user_model
# from base.models import basemodel
# from django.contrib.sites.models import Site
#
# class iga_staff(basemodel):
#     name = models.CharField(blank=True, null=False, max_length=255, verbose_name="人员名")
#     sites = models.ManyToManyField(Site, blank=True, related_name='iga_staff', verbose_name='Site')
#
#     def __str__(self):
#         return self.name
#
#     class Meta(basemodel.Meta):
#         db_table = 'iga_staff'
#         verbose_name = "人员"
#         verbose_name_plural = verbose_name
