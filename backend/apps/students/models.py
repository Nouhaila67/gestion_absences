from django.db import models
from django.contrib.auth.models import AbstractUser
# Modèle utilisateur personnalisé
class User(AbstractUser):
    id = models.AutoField(primary_key=True)  # ID explicite
    role = models.CharField(max_length=50, choices=[('student', 'Student'), ('teacher', 'Teacher')])

    def __str__(self):
        return self.username  

# Modèle étudiant lié au CustomUser
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.user.username 

# Modèle de présence
class Presence(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course_name} - {self.date}"

# Modèle d'assiduité
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('P', 'Présent'), ('A', 'Absent')])

    def __str__(self):
        return f"{self.student.user.username} - {self.date}"
