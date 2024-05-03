from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import QuizForm, QuestionForm, AnswerForm
from .models import Topics, Quiz, Question, Answer, Participants


def home(request):
    topics = Topics.objects.all()
    quizes = Quiz.objects.all().order_by('-created')

    context = {'topics': topics, 'quizes': quizes}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def quiz(request, pk):
    quiz = Quiz.objects.get(title=pk)
    questions = Question.objects.filter(quiz_name=quiz)

    a = Participants.objects.filter(student=request.user, quiz=quiz)
    c = a.filter(is_finished=True)
    if a.exists():
        if c:
            return HttpResponse('قیلا در این آزمون شرکت کرده اید')
    else:
        Participants.objects.create(student=request.user, quiz=quiz)

    context = {'questions': questions, 'quiz': quiz}
    return render(request, 'quiz/quiz.html', context)


@login_required(login_url='login')
def question(request, pk):
    question = Question.objects.get(question_text=pk)
    answers = Answer.objects.filter(question=question)

    context = {'question': question, 'answers': answers}
    return render(request, 'quiz/answers.html', context)


@login_required(login_url='login')
def answer(request, pk, name):
    answer = Answer.objects.get(answer=pk, question__question_text__exact=name)
    question = Question.objects.get(question_text=answer.question)
    quiz = Quiz.objects.get(title=answer.quiz_name)
    participants = Participants.objects.get(student=request.user, quiz=quiz)
    if request.method == 'POST':
        if answer.is_correct:
            participants.total_score += question.score
            participants.save()
            return redirect('quiz', quiz.title)
        return redirect('quiz', quiz.title)

    return redirect('quiz', quiz.title)


@login_required(login_url='login')
def finish(request, pk):
    participants = Participants.objects.get(student=request.user, quiz__title=pk)
    if request.method == 'POST':
        participants.is_finished = True
        participants.save()
        return redirect('home')


@login_required(login_url='login')
def createQuiz(request):
    form = QuizForm(request.POST or None)
    if form.is_valid():
        host = request.user
        topics = form.cleaned_data.get('topics')
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        total_score = form.cleaned_data.get('total_score')
        quiz = Quiz.objects.create(host=host, topics=topics, title=title, description=description, total_score=total_score)
        return redirect('create_question', quiz.title)
    return render(request, 'quiz/create_quiz.html', {'form': form, 'page': 'create_quiz'})


@login_required(login_url='login')
def createQuestion(request, pk):
    form = QuestionForm(request.POST or None)
    quiz = Quiz.objects.get(title=pk)

    if form.is_valid():
        quiz_name = quiz
        question_text = form.cleaned_data.get('question_text')
        score = form.cleaned_data.get('score')
        Question.objects.create(quiz_name=quiz_name, question_text=question_text, score=score)
        question = Question.objects.get(quiz_name=quiz, question_text=question_text)
        return redirect('create_answer', question.question_text)
    return render(request, 'quiz/create_quiz.html', {'page': 'create_question', 'form': form, 'quiz': quiz})


@login_required(login_url='login')
def createAnswer(request, pk):
    answer_form = AnswerForm(request.POST or None)
    question = Question.objects.get(question_text=pk)
    quiz = Quiz.objects.get(title=question.quiz_name)
    if answer_form.is_valid():
        answer = answer_form.cleaned_data.get('answer')
        if Question.objects.filter(question_text=answer):
            raise ValidationError('این جواب قبلا برای این سوال ثبت شده است')
        is_correct = answer_form.cleaned_data.get('is_correct')
        Answer.objects.create(quiz_name=quiz, question=question, answer=answer, is_correct=is_correct)
        return redirect('create_answer', question.question_text)
    return render(request, 'quiz/create_answer.html', {'answer_form': answer_form, 'quiz': quiz})