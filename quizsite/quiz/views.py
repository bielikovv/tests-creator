from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .utils import *

from .models import *
from .forms import *
from django.views.generic import View

class MainPage(View):
    def get(self, request):
        return render(request, 'quiz/main_page.html')



class CreateTest(View):
    def get(self, request):
        return render(request, 'quiz/create_test.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        result = request.POST.get('result')
        Test.objects.create(user=request.user, name=name, description=description, max_result=result, is_published=False)
        test_pk = Test.objects.get(name=name, description=description, max_result=result).pk
        return JsonResponse({'test_pk':test_pk})



class RedactTest(View):
    def get(self, request, test_pk):
        questions = Question.objects.filter(test=get_test(test_pk), user=request.user)
        form = CreateQuestionForm(initial={'user':request.user, 'test':get_test(test_pk)})
        if request.user == get_test(test_pk).user:
            return render(request, 'quiz/redact_test.html', {"form":form, 'questions':questions, "test_pk":test_pk})
        return render(request, 'quiz/current_test.html', {'questions':questions, "test_pk":test_pk})

    def post(self, request, test_pk):
        test = Test.objects.get(pk=test_pk, user=request.user)
        value = 0
        for item in Question.objects.filter(test=test):
            value += item.value
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            question_pk = request.POST.get('question_pk')
            answer = request.POST.get('answer')
            checkbox = request.POST.get('checkbox')
            if request.POST.get('answer_delete'):
                delete_answer(request)
                return JsonResponse({})
            if request.POST.get('question_delete'):
                delete_question(request)
                return JsonResponse({})
            if request.POST.get('validator'):
                if test.max_result == value:
                    add_created_test_to_user_profile(request, test, test_pk)
                    return JsonResponse({})
                else:
                    allocate_values(request, test)
                    return JsonResponse({})
            add_answer(request, answer, checkbox, question_pk)
            return JsonResponse({})

        form = CreateQuestionForm(request.POST, initial={'user': request.user, 'test': test})
        if form.is_valid():
            form.save()
            return redirect(reverse('redact-test', kwargs={'test_pk':test_pk}))



class GetTest(View):
    def get(self, request, test_pk):
        if request.user.profile in Test.objects.get(pk=test_pk).completed_by_user.all():
            return redirect(reverse('completed-test-page', kwargs={'test_pk':test_pk}))
        test = Test.objects.get(pk=test_pk)
        questions = Question.objects.filter(test=test)
        return render(request, 'quiz/current_test.html', {'questions':questions, 'test':test, 'test_pk':test_pk})

    def post(self, request, test_pk):
        test = Test.objects.get(pk=test_pk)
        is_right = request.POST.get('is_right')
        value = request.POST.get('value')
        answer_pk = request.POST.get('answer_pk')
        question_pk = request.POST.get('question_pk')
        question_pk = Question.objects.get(pk=question_pk)

        if is_right == 'True':
            res = get_result(request, test, question_pk, answer_pk)
            if res.result == 0:
                res.result += float(value)
                res.save()
        else:
            res = get_result(request, test, question_pk, answer_pk)
            if res.result != 0:
                res.result -= float(value)
                res.save()
            else:
                res.result += 0
                res.save()
        return JsonResponse({'answer':Answer.objects.get(pk=answer_pk).content})



class TestResult(View):
    def get(self, request, test_pk):
        test = Test.objects.get(pk=test_pk)
        result = Result.objects.filter(test=test, user=request.user)
        tst = Test.objects.get(pk=test_pk)
        tst.completed_by_user.add(request.user.profile)
        res = 0
        for item in result:
            res += float(item.result)
        return render(request, 'quiz/completed_test.html', {'result':result, 'res':res, 'test':test, 'test_pk':test_pk})

    def post(self, request, test_pk):
        test = Test.objects.get(pk=test_pk).completed_by_user
        test.remove(request.user.profile)

        return JsonResponse({})



class SearchTests(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            tests = Test.objects.filter(name__icontains=search_query, is_published=True).order_by('-date')
        else:
            tests = Test.objects.filter(is_published=True).order_by('-date')

        paginator = Paginator(tests, 10)
        page_num = request.GET.get('page', 1)
        page_objects = paginator.get_page(page_num)
        return render(request, 'quiz/search_tests.html', {'tests':tests, 'search':search_query, 'page_obj':page_objects})



class ShowProfile(View):
    def get(self, request):
        created_tests = Test.objects.filter(user=request.user)
        completed_tests = Test.objects.filter(completed_by_user=request.user.profile)

        return render(request, 'quiz/profile.html', {'completed_tests':completed_tests, 'created_tests':created_tests})



def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'quiz/register.html', {'form':form})



def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
    else:
        form = LoginForm()
    return render(request, 'quiz/login.html', {'form':form})



def logout_user(request):
    logout(request)
    return redirect('main_page')

