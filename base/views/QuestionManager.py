from django.shortcuts import render, redirect, get_object_or_404
from base.models import McqQuestionBase
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def add_question(request,path):
    if request.method == 'POST':
        question_text = request.POST['question']
        image = request.FILES.get('image', None)
        category = request.POST['category']
        question_type = request.POST['question_type']
        options = request.POST.getlist('options')
        correct_answer = request.POST['correct_answer']
        path = request.POST['path']

        print(path, options)
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
    return render(request, 'question_manager/add_questions.html',{"path":path})

def delete_question(request, question_id):
    question = get_object_or_404(McqQuestionBase, id=question_id)

    if request.method == 'POST':
        question.delete()
        return HttpResponse('Question deleted successfully!')

    context = {'question': question}
    return render(request, 'delete_question.html', context)

import json

def edit_question(request,path, cat):
    mcq_questions = McqQuestionBase.objects.filter(user_id=request.user, copy_qust_path=path, category=cat)
    # Serialize the questions to JSON format
    if mcq_questions.exists():
        out = {"instructions":mcq_questions[0].instructions,"questions":[{'id':question.id,'question': question.question,'options': question.options,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in mcq_questions]}
        return render(request, 'question_manager/edit_questions.html', {"path": path, 'mcq_quiz': out})
    else:
        # Handle the case when no questions are found
        return render(request, 'question_manager/edit_questions.html', {"path": path, 'mcq_quiz': None})

@csrf_exempt
def update_db(request):
    try:
        # Hardcoded data for testing
        data = {}
        data = json.loads(request.body.decode('utf-8'))

        # Extract data from the JSON
        instructions = data.get('instructions', '')
        questions_data = data.get('questions', [])
        path = data.get('path', '')
        if instructions != '':
            for question_data in questions_data:
                question_text = question_data.get('question', '')
                options = question_data.get('options', [])
                correct_answer = question_data.get('correctAnswer', '')

                # Construct the options array (remove null values)
                options = [option for option in options if option is not None]

                # Find or create the McqQuestionBase object
                question, created = McqQuestionBase.objects.get_or_create(
                    question=question_text,
                    path=path,
                    user_id = request.user,
                    copy_qust_path=path.split('.')[1],
                    defaults={
                        'instructions': instructions,
                        'options': options,
                        'correct_answer': correct_answer,
                        'question_type': 'MCQ',  # You might want to adjust this based on your requirements
                        'category': path.split('.')[1],  # Adjust the category as needed
                    }
                )

                # If the question already existed, update its fields
                if not created:
                    question.instructions = instructions
                    question.options = options
                    question.correct_answer = correct_answer,
                    question.copy_qust_path = path.split('.')[1],
                    question.save()

        return JsonResponse({'success': True, 'message': 'Data received and processed successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def get_questions_by_category(request, category):
    try:
        # Query the database to retrieve questions by category
        questions = McqQuestionBase.objects.filter(category=category)

        # Serialize the questions to JSON format
        serialized_questions = [{
            'id': question.id,
            'question': question.question,
            'options': question.options,
            'correct_answer': question.correct_answer,
            'instructions': question.instructions,
            'last_updated_date': question.last_updated_date,
        } for question in questions]

        return JsonResponse({'questions': serialized_questions})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    
    
@csrf_exempt
def handle_questions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        instructions = data.get('instructions', '')
        questions_data = data.get('questions', [])
        
        print(questions_data, instructions)

        for question_data in questions_data:
            question_id = question_data.get('id', None)
            question_text = question_data.get('question', '')
            options = question_data.get('options', [])
            correct_answer = question_data.get('correctAnswer', '')
            
            # You may need to adjust the category and path values based on your requirements
            category = 'your_category_value'
            path = 'your_path_value'

            # Create or update McqQuestionBase instance
            if question_id and question_id != 'none':
                # Update existing question
                question = McqQuestionBase.objects.get(pk=question_id)
                question.question = question_text
                question.options = options
                question.correct_answer = correct_answer
                question.instructions = instructions
                question.last_updated_date = timezone.now()
                question.save()
                print(question.question,"are updated...!")
            else:
                # Create new question
                McqQuestionBase.objects.create(
                    user_id=request.user,
                    question=question_text,
                    options=options,
                    correct_answer=correct_answer,
                    instructions=instructions,
                    category=category,
                    path=path
                )

        return JsonResponse({'message': 'Data processed successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)