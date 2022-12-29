from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreationForm(UserCreationForm):

    # CHOICES = [('S', 'Студент'), ('T', 'Викладач')]

    # status = forms.ChoiceField(
    #     choices=CHOICES,
    #     widget=forms.RadioSelect,
    #     label=_('Вкажіть ваш статус:'),
    #     required=True
    #     )
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2", "status")
