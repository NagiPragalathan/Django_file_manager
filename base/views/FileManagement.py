from django.shortcuts import render, redirect
from base.models import PathManager, FolderManager

def add_data(request):
    if request.method == 'POST':
        # Retrieve data from request.POST
        
        # check title value are unique or not.. check user are logged or not
        
        path = request.POST.get('path')
        file = request.FILES.get('file')  # Assuming file is submitted in the form
        category = request.POST.get('category')
        title = request.POST.get('title')
        

        # Create a new data entry
        PathManager.objects.create(
            user_id=request.user,
            path=path,
            file=file,
            category=category,
            title=title
        )
        sample = PathManager.objects.filter(user_id=request.user)
        for i in sample:
            print(i.path,i.file)

        return redirect('list_folders',path=path)  # Redirect to the list_data view after successful submission

    return render(request, 'file_manager/add_data.html')

def list_data(request):
    data_entries = PathManager.objects.all()
    return render(request, 'file_manager/list_data.html', {'data_entries': data_entries})




def add_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        category = request.POST.get('category')
        path = request.POST.get('path')

        FolderManager.objects.create(
            user_id=request.user,
            FolderName=folder_name,
            category=category,
            path=path
        )

        return redirect('list_folders',path=path)  # Redirect to the list_folders view after successful submission

    return render(request, 'file_manager/add_folder.html')

def list_folders(request, path):
    user = request.user
    print(path)
    Files = PathManager.objects.filter(user_id=user, path=path)
    folders = FolderManager.objects.filter(user_id=user, path=path).order_by('FolderName')
    Files = sorted(Files, key=lambda x: x.file.name)
    for file in Files:
        file_extension = file.file.name.split('.')[-1].lower()
        file.icon_path = f'/static/images/Folders/{file_extension}.png'  # Adjust the path as needed
        file.type = file_extension
        file.title_name = file.title + "." + file_extension
    out = ""
    path_list = []
    out_path = {}
    for i in path.split("."):
        out = out + i + "."
        path_list.append(out)
    path_list = [s[:-1] if s.endswith('.') else s for s in path_list]
    for i,j in zip(path_list,path.split('.')):
        out_path[j] = i
        
    print(out_path)
    
    return render(request, 'file_manager/Manager.html', {'path':path,'path_alter':path.replace(".", "/"),'path_list':out_path,'folders': folders, 'files': Files})
