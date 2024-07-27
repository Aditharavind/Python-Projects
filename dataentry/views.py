# views.py
from django.core.management import call_command
from django.shortcuts import render, redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages



def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        # Store this file inside the upload model
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # Build the file path
        relative_path = upload.file.url
        base_url = str(settings.BASE_DIR)
        file_path = base_url + relative_path

        # Trigger the Celery task
        try:
            call_command('importdata', file_path, model_name)
        except Exception as e:
            messages.error(request,str(e))

        # Show message to the user
        messages.success(request, "Your data is  imported.")
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
        return render(request, 'dataentry/importdata.html', context)
def export_data(request):
    if request.method=='POST':
        model_name=request.POST.get('model_name')
        try:
            call_command('exportdata',model_name)
        except Exception as  e:
            raise e
        messages.success(request,"Your data is Exported")
        return redirect('export_data')
    else:
        custom_models=get_all_custom_models()
        context={
            'custom_models':custom_models,
        }
    return render(request,'dataentry/exportdata.html',context)
