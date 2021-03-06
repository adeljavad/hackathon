# Generated by Django 2.1.7 on 2019-03-13 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pepole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(1, 'کاربر عادی'), (2, 'کارشناس'), (3, 'مدیر')], default=0, null=True, verbose_name='وضعیت ارسال')),
                ('phone_number', models.CharField(max_length=15, verbose_name='شماره موبایل')),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='نام')),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='نام خانوادگی')),
                ('user_id', models.IntegerField(default=0, null=True, verbose_name='آی دی کاربر')),
                ('owner', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'لیست کاربرها و متخصصین',
            },
        ),
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qa_type', models.IntegerField(choices=[(1, 'سئوال'), (2, 'جواب'), (3, 'سایر')], default=0, null=True, verbose_name='نوع سئوال ')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('content', models.CharField(max_length=30, null=True, verbose_name='محتوا')),
                ('category', models.CharField(max_length=30, null=True, verbose_name='گروه سئوال')),
                ('ref', models.IntegerField(default=0, null=True, verbose_name='ارجاع')),
                ('owner', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'سئوال',
                'verbose_name_plural': 'سئوال و جواب',
            },
        ),
    ]
