from django.shortcuts import render, redirect, get_object_or_404
from base.models import McqQuestionBase, ImageEditor
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import uuid
import json
from django.db.models import Count, F
from itertools import groupby


def add_question(request, path):
    result = (
        McqQuestionBase.objects
        .values('copy_qust_path', 'id', 'user_id', 'question', 'image', 'category', 'question_type', 'options', 'correct_answer', 'instructions', 'path', 'last_updated_date')
        .annotate(count=Count('id'))
        .annotate(copy_qust_path_value=F('path'))
        .filter(copy_qust_path_value__isnull=False, user_id=request.user)
        .exclude(copy_qust_path_value__contains=',', path=path)  # Exclude items with a comma
        .annotate(copy_qust_path_values=F('copy_qust_path_value'))
    )
    print(result)
    # Group the results by copy_qust_path_value
    grouped_data = {key: list(group) for key, group in groupby(result, key=lambda x: x['path'])}
    # Pass the grouped_data to the template
    return render(request, 'question_manager/add_questions.html', {"grouped_data": grouped_data, "path": path})


def add_para_question(request,path):
    return render(request, 'question_manager/para_create.html',{"path":path})


def delete_question(request, question_id):
    question = get_object_or_404(McqQuestionBase, id=question_id)

    if request.method == 'POST':
        question.delete()
        return HttpResponse('Question deleted successfully!')

    context = {'question': question}
    return render(request, 'delete_question.html', context)

def edit_question(request,path):
    mcq_questions = McqQuestionBase.objects.filter(user_id=request.user)
    out_mcq = []
    for i in mcq_questions:
        print(i.copy_qust_path, i.id, i.question)
    print(f"==================================={path}===============================================")
    for i in mcq_questions:
        if "," in i.copy_qust_path:
            if path in i.copy_qust_path.split(", "):
                print(i.copy_qust_path, i.id, i.question)
                out_mcq.append(i)
        else:
            if path == i.copy_qust_path:
                print(i.copy_qust_path, i.id, i.question)
                out_mcq.append(i)
    print(out_mcq)
    out = {"instructions":mcq_questions[0].instructions,"questions":[{'id':question.id,'question': question.question,'options': question.options,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in out_mcq]}
    print(out,len(out))
    
    
    result = (
        McqQuestionBase.objects
        .values('copy_qust_path', 'id', 'user_id', 'question', 'image', 'category', 'question_type', 'options', 'correct_answer', 'instructions', 'path', 'last_updated_date')
        .annotate(count=Count('id'))
        .annotate(copy_qust_path_value=F('copy_qust_path'))
        .filter(copy_qust_path_value__isnull=False, user_id=request.user)
        .exclude(copy_qust_path_value__contains=',')  # Exclude items with a comma
        .annotate(copy_qust_path_values=F('copy_qust_path_value'))
    )

    # Group the results by copy_qust_path_value
    grouped_data = {key: list(group) for key, group in groupby(result, key=lambda x: x['copy_qust_path_value'])}
    # Serialize the questions to JSON format
    if mcq_questions.exists():
        out = {"instructions":mcq_questions[0].instructions,"questions":[{'id':question.id,'question': question.question,'options': question.options,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in out_mcq]}
        return render(request, 'question_manager/edit_questions.html', {"path": path, 'mcq_quiz': out,"grouped_data": grouped_data})
    else:
        # Handle the case when no questions are found
        return render(request, 'question_manager/edit_questions.html', {"path": path, 'mcq_quiz': None})

def para_edit_question(request,path, cat):
    mcq_questions = McqQuestionBase.objects.filter(user_id=request.user, copy_qust_path=path, quest_id=cat)

    # Serialize the questions to JSON format
    if mcq_questions.exists():
        out = {"instructions":mcq_questions[0].instructions,"questions":[{'id':question.id,'question': question.question,'options': question.options,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in mcq_questions]}
        return render(request, 'question_manager/para_quest.html', {"path": path, 'mcq_quiz': out,"cat":cat})
    else:
        # Handle the case when no questions are found
        return render(request, 'question_manager/para_quest.html', {"path": path, 'mcq_quiz': None})

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
                    copy_qust_path=path,
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
                    question.save()
        obj = McqQuestionBase.objects.all()
        for i in obj:
            print(i.path,i.copy_qust_path)

        return JsonResponse({'success': True, 'message': 'Data received and processed successfully','path':path})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def update_para_db(request):
    try:
        # Hardcoded data for testing
        data = {}
        data = json.loads(request.body.decode('utf-8'))
        unique_id = uuid.uuid4()

        # Extract data from the JSON
        Mail_question = data.get('instructions', '')
        questions_data = data.get('questions', [])
        path = data.get('path', '')
        if Mail_question != '':
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
                    quest_id = unique_id,
                    user_id = request.user,
                    copy_qust_path=path,
                    defaults={
                        'instructions': Mail_question,
                        'options': options,
                        'Para_quest':Mail_question,
                        'correct_answer': correct_answer,
                        'question_type': 'PARA',  # You might want to adjust this based on your requirements
                        'category': path.split('.')[1],  # Adjust the category as needed
                    }
                )

                # If the question already existed, update its fields
                if not created:
                    question.instructions = Mail_question
                    question.options = options
                    question.correct_answer = correct_answer,
                    question.save()
        obj = McqQuestionBase.objects.filter(question_type="PARA")
        for i in obj:
            print(i.path,i.copy_qust_path)

        return JsonResponse({'success': True, 'message': 'Data received and processed successfully', 'u_id':unique_id,"path":path})
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
        path = data.get('path', '')
        
        print(questions_data, instructions, len(questions_data))

        for question_data in questions_data:
            question_id = question_data.get('id', None)
            question_text = question_data.get('question', '')
            options = question_data.get('options', [])
            correct_answer = question_data.get('correctAnswer', '')
            
            print(path, len(path))
            # You may need to adjust the category and path values based on your requirements
            category = path.split('.')[1]
            

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
                    path=path,
                    copy_qust_path = path
                )

        return JsonResponse({'message': 'Data processed successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def handle_para_questions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        instructions = data.get('instructions', '')
        questions_data = data.get('questions', [])
        path = data.get('path', '')
        cat = data.get('cat', '')
        
        print(questions_data, instructions, cat)

        for question_data in questions_data:
            question_id = question_data.get('id', None)
            question_text = question_data.get('question', '')
            options = question_data.get('options', [])
            correct_answer = question_data.get('correctAnswer', '')
            
            print(path)
            # You may need to adjust the category and path values based on your requirements
            category = path.split('.')[1]
            

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
                    path=path,
                    copy_qust_path = path,
                    quest_id = cat
                )

        return JsonResponse({'message': 'Data processed successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def import_questions(request):
     if request.method == 'POST':
        data = json.loads(request.body)
        path = data.get('path', '')
        ids = data.get('ids', [])
        print(path,ids)
        for i in ids:
            question = McqQuestionBase.objects.get(id=i)
            if path not in question.path.split(','):
                new_path = question.path +", "+ path
            else:
                continue
            question.copy_qust_path = new_path
            question.last_updated_date = timezone.now()
            question.save()
        for i in ids:
            question = McqQuestionBase.objects.get(id=i)
            print(question.copy_qust_path)
        return JsonResponse({'message': 'Data processed successfully','path':path}, status=200)    
    
    
def add_image_editor(request):
    if request.method == 'POST':
        question_text = request.POST.get('question', '')
        # You may want to do additional processing here if needed
        ImageEditor.objects.create(question=question_text)
        return JsonResponse({'message': 'Data processed successfully'}, status=200)