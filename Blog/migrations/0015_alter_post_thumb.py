# Generated by Django 3.2.7 on 2022-02-26 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0014_alter_post_subheading'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Thumb',
            field=models.ImageField(blank=True, default='pass.jpg', upload_to=''),
        ),
    ]