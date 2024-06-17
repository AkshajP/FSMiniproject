from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Image
import io
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import textwrap
from datetime import datetime


def generate_pdf(df, row,Branch_Choice,test_choice,submission_d,semester,no_of_subjects,note):  
    today = datetime.today()
    day = today.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    date_of_generation = today.strftime(f"%d{suffix} %b, %Y")
    date_of_generation = str(date_of_generation)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0, leftMargin=50, rightMargin=50, bottomMargin=0)
    
    styles = getSampleStyleSheet()

    # Creating a bold and capitalized Times New Roman style
    bold_times_style = styles["Heading1"]
    bold_times_style.fontName = "Times-Bold"
    bold_times_style.fontSize = 12 
    bold_times_style.alignment = 1
    bold_times_style.textTransform = "uppercase"
    bold_times_style.spaceAfter = 1
    bold_times_style.spaceBefore = 1
 


    bold_style = styles["Heading2"]
    bold_style.fontName = "Times-Bold"
    bold_style.fontSize = 10
    bold_style.spaceAfter = 1
    bold_style.spaceBefore = 1


    elements = [] 

    header_path = "Images/Header_RV.png"
    image = Image(header_path, width=8*inch, height=1.6445*inch)
    image.vAlign = "TOP"
    elements.append(image)

    heading = Paragraph('<u>'+Branch_Choice+'</u>', bold_times_style)
    elements.append(heading)
 
    heading = Paragraph('<u>'+test_choice+'</u>', bold_times_style)
    elements.append(heading)

    style_sheet = getSampleStyleSheet() #date
    style = style_sheet['Normal']
    text = date_of_generation
    para = Paragraph(text, style)
    elements.append(para)

    style_sheet = getSampleStyleSheet() #date
    style = style_sheet['Normal']
    text = "\u00a0"
    para = Paragraph(text, style)
    elements.append(para)

    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "To, "
    para = Paragraph(text, style)
    elements.append(para)
    
    father = str(df.iloc[row, 3])
    heading = Paragraph("\u00a0 \u00a0 \u00a0Mr/Mrs \u00a0"+father+",", bold_style)
    elements.append(heading)

    student_name = df.iloc[row,1]
    USN = df.iloc[row,2]
    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0The progress report of your ward <b>"+str(student_name)+",\u00a0"+str(USN)+"</b> studying in <b>"+str(semester)+"</b> is given below : "
    para = Paragraph(text, style)
    elements.append(para)

    wrapped_sl = textwrap.fill("Sl. No", width=3)
    wrapped_attendance  = textwrap.fill("Attendance Percentage", width=10)
    wrapped_classheld  = textwrap.fill("Classes Held", width=7)
    wrapped_classattended = textwrap.fill("Classes Attended", width=9)
    wrapped_testmarks = textwrap.fill(str(df.iloc[1,10]), width=10)
    wrapped_assignment = textwrap.fill(str(df.iloc[1,11]), width=10)
    data = [[wrapped_sl,"Subject Name",wrapped_classheld,wrapped_classattended,wrapped_attendance,wrapped_testmarks,wrapped_assignment]]

    for i in range(no_of_subjects):
        subject = df.iloc[0, 8 + i * 4]
        try:
            classesheld = int(df.iloc[row, 8 + i * 4])
        except ValueError:
            classesheld = 0
        try:
            classattended = int(df.iloc[row, 9 + i * 4])
        except ValueError:
            classattended = 0
    
        # Check if both classesheld and classattended are zero
        if classesheld == 0 and classattended == 0:
            classesheld = '-'
            classattended = '-'
            attendance = '-'
        else:
            try:
                attendance = int(classattended / classesheld * 100)
            except ZeroDivisionError:
                attendance = 0
    
        marks = df.iloc[row, 10 + i * 4]
        assignment = df.iloc[row, 11 + i * 4]
        wrapped_subject = textwrap.fill(subject, width=30)
    
        data.append([str(i + 1), wrapped_subject, classesheld, classattended, "{}%".format(attendance), marks, assignment])

    table = Table(data, splitByRow=1, spaceBefore=10, spaceAfter=10, cornerRadii=[1.5,1.5,1.5,1.5])
    

    table.setStyle(TableStyle([      
    
    ('BACKGROUND', (0, 0), (-1, 0), '#FFFFFF'),
    ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('fontsize', (-1,-1), (-1,-1), 14),
    ('ALIGNMENT', (1, 1), (1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),
    ('GRID', (0, 0), (-1, -1), 1, "black")
  ]))

    elements.append(table)

    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "<b>Remarks:</b>\u00a0"+str(df.iloc[row,7])+""
    para = Paragraph(text, style)
    elements.append(para)

    style = style_sheet['Normal']
    text = "\u00a0 "
    para = Paragraph(text, style)
    elements.append(para)

    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "<b>Note:</b>\u00a0"+str(note)+""
    para = Paragraph(text, style)
    elements.append(para)


    style = style_sheet['Normal']
    text = "\u00a0 "
    para = Paragraph(text, style)
    elements.append(para)


    counsellor_mail = str(df.iloc[row,6])
    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "Please sign and send the report to “"+counsellor_mail+"” on or before "+submission_d+"."
    para = Paragraph(text, style)
    elements.append(para)

    image_path = "Images/default.png"

    # Use if-else statements to set image_path based on the selected branch
    if Branch_Choice == "COMPUTER SCIENCE & ENGINEERING":
        image_path = "Images/CSE_Signature.png"
    elif Branch_Choice == "INFORMATION SCIENCE & ENGINEERING":
        image_path = "Images/ISE_Signature.png"
    elif Branch_Choice == "ELECTRONICS & COMMUNICATION ENGINEERING":
        image_path = "Images/ECE_Signature.png"
    elif Branch_Choice == "MECHANICAL ENGINEERING":
        image_path = "Images/ME_Signature.png"
    elif Branch_Choice == "MASTER OF COMPUTER APPLICATIONS":
        image_path = "Images/MCA_Signature.png"
    image = Image(image_path, width=7*inch, height=1.4155*inch)
    elements.append(image)

    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "\u00a0" 
    para = Paragraph(text, style)
    elements.append(para)

    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "\u00a0"
    para = Paragraph(text, style)
    elements.append(para)

    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "This report was auto-generated through EDUSTACK RVITM"
    para = Paragraph(text, style)
    elements.append(para)

    doc.build(elements)
    
    buffer.seek(0)
    return buffer