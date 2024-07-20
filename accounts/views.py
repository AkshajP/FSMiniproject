from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from main.models import TeacherDB, Student
# Create your views here.

def is_user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            #which page has to be displayed
            if is_user_in_group(user, 'Teachers'):
                return redirect("teacher_dashboard")
            if is_user_in_group(user, 'Students'):
                return redirect("student_dashboard")
            print("logged in")
            return redirect("/")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("login")
    return render(request, "accounts/login.html")

def teacher_register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]        
        email = request.POST["email"]        
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST["password2"]
                
        teacher = TeacherDB.objects.get(email=email)
        if not teacher:
            print("You are not a teacher")
        else:                
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username taken")
                    return redirect('teacher_register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, "Email not yours!")
                    return redirect('teacher_register')
                else:
                    user = User.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        username = username,
                        email = email,
                        password = password1                 
                    )
                    user.save()
                    group = Group.objects.get(name="Teachers")
                    user.groups.add(group)
                    messages.info(request, "user created")   
                    return redirect("login")
                        
            else:
                messages.info("Password not matching") 
                return redirect('teacher_register') 
            return redirect("/")  
    else:
        return render(request, "accounts/teacher_register.html")
  
def student_register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]        
        email = request.POST["email"]        
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST["password2"]
        usn = request.POST["usn"]
        class_code = request.POST["class_code"]
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email not yours!")
                return redirect('register')
            else:
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password1,
                )
                user.save()
                Student.objects.create(
                    student=user,
                    class_code=class_code,
                    usn=usn,
                )
                messages.info(request, "user created")   
                return redirect("login")
                     
        else:
            messages.info("Password not matching") 
            return redirect('register') 
        return redirect("/")  


    else:
        return render(request, "accounts/student_register.html")

def logout(request):
    auth.logout(request)
    return redirect("/")