from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from xhtml2pdf import pisa
from django.contrib.auth.models import User

from .models import Student, Marks, CIE, Semester

# Create your views here.

def render_to_pdf(template_src, context_dict):
    template = render_to_string(template_src, context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="progress_report.pdf"'
    pisa_status = pisa.CreatePDF(template, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + str(pisa_status.err) + '</pre>')
    return response

def index(request):
    return render(request, "index.html")

def teacher(request):
    return render(request, "main/teacher_dashboard.html")

def add_marks(request):
    if request.method == "POST":
        sem = int(request.POST["sem"])
        cie = int(request.POST["cie"])
        class_code = request.POST["class_code"]
        class_students = Student.objects.filter(class_code=class_code)
        students = []
        for student in class_students:
            students.append(User.objects.get(id=student.student.id))
            
        data = {
            'cie': cie,
            'sem': sem,
            'sub_code': request.POST["sub_code"],
            'students': zip(students, class_students),
        }
        return render(request, "main/enter_marks.html", data)
        
        
    return render(request, "main/add_marks.html")

def enter_marks(request):
    sem_val = request.POST["sem"]
    cie_val = request.POST["cie"]
    sub_code_val = request.POST["sub_code"]
    marks = []
    for key in request.POST.keys():
        if "marks" in key:
            student = Student.objects.get(id=key[len("marks-"):])
            attendance = request.POST[f"attendance-{key[len("marks-"):]}"]
            marks.append((student, request.POST[key], attendance))
    
    for mark in marks:
        sem = Semester.objects.get_or_create(
            sem=sem_val
        )
        cie = CIE.objects.get_or_create(
            sem=sem[0],
            cie=cie_val,
            sub_code=sub_code_val
        )
        mark_tup = Marks.objects.get_or_create(
            student=mark[0],
            cie=cie[0],
            # marks=mark[1],
            # attendance=mark[2],
        )
        st_mark = mark_tup[0]
        st_mark.marks=mark[1]
        st_mark.attendance=mark[2]
        st_mark.save()
        
    return redirect("message_page")
    
    
def get_marks(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        cie = request.POST.get('cie')
        sem = request.POST.get('sem')
        
        student = Student.objects.get(usn=usn)
        semester = Semester.objects.get(sem=sem)
        cie_obj = CIE.objects.filter(cie=cie, sem=semester)
        print(cie_obj)
        marks_obj = []
        for cie in cie_obj:
            marks = Marks.objects.get(student=student, cie=cie)
            marks_obj.append(marks)
            print(marks)
        
        return render(request, 'main/marks.html', {'marks_obj': marks_obj})
    
    return render(request, 'main/edit_marks.html')

def update_marks(request, pk):
    marks_obj = Marks.objects.get(pk=pk)
    if request.method == 'POST':
        marks_obj.marks = request.POST.get('marks')
        marks_obj.attendance = request.POST.get('attendance')
        marks_obj.save()
        return redirect('get_marks')
    
    return render(request, 'main/update_marks.html', {'marks_obj': marks_obj})

def view_marks(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        cie = request.POST.get('cie')
        sem = request.POST.get('sem')
        
        student = Student.objects.get(usn=usn)
        semester = Semester.objects.get(sem=sem)
        cie_obj = CIE.objects.filter(cie=cie, sem=semester)
        marks_obj = []
        for cie in cie_obj:
            try:
                marks = Marks.objects.get(student=student, cie=cie)
                marks_obj.append(marks)
            except ObjectDoesNotExist as e:
                print(e)
               
        return render(request, 'main/marks2.html', {'marks_obj': marks_obj})
    
    return render(request, 'main/view_marks.html')
    
# def view_marks2(request, pk):
#     marks_obj = Marks.objects.get(pk=pk)
#     return render(request, 'main/marks2.html', {'marks_obj': marks_obj})

def student_dashboard(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        cie = request.POST.get('cie')
        sem = request.POST.get('sem')
        
        student = Student.objects.get(usn=usn)
        semester = Semester.objects.get(sem=sem)
        cie_obj = CIE.objects.filter(cie=cie, sem=semester)
        marks_obj = []
        # for cie in cie_obj:
        #     marks = Marks.objects.get(student=student, cie=cie)
        #     ## make changes here use view marks
        #     marks_obj.append(marks)
        #     print(marks)
        for cie in cie_obj:
            try:
                marks = Marks.objects.get(student=student, cie=cie)
                marks_obj.append(marks)
            except ObjectDoesNotExist as e:
                print(e)
            
        if 'generate_pdf' in request.POST:
             return render_to_pdf('main/progress_report_pdf.html', {'marks_obj': marks_obj})
               
        return render(request, 'main/student_view_marks.html', {'marks_obj': marks_obj})  
    

    return render(request, "main/student_dashboard.html")

def is_user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def message_page(request):
    user = request.user
    is_teacher = is_user_in_group(user, 'Teachers')
    is_student = is_user_in_group(user, 'Students')
    data = {
        'is_teacher': is_teacher,
        'is_student': is_student,
    }
    return render(request, "main/message_page.html", data)



        
    