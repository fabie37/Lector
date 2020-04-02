

class RecordingForm(forms.ModelForm):
    class Meta:
        model = models.Recording
        fields = ('book', 'mp3file' )# TODO +username +duration
