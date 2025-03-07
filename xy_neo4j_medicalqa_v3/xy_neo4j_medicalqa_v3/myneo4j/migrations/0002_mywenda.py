# Generated by Django 3.2.7 on 2023-01-25 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myneo4j', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyWenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='问题')),
                ('anster', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='答案')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '问答信息',
                'verbose_name_plural': '问答信息',
                'ordering': ['-id'],
            },
        ),
    ]
