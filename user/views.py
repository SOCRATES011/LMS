from django.shortcuts import render, redirect
from django.contrib import messages 
from django.views import View
from user.models import ContactMessage
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def homepage(request):
    return render(request, 'home.html')

@login_required
def aboutpage(request):
    return render(request, 'about.html')
@login_required
def contactfunction(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if not name or not email or not message:
            messages.error(request, 'All fields are required')
            return render(request, 'contact.html')
        # if not email:
        #     messages.error(request, 'Email is required')
        #     return render(request, 'contact.html')
        # if not message:
        #     messages.error(request, 'No message sent')
        #     return render(request, 'contact.html')
        if len(name) < 2:
            messages.warning(request, 'Name is too short')
            return render(request, 'contact.html')
        messages.success(request, 'Your message has been received, we will be in touch!')
        return redirect(homepage)
    
    return render(request, 'contact.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')
    
    
    def post(self, request):
         name = request.POST.get("name")
         email = request.POST.get("email")
         message = request.POST.get("message")
         if not name or not email or not message:
            messages.error(request, 'All fields are required')
            render(request, 'contact.html')
        
         if len(name) < 2:
            messages.error(request, 'Name is too short')
            return render(request, 'contact.html')
         
         if len(name) > 250:
            messages.error(request, 'Name is too long')
            return render(request, 'contact.html')
         
        #? Do something with user's input

         ContactMessage.objects.create(name = name, email = email, message = message)
         messages.success(request, 'Your message has been received, we will be in touch!')
         return redirect(homepage)
         