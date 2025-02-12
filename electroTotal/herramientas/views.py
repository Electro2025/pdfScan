import os
import threading
import time
from django.shortcuts import render, redirect
from django.http import FileResponse, Http404, HttpResponseRedirect
from django.conf import settings
import img2pdf
from pdf2image import convert_from_bytes
from django.urls import reverse
from urllib.parse import urlencode
from PIL import Image, ImageFilter
from .forms import PDFUploadForm

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            color_mode = form.cleaned_data['color_mode']
            dpi = form.cleaned_data['dpi']
            denoise = form.cleaned_data['denoise']
            processed_pdf_path = process_pdf(uploaded_file, color_mode, dpi, denoise)
            return HttpResponseRedirect(reverse('download_pdf') + '?' + urlencode({'pdf_path': processed_pdf_path}))
    else:
        form = PDFUploadForm()
    return render(request, 'upload.html', {'form': form})

def process_pdf(uploaded_file, color_mode, dpi, denoise):
    images = convert_from_bytes(uploaded_file.read(), dpi=dpi)
    processed_images = []
    temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    for i, img in enumerate(images):
        if color_mode == 'grayscale':
            img = img.convert("L")
        if denoise:
            img = img.filter(ImageFilter.MedianFilter(size=3))
        temp_img_path = os.path.join(temp_dir, f"temp_page_{i}.jpg")
        img.save(temp_img_path, "JPEG", quality=75)
        processed_images.append(temp_img_path)
    processed_pdf_path = os.path.join(temp_dir, "processed_document.pdf")
    with open(processed_pdf_path, "wb") as f:
        f.write(img2pdf.convert(processed_images))
    for img_path in processed_images:
        os.remove(img_path)
    return processed_pdf_path

def delete_file_later(file_path, delay=5):
    time.sleep(delay)
    try:
        os.remove(file_path)
        print(f"Archivo eliminado: {file_path}")
    except PermissionError:
        print(f"El archivo {file_path} aún está en uso y no pudo eliminarse.")
    except FileNotFoundError:
        print(f"El archivo {file_path} ya fue eliminado.")

def download_pdf(request):
    pdf_path = request.GET.get('pdf_path')
    if not pdf_path or not os.path.exists(pdf_path):
        raise Http404("El archivo solicitado no existe.")
    response = FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename="processed_document.pdf")
    threading.Thread(target=delete_file_later, args=(pdf_path,)).start()
    return response
