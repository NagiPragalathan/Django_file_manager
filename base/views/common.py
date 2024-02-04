from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from base.models import FolderManager, Rating

def home(request):
    folders = FolderManager.objects.filter(path='root').order_by('FolderName')[::-1]
    rating = {}
        
    for i in folders:
        average_rating = Rating.calculate_average_rating(category=i.category)
        rating[i.category] = average_rating
        print(average_rating)
    for i in folders:
        i.rating = rating.get(i.category)
        print(i.category,rating.get(i.category), i.rating)
    
    if len(folders) > 4:
        folders = folders[0:4]
    
    if request.user.is_authenticated:
        login = True
    else:
        login = False
    if request.user.is_authenticated:
        return redirect("list_course", path="root")
    elif request.user.is_superuser:
        return redirect('list_folders', path='root')
    else:
        return render(request, "home/index.html", {'auth':login, 'courses':folders, 'rate':[1,2,3,4,5]})

def logout_view(request):
    logout(request)
    return redirect('home')