# views.py
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User
from base.models import Config


def config_list(request, path):
    configs = Config.objects.filter(q_path=path)
    return render(request, 'TimeConfig/config_list.html', {'configs': configs,'path':path})

def create_config(request,path):
    try:
        obj = Config.objects.filter(q_path=path)[::-1][0]
        configs = Config.objects.filter(q_path=path)
        print(obj)
        return render(request, 'TimeConfig/Show_msg.html', {'configs': configs, 'path':path, 'obj':obj})
    except:
            print("error")
            time_mis = request.POST.get('time_mis', '')
            Config.objects.create(q_path=path, time_mis=time_mis)
            return render(request, 'TimeConfig/create_config.html', {'path':path})
        

def update_config(request, config_id, path):
    config = get_object_or_404(Config, pk=config_id)

    if request.method == 'POST':
        time_mis = request.POST.get('time_mis', '')
        config.time_mis = time_mis
        config.save()
        return redirect('list_folders', path)

    return render(request, 'TimeConfig/update_config.html', {'config': config, "path":path})

def delete_config(request, config_id,path):
    config = get_object_or_404(Config, pk=config_id)
    config.delete()
    return redirect('config_list',path)
