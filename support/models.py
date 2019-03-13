from django.db import models
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

User_Type = ((1, 'کاربر عادی'),
             (2, 'کارشناس'),
             (3, 'مدیر')
             )

Qa_Type = ((1, 'سئوال'),
           (2, 'جواب'),
           (3, 'سایر')
           )


class Pepole(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('owner'), null=True,
                              default=1)
    user_type = models.IntegerField(default=0, null=True, verbose_name="وضعیت ارسال", choices=User_Type)
    phone_number = models.CharField(max_length=15, verbose_name="شماره موبایل")
    first_name = models.CharField(null=True, max_length=30, verbose_name="نام")
    last_name = models.CharField(null=True, max_length=30, verbose_name="نام خانوادگی")
    user_id = models.IntegerField(default=0, null=True, verbose_name="آی دی کاربر")

    def __str__(self):
        return str(self.user_id)  # self.phone_number+','+str(

    class Meta:
        managed: True
        verbose_name = 'کاربر'
        verbose_name_plural = 'لیست کاربرها و متخصصین'


class QA(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('owner'), null=True,
                              default=1)
    qa_type = models.IntegerField(default=0, null=True, verbose_name="نوع سئوال ", choices=Qa_Type)
    title = models.CharField(max_length=100, verbose_name="عنوان")
    content = models.CharField(null=True, max_length=30, verbose_name="محتوا")
    category = models.CharField(null=True, max_length=30, verbose_name="گروه سئوال")
    ref = models.IntegerField(default=0, null=True, verbose_name="ارجاع")

    def __str__(self):
        return str(self.title)  # self.phone_number+','+str(

    class Meta:
        managed: True
        verbose_name = 'سئوال'
        verbose_name_plural = 'سئوال و جواب'


class Ticket(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('owner'), null=True,
                              default=1)
    user_id = models.ForeignKey(Pepole, on_delete=models.PROTECT,  null=True,   default=1, verbose_name="کد کاربر")
    tecn_id = models.IntegerField(default=1, null=True,  verbose_name="کد متخصص")
    qa_id = models.ForeignKey(QA, on_delete=models.PROTECT,  null=True,   default=1, verbose_name="شماره سئوال")
    create_date = models.DateField(null=True,  verbose_name="تاریخ ایجاد")
    ref = models.IntegerField(default=0, null=True, verbose_name="ارجاع")

    def __str__(self):
        return str(self.user_id)

    class Meta:
        managed: True
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت'

