from .models import *




def delete_answer(request):
    answer_delete_pk = request.POST.get('answer_delete')
    Answer.objects.get(pk=answer_delete_pk).delete()



def delete_question(request):
    question_delete_pk = request.POST.get('question_delete')
    Question.objects.get(pk=question_delete_pk).delete()



def add_answer(request, answer, checkbox, question_pk):
    ans = Answer.objects.create(content=answer, is_right=checkbox, user=request.user)
    quest = Question.objects.get(pk=question_pk)
    quest.answer.add(ans)



def allocate_values(request, test):
    N = len(Question.objects.filter(test=test))
    t = test.max_result / N
    for item in Question.objects.filter(test=test):
        item.value = t
        item.save()
    Profile.objects.get(user=request.user).created_test.add(test)



def get_result(request, test, question_pk, answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    Result.objects.get_or_create(user=request.user, test=test, question=question_pk, defaults={'user': request.user, 'test': test, 'result': 0, 'question': question_pk})
    res = Result.objects.get(user=request.user, test=test, question=question_pk)
    res.answer.clear()
    res.answer.add(answer)
    res.save()
    return res


def get_test(test_pk):
    test = Test.objects.get(pk=test_pk)
    return test



def add_created_test_to_user_profile(request, test, test_pk):
    Profile.objects.get(user=request.user).created_test.add(test)
    status = Test.objects.get(pk=test_pk)
    status.is_published = True
    status.save()