# registration/views.py
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import UserProfile

import random
from django.core.mail import send_mail
from .models import UserProfile


def homepage(request):
    return render(request, 'homepage.html')

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password == confirm_password:
                # Create a new user profile
                UserProfile.objects.create(username=username, email=email, password=password)
                return redirect('registration_success')
            else:
                form.add_error('confirm_password', 'Passwords do not match')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

def registration_success_view(request):
    return render(request, 'registration_success.html')

def login_with_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username and password match
        user = UserProfile.objects.get(username=username)  # Assume the user exists

        if user.password == password:
            # Generate OTP
            otp_generated = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP

            # Send OTP to the user's email
            send_mail(
                'Your OTP for login',
                f'Your OTP is: {otp_generated}',
                'your_email@example.com',  # Replace with your sender email
                [user.email],  # Get user's email from the User model
                fail_silently=False,
            )
            # Store the OTP (you might want to use a separate model or extend User model to store OTP)
            user.profile.otp = otp_generated  # Replace with how you store OTP for the user
            user.profile.save()

            # Redirect to OTP verification page
            return render(request, 'otp_verification.html', {'username': username})
        else:
            # Handle invalid username or password
            pass

    return render(request, 'login.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         otp_entered = request.POST.get('otp')

#         # Check if username and password match in the database
#         user = UserProfile.objects.get(username=username, password=password)  # Handle exceptions for non-existent users

#         # Check if entered OTP matches the stored OTP for the user (assuming OTP is stored in UserProfile model)
#         # if user.otp == otp_entered:
#         #     # OTP matches, log in the user
#         #     # Your login logic here
#         #     return redirect('home')
#         # else:
#         #     # Invalid OTP, display an error or handle accordingly
#         #     pass
#         #else:
#         # Generate and send OTP to the user's email
#         # Generate OTP
#         otp_generated = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
        
#         # Send OTP to the user's email
#         send_mail(
#             'Your OTP for login',
#             f'Your OTP is: {otp_generated}',
#             'your_email@example.com',  # Replace with your sender email
#             [user.email],  # Get user's email from the form or UserProfile model
#             fail_silently=False,
#         )
#         # Store OTP in the database (update the user's OTP field in UserProfile model)
#         user.otp = otp_generated
#         user.save()
        
#         if user.otp == otp_entered:
#         # OTP matches, log in the user
#         # Your login logic here
#             return redirect('home')

#     return render(request, 'login.html')


# views.py

def verify_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        otp_entered = request.POST.get('otp')

        # Get the user based on the username
        user = UserProfile.objects.get(username=username)  # Assume the user exists

        if user.profile.otp == otp_entered:  # Compare the stored OTP
            # OTP matches, log in the user (you can implement your login logic here)
            # Redirect to the home page or dashboard upon successful login
            return render(request, 'home.html')
        else:
            # Handle invalid OTP
            pass

    return render(request, 'otp_verification.html', {'username': username})

