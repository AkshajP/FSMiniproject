from django.shortcuts import render,HttpResponse
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
            return render_to_pdf('main/progress_report_pdf.html', data)
        
        return render(request, "main/progress_report_student.html", data)
    
    return render(request, "main/student_dashboard.html")