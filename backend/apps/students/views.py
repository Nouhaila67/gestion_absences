from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from apps.students.models import User, Presence
import qrcode
from io import BytesIO

# Utiliser le modèle d'utilisateur personnalisé
User = get_user_model()

# Test: Création d'un utilisateur et d'une présence
user = User.objects.create_user(username='testuser', password='password123')
print(user.username)
student = User.objects.first()  # Choisir un étudiant existant
presence = Presence.objects.create(student=student, course_name="Maths")
print(presence)

# Vue pour enregistrer la présence
@api_view(['POST'])
def register_presence(request):
    student_id = request.data.get('student_id')
    course_name = request.data.get('course_name')

    if not student_id or not course_name:
        return Response({'error': 'Student ID and Course name are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = User.objects.get(id=student_id, role='student')  # Utilisation de User pour trouver l'étudiant
        Presence.objects.create(student=student, course_name=course_name)
        return Response({'message': 'Presence registered successfully'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)


# Vue pour générer un QR code
@api_view(['GET'])
def generate_qr_code(request, student_id):
    try:
        # Vérifier que student_id est bien un entier
        if not str(student_id).isdigit():
            return Response({'error': 'Invalid student ID'}, status=status.HTTP_400_BAD_REQUEST)

        student = User.objects.get(id=student_id)  # Utilise User ici

        # Générer les données QR
        qr_data = f"student_id:{student.pk}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Enregistrer l'image en mémoire
        buffer = BytesIO()
        img = qr.make_image(fill='black', back_color='white')
        img.save(buffer, "PNG")
        buffer.seek(0)

        return HttpResponse(buffer.read(), content_type='image/png')

    except User.DoesNotExist:  # Utilise User ici
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
