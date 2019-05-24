from django.shortcuts import render


def search_view(request):
    if request.method == 'GET':
        return render(request, 'place/search_view.html')


