from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser, Event, Booking ,Tag


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number")

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})

        if 'password' in self.fields:
            self.fields.pop('password')


class CustomAdminUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type', 'password', 'is_staff',
        #           'is_active', 'is_superuser', 'groups', 'user_permissions']
        fields = ['user_type', 'is_superuser',]


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}), label="Email")
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_incorrect': "Your old password was entered incorrectly. Please enter it again.",
        'password_mismatch': "The two password fields didn't match.",
        'password_too_short': "The new password must contain at least 8 characters.",
        'password_common': "The new password is too common. Please choose a different password.",
        'password_entirely_numeric': "The new password cannot be entirely numeric."
    }

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(self.error_messages['password_incorrect'])
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(self.error_messages['password_mismatch'])
            if len(password1) < 8:
                raise forms.ValidationError(self.error_messages['password_too_short'])
            if password1.isdigit():
                raise forms.ValidationError(self.error_messages['password_entirely_numeric'])
            if password1.lower() in ["password", "12345678", "qwerty"]:  # Example of a common password check
                raise forms.ValidationError(self.error_messages['password_common'])

        return password2


class EventForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Tags"
    )

    class Meta:
        model = Event
        fields = ['title', 'image', 'description', 'location', 'start_date', 'end_date', 'max_tickets', 'tags']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'student_id', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }