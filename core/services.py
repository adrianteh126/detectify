from roboflow import Roboflow
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import random
import string
import json
from datetime import datetime


api_key = os.getenv("ROBOFLOW_API_KEY")
project_id = os.getenv("ROBOFLOW_PROJECT_ID")
model_version = os.getenv("ROBOFLOW_MODEL_VERSION")

rf = Roboflow(api_key=api_key)
project = rf.workspace().project(project_id)
model = project.version(model_version).model

# define the path to the media directory
base_dir = settings.BASE_DIR
media_dir = os.path.join(base_dir, "media")
save_dir = os.path.join(base_dir, "result")


def classify_face_shape_and_save(uploaded_image) -> str:
    if not uploaded_image:
        raise Exception("No image is provided")
    filename = uploaded_image.name
    _, file_extension = os.path.splitext(filename)
    img_file_extension = [".jpeg", ".jpg", ".png", ".webp"]
    if file_extension not in img_file_extension:
        raise Exception("No image shape not supported")

    # construct the path to for uploaded image
    fs = FileSystemStorage()
    media_path = os.path.join(media_dir, filename)
    save_path = os.path.join(save_dir, filename)
    # check duplicated filename / path
    if os.path.exists(media_path) or os.path.exists(save_path):
        filename, media_path, save_path = generate_new_path(filename)
    # save an image annotated with the predictions
    fs.save(media_path, uploaded_image)
    # predict face class
    res = model.predict(media_path)
    res.save(save_path)
    predictions = res.json()["predictions"][0]
    shape = predictions["top"]
    return filename, shape


def capture_classify_face_shape_and_save(image_data: bytes):
    # Get current date and time to use in the image name
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{formatted_datetime}.png"
    media_path = os.path.join(media_dir, filename)
    save_path = os.path.join(save_dir, filename)
    # check duplicated filename / path
    if os.path.exists(media_path) or os.path.exists(save_path):
        filename, media_path, save_path = generate_new_path(filename)
    # save image in /media
    with open(media_path, "wb") as f:
        f.write(image_data)
    # predict face class
    res = model.predict(media_path)
    res.save(save_path)
    predictions = res.json()["predictions"][0]
    shape = predictions["top"]
    return filename, shape


def classify_face_shape_by_url(url: str):
    # infer on an image hosted elsewhere
    try:
        res = model.predict(
            url,
            hosted=True,
        )
        prediction = res.json()["predictions"][0]
        result = {
            "face_shape": prediction["top"],
            "confidence": prediction["confidence"],
        }
        return result
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Utils
def generate_new_path(filename: str):
    file_name, file_extension = os.path.splitext(filename)
    random_suffix = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    filename = f"{file_name}_{random_suffix}{file_extension}"
    # generate new path based on new filename
    media_path = os.path.join(media_dir, filename)
    save_path = os.path.join(save_dir, filename)
    return filename, media_path, save_path


def get_glasses_info(shape: str):
    file_path = os.path.join(base_dir, "core", "config", "face_shape.json")
    with open(file_path, "r") as json_file:
        face_shape = json.load(json_file)
    if shape == "Heart":
        return face_shape["heart"]
    elif shape == "Oblong":
        return face_shape["oblong"]
    elif shape == "Oval":
        return face_shape["oval"]
    elif shape == "Round":
        return face_shape["round"]
    elif shape == "Square":
        return face_shape["square"]
    else:
        return None
