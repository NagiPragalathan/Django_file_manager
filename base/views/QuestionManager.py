from django.shortcuts import render, redirect, get_object_or_404
from base.models import McqQuestionBase
from django.http import HttpResponse

def add_question(request):
    if request.method == 'POST':
        question_text = request.POST['question']
        image = request.FILES.get('image', None)
        category = request.POST['category']
        question_type = request.POST['question_type']
        options = request.POST.getlist('options')
        correct_answer = request.POST['correct_answer']

        # Creating a new McqQuestionBase instance
        new_question = McqQuestionBase(
            question=question_text,
            image=image,
            category=category,
            question_type=question_type,
            options=options,
            correct_answer=correct_answer
        )
        new_question.save()

        return HttpResponse('Question added successfully!')

    return render(request, 'question_manager/add_question.html')

def edit_question(request, question_id):
    question = get_object_or_404(McqQuestionBase, id=question_id)

    if request.method == 'POST':
        question.question = request.POST['question']
        question.image = request.FILES.get('image', None)
        question.category = request.POST['category']
        question.question_type = request.POST['question_type']
        question.options = request.POST.getlist('options')
        question.correct_answer = request.POST['correct_answer']
        question.save()

        return HttpResponse('Question updated successfully!')

    context = {'question': question}
    return render(request, 'edit_question.html', context)

def delete_question(request, question_id):
    question = get_object_or_404(McqQuestionBase, id=question_id)

    if request.method == 'POST':
        question.delete()
        return HttpResponse('Question deleted successfully!')

    context = {'question': question}
    return render(request, 'delete_question.html', context)
