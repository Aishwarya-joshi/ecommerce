# views.py
import random
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User

def login_with_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username and password match
        user = User.objects.get(username=username)  # Assume the user exists

        if user.check_password(password):
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
