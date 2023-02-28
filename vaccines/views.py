from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from .tasks import send_confirmation_email
from .forms import CreateUserForm
from .models import Vaccine, Appointment, ConfirmationEmail, User


# def register(request):
#     print('test1')
#     if request.method == 'POST':
#         print('test4')
#         form = CustomUserCreationForm(request.POST)
#         formset = ChildFormSet(request.POST, instance=form.instance)
#         if form.is_valid() and formset.is_valid():
#             print('test2')
#             user = form.save()
#             formset.instance = user
#             formset.save()
#             messages.success(request, 'تم إنشاء الحساب بنجاح')
#             return redirect('login')
#     else:
#         print('test3')
#         form = CustomUserCreationForm()
#         formset = ChildFormSet(instance=User())
#     return render(request, 'accounts/registration1.html', {'form': form, 'formset': formset})


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vaccines:vaccine_list')  # Replace 'home' with your desired redirect URL
    else:
        form = CreateUserForm()
    return render(request, 'accounts/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('vaccines:vaccine_list')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('vaccines:vaccine_list')


@login_required
def vaccine_list(request):
    user = get_object_or_404(User, pk=request.user.id)
    vaccines = Vaccine.objects.exclude(pk__in=user.previous_vaccinations.all().values_list('pk', flat=True))
    return render(request, 'vaccines/vaccine_list1.html', {'vaccines': vaccines})


def book_appointment(request, vaccine_id):
    vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        date = request.POST['date']
        email = request.POST['email']
        appointment = Appointment.objects.create(vaccine=vaccine, date=date, father=user, email=email)
        confirmation_email = ConfirmationEmail.objects.create(appointment=appointment)
        send_confirmation_email.delay(appointment.id)

        return HttpResponseRedirect(reverse('vaccines:appointment_confirmation', args=(vaccine_id, date)))
    return render(request, 'vaccines/book_appointment.html', {'vaccine': vaccine})


def appointment_confirmation(request, vaccine_id , date):
    appointment = get_object_or_404(Appointment, vaccine__id=vaccine_id, date=date)
    confirmation_email = get_object_or_404(ConfirmationEmail, appointment=appointment)
    return render(request, 'vaccines/appointment_confirmation.html', {'appointment': appointment, 'confirmation_email': confirmation_email})


def vaccine_detail(request, vaccine_id):
    vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
    context = {'vaccine': vaccine}
    return render(request, 'vaccines/vaccine_detail.html', context)