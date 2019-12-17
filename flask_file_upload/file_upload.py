"""
Flask File Upload

    # Public api:

        file_uploads = FileUpload(app)

    ##### General Flask config options
    ````python
        UPLOAD_FOLDER = join(dirname(realpath(__file__)), "uploads/lessons")
        ALLOWED_EXTENSIONS = ["jpg", "png", "mov", "mp4", "mpg"]
        MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 1000mb
    ````


    ##### Setup
    ````python
        db = SQLAlchemy()
        file_uploads = FileUpload()
    ````


    ##### FlaskFileUploads needs to do some work with your SqlAlchemy model
    Decorate your SqlAlchemy model with your files
     ````python
        @file_uploads.Model("my_video")
        @file_uploads.Model("placeholder_img")
        class MyModel(db, uploads):
           id = Model(Integer, primary_key=True)
    ````

    ##### define files to be upload:
        (This is an example of a video with placeholder image attached):
    ````python
        my_video = request.files["my_video"]
        placeholder_img = request.files["placeholder_img"]
    ````


    ##### Get main form data and pass to your SqlAlchemy Model
    ````python
        blog_post = BlogPostModel(title="Hello World Today")

        file_uploads.save_files(blog_post, files={
            "my_video": my_video,
            "placeholder_img": placeholder_img,
        })
    ````

    ##### Update files
    ````python
        file_uploads.update_files(BlogPostModel, files=[my_video])
    ````


    ##### Update file name
    ````python
        file_uploads.update_file_name(BlogPostModel, my_video, new_filename="new_name")
    ````


    ##### Stream a file
    ````python
        First get your entity
        my_blog_post = BlogModel().get(id=1)  # Or your way of getting an entity
        file_upload.stream_file(blog_post, filename="my_video")
    ````


    ##### File Url paths
    ````python
        file_upload.get_file_url(blog_post, filename="placeholder_img")
    ````


"""
import os
from warnings import warn
from flask import send_from_directory, Flask
from werkzeug.utils import secure_filename
from typing import Any, List, Tuple, Dict

from ._config import Config
from .model import Model
from .column import Column


class FileUpload:

    app: Flask

    config: Config = Config()

    def __init__(self, app=None):
        self.Model = Model
        self.Column = Column
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.config.init_config(app)

    def allowed_file(self, filename):
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in self.config.allowed_extensions

    def save_files(self, model: Tuple, **kwargs) -> List[Dict[str, Any]]:
        """
        1. Get files from request
        2. Check that files exist in model
        3. Create list of dicts
        4.
        :param model: Sets the model attribute
        :param kwargs: files: List - request.files
        :return:
        """
        self.model = model
        file_data = []
        for k in kwargs.get("files").keys():
            file_data.append(self.create_file_dict(k))
        return file_data

    def create_file_dict(self, file):
        if file.filename != "" and file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mime_type = file.content_type
            file_type = filename.split(".")[1]
            return {
                f"{filename}__{self.Model.keys[0]}": filename,
                f"{filename}__{self.Model.keys[1]}": mime_type,
                f"{filename}__{self.Model.keys[2]}": file_type,
            }
        else:
            warn("Flask-File-Upload: No files were saved")
            return {}


    def update_model_attr(self):
        """
        Updates the model with attributes:
            - orig_name
            - mime_type
            - file_type
        :return:
        """
        pass

    def get_store_name(self, model):
        """TODO Attach to model"""
        model.store_name = f"{model.id}.{model.file_type}"

    def save_file(self, file, config):
        file.save(os.path.join(config["UPLOAD_FOLDER"]))

    def stream_file(self, model, **kwargs):
        """TODO """
        return send_from_directory(
            self.config["UPLOAD_FOLDER"],
            f"{model.id}"
            f"{self.get_file_ext(kwargs.get('filename'))}"
            f".{model['file_type']}",
            conditional=True,
        )

    def get_file_ext(self, filename):
        """
        This checks which file in the table we need to stream
        and returns the extension name
        :param filename:
        :return:
        """
        pass

    def get_file_url(self, model, **kwargs):
        """returns file url"""
        pass