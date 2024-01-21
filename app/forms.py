from django import forms 
from .models import Korisnici, Predmeti, Uloge

class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['nositelj'].queryset = Korisnici.objects.filter(role_id=2)

    class Meta:
        model = Predmeti
        fields = '__all__'

class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset=Uloge.objects.filter(role="student")
        self.fields['username'].help_text = None

    class Meta:
        model = Korisnici
        fields = ['username','password','first_name','last_name','status','role']
        widgets = {'password': forms.PasswordInput()}

class ProfesorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [('none', 'None')]
        self.fields['role'].queryset=Uloge.objects.filter(role="profesor")
        self.fields['username'].help_text = None

    class Meta:
        model = Korisnici
        fields = ['username','password','first_name','last_name','status','role']
        widgets = {'password': forms.PasswordInput()}