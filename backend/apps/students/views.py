from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import User, Presence
import qrcode
from io import BytesIO


# Enregistrer la présence d'un étudiant
@api_view(['POST'])
def register_presence(request):
    student_id = request.data.get('student_id')
    course_name = request.data.get('course_name')

    if not student_id or not course_name:
        return Response({'error': 'Student ID and Course name are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student: User = User.objects.get(id=student_id)
        Presence.objects.create(student=student, course_name=course_name)
        return Response({'message': 'Presence registered successfully'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)


# Générer un QR Code pour un étudiant avec paramètre dans l'URL
@api_view(['GET'])
def generate_qr_code(request, student_id: int):
    try:
        student: User = User.objects.get(id=student_id)

        # Générer les données QR
        qr_data = f"student_id:{student.id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Enregistrer l'image en mémoire
        buffer = BytesIO()
        img = qr.make_image(fill='black', back_color='white')
        img.save(buffer, format='PNG')
        buffer.seek(0)

        return HttpResponse(buffer.read(), content_type='image/png')

    except User.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
