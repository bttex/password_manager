# Generated by Django 5.1.4 on 2024-12-30 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passwords', '0005_rename_login_password_encrypted_password_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='password',
            old_name='site',
            new_name='service_name',
        ),
    ]