from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from. const import GENDER_TYPE
from. models import UserAccount,UserAddress

class RegistrationsForm(UserCreationForm):
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    street=forms.CharField()
    city=forms.CharField()
    postal_code=forms.IntegerField()
    country=forms.CharField()
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','birth_date', 'gender','password1','password2', 'street','city','postal_code', 'country']

    def save(self,commit=True):
        current_user = super().save(commit=False)
        if commit==True:
            current_user.save()
            gender=self.cleaned_data.get('gender')
            birth_date=self.cleaned_data.get('birth_date')
            postal_code=self.cleaned_data.get('postal_code')
            city=self.cleaned_data.get('city')
            street=self.cleaned_data.get('street')
            country=self.cleaned_data.get('country')

            UserAddress.objects.create(
                user=current_user,
                postal_code=postal_code,
                city=city,
                street=street,
                country=country,
            )

            UserAccount.objects.create(
                user=current_user,
                birth_date=birth_date,
                gender=gender,
                account_no=100000+current_user.id
            )
        return current_user

class UpdateUserform(forms.ModelForm):
    birth_date=forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    street=forms.CharField()
    city=forms.CharField()
    postal_code=forms.IntegerField()
    country=forms.CharField()
    class Meta:
        model=User
        fields=['first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_account=self.instance.account
                user_address=self.instance.address
            except UserAccount.DoesNotExist:
                user_account=None
                user_address=None
            if user_account and user_address:
                self.fields['gender'].initial=user_account.gender
                self.fields['birth_date'].initial=user_account.birth_date   
                self.fields['street'].initial=user_address.street
                self.fields['city'].initial=user_address.city
                self.fields['postal_code'].initial=user_address.postal_code
                self.fields['country'].initial=user_address.country
    def save(self,commit=True):
        current_user=super().save(commit=False)
        if commit:
            current_user.save()
            user_account,created=UserAccount.objects.get_or_create(user=current_user)            
            user_address,created=UserAddress.objects.get_or_create(user=current_user)
            
            user_account.gender=self.cleaned_data['gender']
            user_account.birth_date=self.cleaned_data['birth_date']
            user_account.save()

            user_address.city=self.cleaned_data['city']
            user_address.street=self.cleaned_data['street']
            user_address.postal_code=self.cleaned_data['postal_code']
            user_address.country=self.cleaned_data['country']
            user_address.save()
        return current_user

class DepositForm(forms.Form):
    amount=forms.DecimalField()
    def clean(self):
        return super().clean()
