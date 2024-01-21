from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Uloge(models.Model):
    ROLES=(('admin', 'admin'),('profesor','profesor'),('student','student'))
    role=models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        return self.role

class Korisnici(AbstractUser):
    STATUS=(('none','None'),('redovni','redovni'),('izvanredni','izvanredni'))
    status=models.CharField(max_length=50, choices=STATUS)
    role=models.ForeignKey(Uloge, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s' % (self.username)

class Predmeti(models.Model):
    IZBORNI=(('DA','da'),('NE','ne'))
    name=models.CharField(max_length=50)
    kod=models.CharField(max_length=50)
    program=models.CharField(max_length=50)
    ects=models.IntegerField()
    sem_red=models.IntegerField()
    sem_izv=models.IntegerField()
    izborni=models.CharField(max_length=50, choices=IZBORNI)
    nositelj=models.ForeignKey(Korisnici, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.name, self.kod, self.program,self.ects,self.sem_red,self.sem_izv,self.izborni,self.nositelj)

class Upisi(models.Model):
    student=models.ForeignKey(Korisnici, on_delete=models.CASCADE, db_constraint=False)
    predmet=models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    STATUS=(('Upisan','Upisan'),('Polozen','Polozen'),('Izgubio_potpis', 'Izgubio potpis'))
    status=models.CharField(max_length=64, choices=STATUS, default="Upisan")

    def __str__(self):
        return '%s %s %s' % (self.student, self.predmet, self.status)