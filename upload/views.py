from django.shortcuts import render
from .forms import ImageForm
from fer import FER
from cv2 import cv2
import glob
import operator
import os
from django.conf import settings


def clear_directory():

    if not os.listdir(settings.MEDIA_ROOT + "images"):
        pass
    else:
        files = glob.glob(settings.MEDIA_ROOT + "images/*")
        for f in files:
            os.remove(f)


def detect_emotions(image_file):

    # clear_directory()

    img = cv2.imread(settings.MEDIA_ROOT + str(image_file))
    detector = FER(mtcnn=True)
    result = detector.detect_emotions(img)

    for i in range(len(result)):
        box = result[i]['box']
        x, y, h, w = box[0], box[1], box[2], box[3]
        emotion = max(result[0]['emotions'].items(), key=operator.itemgetter(1))[0]
        if img.shape[0] < 500 or img.shape[1] < 500:
            cv2.rectangle(img, (x, y), (x+h, y+w), (0, 0, 0), 2)
            cv2.rectangle(img, (x, y), (x+h, y+w), (255, 255, 255), 1)
            cv2.putText(img, emotion, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), thickness=2)
            cv2.putText(img, emotion, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=1)
        else:
            cv2.rectangle(img, (x, y), (x+h, y+w), (0, 0, 0), 5)
            cv2.rectangle(img, (x, y), (x+h, y+w), (255, 255, 255), 3)
            cv2.putText(img, emotion, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), thickness=5)
            cv2.putText(img, emotion, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), thickness=3)

    path = settings.MEDIA_ROOT + str(image_file)
    cv2.imwrite(path, img)


def image_upload_view(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img = form.instance.image

            detect_emotions(img.name)
            img = "/media/" + img.name

            return render(request, 'index.html', {'form': form, 'img': img})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})
