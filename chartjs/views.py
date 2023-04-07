import json

from django.db.models import Case, CharField, IntegerField, Value, When
import cv2
import os
import requests
from django.core.files.base import ContentFile
from django.db.models import Case, CharField, IntegerField, Value, When
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from requests import Response
from rest_framework.views import APIView
from skimage.metrics import structural_similarity as ssim
from .models import Iteration, Data, ImageMetrics


class HomeView(View):
    def get(self, request, *args, **kwargs):
        # Make a GET request and save the data to a variable
        response = requests.get('http://art1x.pythonanywhere.com/snippets/1/')
        response_data = response.json()

        # Create a directory to save the images in
        folder_name = 'media'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Create a new Iteration instance
        iteration = Iteration.objects.create(name='')

        # Create a new Data instance and associate it with the Iteration instance
        data = Data.objects.create(iteration=iteration)

        # Save the images into the "media" folder with filenames darkN.png, decodedN.png, etc.
        file_names = ['dark', 'decoded', 'disparity', 'edited', 'light', 'lookup', 'mask']
        for i, file_name in enumerate(file_names):
            url = response_data[file_name]
            # Get the file extension from the URL
            file_ext = os.path.splitext(url)[1]
            # Construct the filename as a string with the index plus 1
            file_name_template = '{}{}'.format(i + 1, file_ext)
            file_path = os.path.join(settings.MEDIA_ROOT, folder_name, file_name_template)
            # Download the image from the URL and save it to the file path
            with open(file_path, 'wb') as f:
                f.write(requests.get(url).content)
            # Save the image to the database with the corresponding iteration ID and filename
            setattr(data, file_name, ContentFile(requests.get(url).content, f"{file_name}{iteration.pk}{file_ext}"))

            # Load the original image and the mask image
            orig_img = cv2.imread('uploads/media/1.png')
            mask_img = cv2.imread('uploads/media/5.png')

            # Convert both images to grayscale
            orig_gray = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
            mask_gray = cv2.cvtColor(mask_img, cv2.COLOR_BGR2GRAY)

            # Compute the absolute difference between the pixel values of the two images
            diff = cv2.absdiff(orig_gray, mask_gray)

            # Threshold the difference image to create a binary mask where the values represent the areas of the images where the two images differ
            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            # Compute image quality metrics
            ssim_score = ssim(orig_gray, mask_gray) * 100
            mse = ((orig_gray.astype("float") - mask_gray.astype("float")) ** 2).mean()

            # Save the metrics to the database
            data.ssim_score = ssim_score
            data.mse = mse
            data.save()

            # Create a new ImageMetrics instance and save it to the database
            ImageMetrics.objects.create(x=mse, y=ssim_score, data=data)

            # Assign quality categories based on threshold values
            setattr(data, f"{file_name}_quality", Case(
                When(ssim_score__gte=95, then=Value('Good Quality')),
                When(ssim_score__gte=80, then=Value('Medium Quality')),
                default=Value('Bad Quality'),
                output_field=CharField()
            ))

            return render(request, 'chartjs/index.html')


class ChartData(APIView):
    def get(self, request, format=None):
        # Code to generate the data
        data = {'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                'datasets': [{'label': 'My First Dataset',
                              'data': [65, 59, 80, 81, 56, 55, 40],
                              'fill': False,
                              'borderColor': 'rgb(75, 192, 192)',
                              'lineTension': 0.1}]}



    def get(self, request, format=None):
        labels = [
            '5%',
            '10%',
            '15%',
            '20%',
            '25%',
            '30%',
            '35%',
            '40%',
            '45%',
            '50%',
            '55%',
            '60%',
            '65%',
            '70%',
            '75%',
            '80%',
            '85%',
            '90%',
            '95%',
            '100%',
            ]
        chartLabel = 'Iteration Data'
        y = [0, 10, 5, 2, 20, 30, 100]

        data = {
            'labels':labels,
            'chartLabel':chartLabel,
            'chartdata':y,
        }

        # Return the data as a JSON response with an HTTP status code of 200
        return HttpResponse(json.dumps(data), content_type='application/json')