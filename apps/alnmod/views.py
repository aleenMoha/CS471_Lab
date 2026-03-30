from django.shortcuts import render

def index(request):
    return render(request, 'alnmod/index.html', {'name':'Aleen'})

def age(request):
    return render (request, 'alnmod/age.html', {'age':21.1})

def bros(request):
   return render (request, 'alnmod/bros.html', {'bros':['toto', 'lno', 'koki']})
