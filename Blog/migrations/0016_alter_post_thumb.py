# Generated by Django 3.2.7 on 2022-02-26 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0015_alter_post_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Thumb',
            field=models.ImageField(blank=True, default='pass.jpg', null=True, upload_to=''),
        ),
    ]