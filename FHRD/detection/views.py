from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from django.conf import settings

from .models import *
from .forms import *
from .camera import *

import cv2
from random import randint

# Create your views here.

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def find_faces(img_path):
    xml_path = os.path.join(settings.BASE_DIR, 'static/xml/haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(xml_path)
    photo_read = cv2.imread(img_path)
    photo_read = cv2.resize(photo_read, (780, 540),
               interpolation = cv2.INTER_NEAREST)
    gray = cv2.cvtColor(photo_read, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(photo_read, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imwrite(settings.MEDIA_ROOT + '\detected_images\image.jpeg', photo_read)
    return True

def home(request):
    l = ['Bonjour', 'Hola', 'Zdravstvuyte', 'Nǐn hǎo', 'Salve', 'Konnichiwa', 'Guten Tag', 'Olá',
        'Anyoung haseyo', 'Goddag', 'Shikamoo', 'Goedendag', 'Yassas', 'Dzień dobry', 'Selamat siang',
        'Namaste', 'Merhaba', 'Shalom', 'God dag', 'Hello'   
    ]
    greet = l[randint(0, len(l)-1)] + ','
    return render(request, 'detection/home.html', context={'greet': greet})

def face_detection(request):
    photos = Photo.objects.all()
    photos_count = photos.count()
    context = {'photos': photos, 'photos_count': photos_count}
    return render(request, 'detection/face.html', context)

def heart_rate_calculation(request):
    result = VideoCamera().get_heart_rate()
    result *= 3
    if result < 50 or result > 100:
        result = "Some Error!! Try again"
    context = {'result': result}
    return render(request, 'detection/heart_calc.html', context)

def heart_rate_detection(request):
    return render(request, 'detection/heart.html')

def file_upload(request):
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(data=request.POST, files=request.FILES)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('face')

    context = {'form': form}
    return render(request, 'detection/file_upload.html', context)

def video(request):
	return render(request, 'detection/video.html')

def view_photo(request, pk):
    image = Photo.objects.get(id=pk)
    context = {'image': image}
    return render(request, 'detection/view_photo.html', context)

def detect_faces(request, pk):
    image = Photo.objects.get(id=pk)
    final_path = os.path.join(settings.MEDIA_ROOT, str(image.img))
    find_faces(final_path)
    context = {'image' : image}
    return render(request, 'detection/detect_faces.html', context=context)
   
def delete_photo(request, pk):
    image = Photo.objects.get(id=pk)
    if request.method == "POST":
        image.delete()
        return redirect('face')
    context = {'image' : image}
    return render(request, 'detection/delete_photo.html', context=context)