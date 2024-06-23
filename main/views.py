from django.shortcuts import render,HttpResponse, redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Students
from .models import Teachers
from .models import Subject
from .models import Marks

# Create your views here.
def index(request):
    return render(request, "base.html")

def render_to_pdf(template_src, context_dict):
    template = render_to_string(template_src, context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="progress_report.pdf"'
    pisa_status = pisa.CreatePDF(template, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + str(pisa_status.err) + '</pre>')
    return response

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
        
        if 'generate_pdf' in request.POST:
            counsellor = Teachers.objects.get(id=student.counsellor_id)
            data["counsellor"] = counsellor
            return render_to_pdf('main/progress_report_pdf.html', data)
        
        return render(request, "main/progress_report_student.html", data)
    
    return render(request, "main/student_dashboard.html")

def teacher_dashboard(request):
    if request.method == "POST" or "old_page" in request.session:
        if "old_page" in request.session:
            old_data = request.session["old_page"]
            usn = old_data["usn"]
            sem = old_data["sem"]
            cie = old_data["cie"]
            action = old_data['action']
            del request.session["old_page"]
        else:
            usn = request.POST["usn"]
            sem = request.POST["sem"]
            cie = request.POST["cie"]
            action = request.POST['action']
        
        student = Students.objects.get(usn=usn)
        marks = Marks.objects.filter(usn=student.id, cie=cie)
        
        report = list()
        i = 1
        for mark in marks:
            subject = Subject.objects.get(id=mark.sub_code.id)
            subject_mark = mark.marks
            subject_attendence = mark.attendance
            report.append((subject.sub_code, subject.sub_name, subject_mark, subject_attendence, i))
            i += 1
        
        data = {
            "usn": usn,
            "sem": sem,
            "cie": cie,
            "reports": report,
        }
        
        if action == 'add':
            return render(request, 'main/add_marks.html', data)
        if action == 'edit':
            return render(request, 'main/edit_marks.html', data)
        if action == 'view':
            return render(request, 'main/view_marks.html', data)
    
    
    return render(request, "main/teacher_dashboard.html")

def add_or_edit(request):
    return render(request, "main/teacher_dashboard.html")

def add_marks(request):
    return render(request, "main/add_marks.html")

def edit_marks(request):
    if request.method == "POST":
        usn = request.POST["usn"]
        next_page = {
            "usn": usn,
            "sem": request.POST["sem"],
            "cie": request.POST["cie"],
            "action": request.POST["action"],
        }
        for key in request.POST.keys():
            if "sub_code" in key:
                sub_code = request.POST[key]
                mark = request.POST[f"marks_{request.POST[key]}"]
                attendance = request.POST[f"attendance_{request.POST[key]}"]
                
                student = Students.objects.get(usn=usn)
                subject = Subject.objects.get(sub_code=sub_code)
                marks = Marks.objects.get(usn=student.id, sub_code=subject.id)
                marks.marks = mark
                marks.attendance = attendance
                marks.save()
        
        request.session["old_page"] = next_page             
        return redirect("teacher_dashboard")