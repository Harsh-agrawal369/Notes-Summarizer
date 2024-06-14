from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'index.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES['notesFile']:
        noteFile = request.FILES['notesFile']
        
        return HttpResponse(request, noteFile)