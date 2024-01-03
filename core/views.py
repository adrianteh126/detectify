from django.http import HttpRequest
from django.shortcuts import render
from .services import (
    classify_face_shape_and_save,
    capture_classify_face_shape_and_save,
    classify_face_shape_by_url,
)
from django.views.decorators.http import require_GET, require_POST
import base64
from urllib.parse import unquote


@require_GET
def index(request: HttpRequest):
    return render(request, "index.html")


@require_GET
def find_your_perfect_glasses(request: HttpRequest):
    return render(request, "find-your-perfect-glasses.html")


@require_POST
def submit_image_url(request: HttpRequest):
    imageUrl = request.POST.get("img_url", "")
    try:
        result = classify_face_shape_by_url(imageUrl)
        context = {
            "imageUrl": imageUrl,
            "face_shape": result["face_shape"],
            "confidence": result["confidence"],
        }
        return render(request, "result.html", context)
    except:
        context = {
            "imageUrl": imageUrl,
        }
        return render(request, "result.html", context)


@require_GET
def result(request: HttpRequest, imageUrl=None):
    context = {
        "imageUrl": imageUrl,
    }
    return render(request, "result.html", context)


@require_POST
def upload_image(request: HttpRequest):
    uploaded_image = request.FILES["uploaded_image"]
    try:
        filename = classify_face_shape_and_save(uploaded_image)
        context = {"filename": filename}
        return render(request, "result-upload.html", context)
    except:
        context = {"filename": None}
        return render(request, "result-upload.html", context)


@require_POST
def captured_image(request: HttpRequest):
    data = request.POST.get("capturedImage", "")
    # Remove the data URI prefix
    cleaned_data = data.replace("data:image/png;base64,", "")
    # Unquote the URL-encoded data
    unquoted_data = unquote(cleaned_data)
    # Decode the base64 data
    image_data = base64.b64decode(unquoted_data)
    try:
        filename = capture_classify_face_shape_and_save(image_data)
        context = {"filename": filename}
        return render(request, "result-upload.html", context)
    except:
        context = {"filename": None}
        return render(request, "result-upload.html", context)
