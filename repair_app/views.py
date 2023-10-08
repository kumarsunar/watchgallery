from django.shortcuts import render

def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        watch_brand = request.POST.get('watch-brand')
        watch_model = request.POST.get('watch-model')
        description = request.POST.get('description')

        # Perform further processing (e.g., store data in database)

        # Return a response
        return render(request, 'confirmation.html')
    else:
        return render(request, 'form.html')
