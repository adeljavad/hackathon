from django.db import models
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

User_Type= ((1,'کاربر عادی'),
            (2, 'کارشناس'),
            (3, 'مدیر')
                       )


class Pepole(models.Model):
    # reg_phone_id=models.BigIntegerField( help_text="سریال")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('owner'), null=True,
                              default=1)
    user_type = models.IntegerField(default=0, null=True, verbose_name="وضعیت ارسال", choices=User_Type)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,
                                default=1, help_text="کد شرکت", verbose_name='کد شرکت')
    groupName = models.ForeignKey(GroupPhone, on_delete=models.CASCADE, verbose_name='نام گروه', null=True, default=1)
    phone_number = models.CharField(max_length=15, verbose_name="شماره موبایل")
    first_name = models.CharField(null=True,max_length=30, verbose_name="نام")
    last_name = models.CharField(null=True,max_length=30, verbose_name="نام خانوادگی")
    user_id = models.IntegerField(default=0, null=True, verbose_name="آی دی کاربر")
    access_hash = models.CharField(max_length=30, null=True, verbose_name="کد دسترسی")
    permission = models.BooleanField(help_text="تنظیم دریافت پیام کاربر",
                                     verbose_name="آیا برای کاربر پیام برود")  # permission
    province = models.CharField(null=True, max_length=30, verbose_name="استان")
    group = models.IntegerField(null=True, default=0, verbose_name="گروه")
    sent_status = models.IntegerField(null=True, default=0, verbose_name="وضعیت حضور در بله")
    create_date = models.DateTimeField(null=True, verbose_name='زمان ایجاد')
    submission_date = models.DateTimeField(null=True, verbose_name='date published')
    sync = models.IntegerField(default=0, null=True, verbose_name='هماهنگی کلاینت با سرور')
    Code_Melli = models.CharField(max_length=10, help_text="کد ملی", verbose_name='کد ملی')

    # objects = models.Manager()
    # phone_count = PhoneCountManager()

    def __str__(self):
        return str(self.user_id) #self.phone_number+','+str(

    class Meta:
        managed: True
        verbose_name = 'تلفن'
        verbose_name_plural = 'لیست تلفنها'
