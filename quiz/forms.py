from django import forms
from quiz.models import Quiz, Topics, Question, Answer


class QuizForm(forms.Form):

    topics = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'موضوع'}),
        label='موضوع'
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'عنوان کوییز'}),
        label='عنوان کوییز'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'توضیحات'}),
        label='توضیحات'
    )

    total_score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'بارم'}),
        label='بارم'
    )

    def clean_topics(self):
        topics = self.cleaned_data.get('topics')
        if not Topics.objects.filter(name=topics).exists():
            Topics.objects.create(name=topics)
        topic = Topics.objects.get(name=topics)
        return topic

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Quiz.objects.filter(title=title).exists():
            raise forms.ValidationError('این عنوان قبلا ثبت شده است')
        return title


class QuestionForm(forms.Form):

    question_text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'صورت سوال'}),
        label='صورت سوال'
    )

    score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'بارم'}),
        label='بارم'
    )

    def clean_question_text(self):
        text = self.cleaned_data.get('question_text')
        if Question.objects.filter(question_text=text).exists():
            raise forms.ValidationError('این سوال قبلا ثبت شده است')
        return text


class AnswerForm(forms.Form):

    answer = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'جواب'}),
        label='جواب'
    )

    is_correct = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label='درست/غلط',
        required=False
    )

