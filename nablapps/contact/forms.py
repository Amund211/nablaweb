from django import forms

class ContactForm(forms.Form):
    your_name = forms.CharField(label='Ditt navn', max_length=100)
    email = forms.EmailField(label='Din e-post:', max_length=100)
    subject = forms.CharField(label='Emne', max_length=100)
    message = forms.CharField(label='Melding', widget=forms.Textarea)

    def process(self):
        cd = self.cleaned_data
        name = cd['your_name']
        email = cd['email']
        subject = cd['subject']
        message = cd['message']

        return name, email, subject, message

