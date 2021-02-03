# Generated by Django 3.1.6 on 2021-02-01 18:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import polls.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='start date')),
                ('end_date', models.DateTimeField(default=polls.models.in_two_days, verbose_name='end date')),
                ('description', models.TextField(default='something')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
            ],
        ),
    ]
