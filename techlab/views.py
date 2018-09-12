from django.shortcuts import render


def index(request):
	return render(request, 'techlab/index.html')

def about(request):
	return render(request, 'techlab/about.html')

def contact(request):
	return render(request, 'techlab/contact.html')
