from django.shortcuts import render
from .models import Students
from .models import Teachers
from .models import Subject
from .models import Marks

# Create your views here.
def index(request):
    return render(request, "base.html")

def student_dashboard(request):
    if request.method == "POST":
        usn = request.POST["usn"]
        sem = request.POST["sem"]
        cie = request.POST["cie"]
        
        student = Students.objects.get(usn=usn)
        marks = Marks.objects.filter(usn=student.id, cie=cie)
        
        report = list()
        for mark in marks:
            subject = Subject.objects.get(id=mark.sub_code.id)
            subject_mark = mark.marks
            subject_attendence = mark.attendance
            report.append((subject.sub_code, subject.sub_name, subject_mark, subject_attendence))
        
        data = {
            "usn": usn,
            "sem": sem,
            "cie": cie,
            "reports": report,
        }
        return render(request, "main/test_page.html", data)
    
    return render(request, "main/student_dashboard.html")