from django.contrib.auth.models import User
from django.db import models


class Topics(models.Model):
    name = models.CharField('موضوع', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'موضوع'
        verbose_name_plural = 'موضوعات'


class Quiz(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ForeignKey(Topics, on_delete=models.CASCADE, verbose_name='موضوع')
    title = models.CharField('عنوان کوییز', max_length=100, unique=True)
    description = models.TextField('شرح')
    total_score = models.IntegerField('بارم', default=20)
    created = models.DateTimeField('زمان بارگذاری', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کوییز'
        verbose_name_plural = 'کوییز ها'


class Question(models.Model):
    quiz_name = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='عنوان کوییز')
    question_text = models.TextField('صورت سوال')
    score = models.IntegerField('بارم', default=0)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'


class Answer(models.Model):
    quiz_name = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='عنوان کوییز', null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='سوال')
    answer = models.CharField('جواب', max_length=150)
    is_correct = models.BooleanField('درست/غلط', default=False)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'جواب'
        verbose_name_plural = 'جواب ها'


class Participants(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نام دانش آموز')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='کوییز')
    total_score = models.IntegerField('نمره ی کسب شده', default=0)
    date = models.DateTimeField('زمان برگزاری', auto_now_add=True)

    is_finished = models.BooleanField('پایان یافته/نیافته', default=False)

    def __str__(self):
        return self.quiz.title

    class Meta:
        verbose_name = 'دانش آموز'
        verbose_name_plural = 'دانش آموزان'