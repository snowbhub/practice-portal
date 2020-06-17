from django import forms

from jobsapp.models import Job, Applicant, About


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'created_at',)

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('job',)

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('name', 'email', 'messages', )
class UpdateJobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateJobForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'lol',
            }
        )
        self.fields['last_date'].widget.attrs.update(
            {
                'input_type': 'date',
            }
        )


    class Meta:
        model = Job
        fields = ["title", "description", "location","last_date"]