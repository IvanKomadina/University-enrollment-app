from django.shortcuts import render, redirect
from .models import Korisnici, Uloge, Predmeti, Upisi
from .decorators import admin_required, student_required, profesor_required, admin_student_required
from projekt.authentication import Authentication
from django.contrib.auth import login, logout
from .forms import CourseForm, StudentForm, ProfesorForm	
from django.contrib.auth.hashers import make_password
from django import forms 
from django.http import HttpResponseRedirect

# Create your views here.

# LOGIN
def userLogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = None
        auth = Authentication()
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user = request.user
            if(user.role_id == 1):
                return redirect('adminHome')
            elif(user.role_id == 2):
                return redirect('profesorHome')
            elif(user.role_id == 3):
                return redirect('studentHome')
        else:             
            message = {"message": "Invalid credentials!"}
            return render(request, 'login.html', message) 
    return render(request, 'login.html')

# LOGOUT
def userLogout(request):
    logout(request)
    return redirect('login')

# ADMIN HOMEPAGE
@admin_required
def adminHome(request):
    return render(request, 'home_admin.html')

#ADMIN COURSE FUNCTIONS
@admin_required
def courses(request):
    courses = Predmeti.objects.all()
    return render(request, 'courses.html', {'courses': courses})

@admin_required
def addCourse(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('courses')
    elif request.method == "GET":
        form = CourseForm()
        return render(request, 'add_course.html', {'form': form})
    
@admin_required
def editCourse(request, courseID):
    course = Predmeti.objects.get(id=courseID)
    if request.method == "POST":
        if "update" in request.POST:
            form = CourseForm( request.POST, instance=course)
            if form.is_valid():
                form.save()
            return redirect('courses')
        elif "delete" in request.POST:
            course.delete() 
            return redirect('courses')
    elif request.method == "GET":
        form = CourseForm(instance=course)
        return render(request, 'edit_course.html', {'form': form})
    
@admin_required
def studentsOnCourse(request, courseID):
    upisi = Upisi.objects.all().filter(predmet_id=courseID)
    return render(request, 'students_on_course.html', {'upisi': upisi}) 

# ADMIN STUDENT FUNCTIONS
@admin_required
def students(request):
    students = Korisnici.objects.all().filter(role_id=3)
    return render(request, 'students.html', {'students': students})

@admin_required
def addStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.password = make_password(form.cleaned_data['password'])
            form2.save()
        return redirect('students')
    elif request.method == 'GET':
        form = StudentForm()
        return render (request, 'add_student.html', {'form': form})
    
@admin_required
def editStudent(request, studentID):
    student = Korisnici.objects.get(id=studentID)
    if request.method == "POST":
        form = StudentForm( request.POST, instance=student)
        if form.is_valid():
            form.save()
        return redirect('students')
    elif request.method == "GET":
        form = StudentForm(instance=student)
        form.fields['password'].required = False
        form.fields['password'].widget = forms.HiddenInput() 
        return render(request, 'edit_student.html', {'form': form})
    
# ADMIN PROFESOR FUNCTIONS
@admin_required
def profesors(request):
    profesors = Korisnici.objects.all().filter(role_id=2)
    return render(request, 'profesors.html', {'profesors': profesors})

@admin_required
def addProfesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.password = make_password(form.cleaned_data['password'])
            form2.save()
        return redirect('profesors')
    elif request.method == 'GET':
        form = ProfesorForm()
        return render (request, 'add_profesor.html', {'form': form})
    
@admin_required
def editProfesor(request, profesorID):
    profesor = Korisnici.objects.get(id=profesorID)
    if request.method == "POST":
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
        return redirect('profesors')
    elif request.method == "GET":
        form = ProfesorForm(instance=profesor)
        form.fields['password'].required = False
        form.fields['password'].widget = forms.HiddenInput() 
        return render(request, 'edit_profesor.html', {'form': form})
    
# UPISNI LIST
@admin_student_required
def upisniList(request, studentID):
    courses = Predmeti.objects.all()
    student = Korisnici.objects.get(id=studentID)
    upisi = Upisi.objects.filter(student_id=studentID)
    upisani = Upisi.objects.filter(status='Upisan').filter(student_id=studentID)
    polozeni = Upisi.objects.filter(status='Polozen').filter(student_id=studentID)
    izg_potpis = Upisi.objects.filter(status='Izgubio potpis').filter(student_id=studentID)
    neupisani = courses.exclude(id__in=upisani.values('predmet_id'))
    neupisani = neupisani.exclude(id__in=polozeni.values('predmet_id'))
    neupisani = neupisani.exclude(id__in=izg_potpis.values('predmet_id'))
    if request.method == "POST":
        for course in courses:
            if course.name in request.POST:
                if request.POST[course.name] == 'Upis':
                    upis = Upisi(predmet_id=course.id, student_id=studentID, status='Upisan')    
                    upis.save()
                elif request.POST[course.name] == 'Ispis':
                    Upisi.objects.get(student_id=studentID, predmet_id=course.id).delete()
    if (student.status == 'redovni' and request.user.role_id == 1):
        semestri = {1,2,3,4,5,6}
        return render(request, 'upisni_list_redovni.html', {'courses': courses, 'student': student, 'semestri': semestri,'upisi': upisi, 'upisani': upisani, 'neupisani': neupisani})
    elif (student.status == 'izvanredni' and request.user.role_id == 1):
        semestri = {1,2,3,4,5,6,7,8}
        return render(request, 'upisni_list_izvanredni.html', {'courses': courses, 'student': student, 'semestri': semestri,'upisi': upisi, 'upisani': upisani, 'neupisani': neupisani})
    elif (student.status == 'redovni' and request.user.role_id == 3):
        semestri = {1,2,3,4,5,6}
        return render(request, 'upisni_list_redovni_student.html', {'courses': courses, 'student': student, 'semestri': semestri,'upisi': upisi, 'upisani': upisani, 'neupisani': neupisani})
    elif (student.status == 'izvanredni' and request.user.role_id == 3):
        semestri = {1,2,3,4,5,6,7,8}
        return render(request, 'upisni_list_izvanredni_student.html', {'courses': courses, 'student': student, 'semestri': semestri,'upisi': upisi, 'upisani': upisani, 'neupisani': neupisani})


# STUDENT HOMEPAGE
@student_required
def studentHome(request):
    student = request.user
    return render(request, 'home_student.html', {'student': student})

# PROFESOR HOMEPAGE
@profesor_required
def profesorHome(request):
    return render(request, 'home_profesor.html')

@profesor_required
def profesorCourses(request):
    courses = Predmeti.objects.all().filter(nositelj_id=request.user.id)
    return render(request, 'profesor_courses.html', {'courses': courses})

@profesor_required
def studentsOnCourseProfesor(request, courseID):
    polozeni = Upisi.objects.all().filter(predmet_id=courseID, status='Polozen')
    upisani = Upisi.objects.all().filter(predmet_id=courseID, status='Upisan')
    izg_potpis = Upisi.objects.all().filter(predmet_id=courseID, status='Izgubio potpis')
    if request.method == "POST":
        for upis in upisani:
            if upis.student.username in request.POST:
                if request.POST[upis.student.username] == 'Polozio': 
                    polozen = Upisi.objects.get(predmet_id=courseID, student_id=upis.student_id)    
                    polozen.status = "Polozen"
                    polozen.save()
                    return HttpResponseRedirect("#")
                elif request.POST[upis.student.username] == 'Izgubio potpis': 
                    polozen = Upisi.objects.get(predmet_id=courseID, student_id=upis.student_id)    
                    polozen.status = "Izgubio potpis"
                    polozen.save()
                    return HttpResponseRedirect("#")
    return render(request, 'students_on_course_profesor.html', {'upisani': upisani, 'polozeni': polozeni, 'izg_potpis': izg_potpis}) 


# FILTRIRANJE PREDMETA
@student_required
def filterPredmeta(request, studentID):
    student = Korisnici.objects.get(id=studentID)
    courses = Predmeti.objects.all()
    ects_filter = []
    semestar_filter = []
    sem_ects_filter = []
    if request.method == "POST":
        if request.POST['filter'] == 'Filtriraj po bodovima':
            for course in courses:
                if course.ects > int(request.POST['bodovi']):
                    ects_filter.append(course.name)
        elif request.POST['filter'] == 'Filtriraj po semestru':
            for course in courses:
                if course.sem_red == int(request.POST['semestar']):
                    semestar_filter.append(course.name)
        elif request.POST['filter'] == 'Filtriraj po semestru i bodovima':
            for course in courses:
                if (course.sem_red == int(request.POST['semestar']) and course.ects > int(request.POST['bodovi'])):
                    sem_ects_filter.append(course.name)
    return render(request, 'filter_predmeta.html', {'student': student, 'ects_filter': ects_filter, 'semestar_filter': semestar_filter, 'sem_ects_filter': sem_ects_filter})


# OSOBNA STATISTIKA
@student_required
def osobnaStatistika(request, studentID):
    student = Korisnici.objects.get(id=studentID)
    polozeni = Upisi.objects.all().filter(student_id=studentID, status='Polozen')
    upisani = Upisi.objects.all().filter(student_id=studentID, status='Upisan')
    broj_obaveznih = 0
    broj_upisanih = 0
    for upis in polozeni:
        if (upis.predmet.izborni == 'ne' or upis.predmet.izborni == 'NE'):
            broj_obaveznih += 1
    for upis in upisani:
        if upis.predmet.ects > 6:
            broj_upisanih += 1
    return render(request, 'osobna_statistika.html', {'student': student, 'broj_obaveznih': broj_obaveznih, 'broj_upisanih': broj_upisanih})