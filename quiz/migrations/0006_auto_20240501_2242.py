# Generated by Django 3.2.25 on 2024-05-01 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0005_question_is_checked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='participant_score',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='participants',
        ),
        migrations.AddField(
            model_name='quiz',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.IntegerField(default=0, verbose_name='نمره ی کسب شده')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='زمان برگزاری')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz', verbose_name='کوییز')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نام دانش آموز')),
            ],
        ),
    ]