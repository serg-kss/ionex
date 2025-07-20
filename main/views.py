from django.contrib import messages
from django.shortcuts import redirect, render
from main.models import Contacts, Contact


def index(request):
    record = Contacts.objects.first()
    #seo = record.seo

    context ={
        'title': "ІОНЕКС - Товари та послуги для рентгенкабінету",
        'seo': 'seo', #here
    }
    return render(request, 'main/index.html', context)


def contacts(request):

    record = Contacts.objects.first()
    contact_email = record.email
    contact_phone = record.phone
    contact_address = record.address
    seo = record.seo

    context ={
        'title': "ІОНЕКС - Наші контакти",
        'email': contact_email,
        'phone': contact_phone,
        'address': contact_address,
        'seo': seo,
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Contact.objects.create(name=name, email=email, message=message)
            messages.success(request, "Питання відправлено")
            return redirect('/')
        else:
            error = "Пожалуйста, заполните все поля."
            return render(request, 'main/contact.html', {'error': error})

    return render(request, 'main/contact.html', context)