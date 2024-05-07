from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee

class EmployeeCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'home_team', 'employment_type', 'managed_teams', 'password1', 'password2')
