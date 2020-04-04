from django import forms

from .models import User, UserProfile


class BaseCustomModelForm(forms.ModelForm):
    def __init__(self, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def as_table(self):
        for field_name in self.errors:
            self.fields[field_name].widget.attrs.update({'class': 'form-control is-invalid'})

        return self._html_output(
            normal_row='<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%('
                       'help_text)s</td></tr>',
            error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<span class="form-text helptext">%s</span>',
            errors_on_separate_row=False,
        )


class UserForm(BaseCustomModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }


class UserProfileForm(BaseCustomModelForm):
    class Meta:
        model = UserProfile
        fields = ['voice_type']
