from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadDataForm(FlaskForm):
    coordinates = FileField('Coordinates', validators=[
        FileRequired(), FileAllowed(['csv'], 'csv files only')])
    precipitation = FileField('Precipitation', validators=[
        FileRequired(), FileAllowed(['csv'], 'csv files only')])
