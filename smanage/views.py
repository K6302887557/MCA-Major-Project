import io
import csv
import base64
import pandas as pd
from PIL import Image
from django.shortcuts import render,redirect
from .models import CustomUser, UploadedFile, UserCredentials
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UploadFileForm
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        generate_key = request.POST.get('generate_key')
        
        try:
            user = CustomUser.objects.create_user(
                email=email, username=username, password=password, name=name, generate_key=generate_key
            )
            
            # Save the generated key in the user model
            user.generated_key = generate_key
            user.save()
            
        except IntegrityError:
            messages.error(request, f'The email address {email} is already in use.')
            return redirect('signup')
        
        messages.success(request, f'Account created for {username}!')
        return redirect('home_page')
    else:
        return render(request, 'signup.html')
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("UserID:", username)
        print('Password:', password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def home_page(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        password = request.POST.get('password')
       
        
        # Retrieve the saved key and password from the database
        user_credentials = UserCredentials.objects.first()

        if user_credentials and user_credentials.key_field == key and check_password(password, user_credentials.password_field):
            # Key and password are valid, perform the desired action
            return redirect('manage_details')
        else:
            # Invalid credentials, display an error message
            messages.error(request, 'Invalid credentials. Please try again.')

    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('-upload_date')
    
    
    for uploaded_file in uploaded_files:
        if uploaded_file.file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file.file.path)
            uploaded_file.file_content = df.to_html(classes='table table-striped')

    return render(request, 'home_page.html', {'uploaded_files': uploaded_files})

def manage_details(request):
    if request.method == 'POST':
        form_upload = UploadFileForm(request.POST, request.FILES)
        if form_upload.is_valid():
            uploaded_file = form_upload.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('manage_details')
    else:
        form_upload = UploadFileForm()
    
    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('upload_date')
    uploaded_files = uploaded_files[::-1] #Reverse the order of the queryset
    
    return render(request, 'manage_details.html', {'form_upload': form_upload, 'uploaded_files': uploaded_files})

def delete_file(request, file_id):
    file = UploadedFile.objects.get(id=file_id)
    file.delete()
    return redirect(reverse('manage_details'))



def logout(request):
    return render(request,'logout.html')


