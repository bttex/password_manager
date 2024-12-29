# Generated by Django 5.1.4 on 2024-12-29 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otp_totp', '0003_add_timestamps'),
        ('passwords', '0003_remove_password_encrypted_password_password_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomTOTPDevice',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('otp_totp.totpdevice',),
        ),
    ]
