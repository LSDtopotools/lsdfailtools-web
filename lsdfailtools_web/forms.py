from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadDataForm(FlaskForm):
    lsddata = FileField('LSDData', validators=[
        FileRequired(), FileAllowed(['csv'], 'csv files only')])
