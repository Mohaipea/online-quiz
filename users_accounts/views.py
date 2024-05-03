from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegistrationForm, EditProfileForm
from quiz.models import Participants, Quiz


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        raise Http404('کاربر مورد نظر یافت نشد')

    context = {'page': 'login'}
    return render(request, 'users_accounts/login_register.html', context)


def registerPage(request):
    regisetr_form = RegistrationForm(request.POST or None)
    if regisetr_form.is_valid():
        user = regisetr_form.save(commit=False)
        user.username = regisetr_form.cleaned_data.get('username')
        user.save()
        login(request, user)
        return redirect('home')

    context = {'page': 'register', 'form': regisetr_form}
    return render(request, 'users_accounts/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profilePage(request):
    user = User.objects.get(id=request.user.id)
    name = user.get_full_name()
    participants = Participants.objects.filter(student=user, is_finished=True)
    quiz = Quiz.objects.filter(host=user)
    context = {'user': user, 'name': name, 'participants': participants, 'quiz': quiz}
    return render(request, 'users_accounts/profile.html', context)


def editProfilePage(request):
    user = User.objects.get(id=request.user.id)
    form = EditProfileForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('profile')

    context = {'form': form, 'user': user}

    return render(request, 'users_accounts/edit_profile.html', context)


def quizStudents(request, pk):
    quiz = Quiz.objects.get(title=pk)
    participants = Participants.objects.filter(quiz=quiz, is_finished=True)
    context = {'quiz': quiz, 'participants': participants}
    return render(request, 'users_accounts/quiz_students.html', context)