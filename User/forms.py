from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . constant import  GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserLibraryAccount, UserAddress
from django.db import models

class UserRegistrationForm(UserCreationForm):
    reference_code = forms.IntegerField()
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'})) #ke o faka rakhle o somossa nai
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name' , 'last_name','email','reference_code',
        'birth_date','gender','postal_code','city','country','street_address']

    def save(self, commit=True):
        our_user = super().save(commit=False) #ami database e data save korbo na ekhon
        if commit == True:
            our_user.save() #user model e data save korlam
            reference_code = self.cleaned_data.get('reference_code')
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')

            UserAddress.objects.create(
                user = our_user,
                postal_code = postal_code,
                country = country, 
                city = city, 
                street_address = street_address,
            )
            UserLibraryAccount.objects.create(
                user = our_user,
                reference_code =  reference_code,
                gender = gender,
                birth_date = birth_date ,
                account_no = 100000+ our_user.id, 
            )     
        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            # print(field)
            self.fields[field].widget.attrs.update(
                {
                    'class':(
                            'appearance-none block w-full bg-gray-200 '
                            'text-gray-700 border border-gray-200 rounded '
                            'py-3 px-4 leading-tight focus:outline-none '
                            'focus:bg-white focus:border-gray-500'
                    )
                }
            )


class UserUpdateForm(forms.ModelForm):
    reference_code = forms.CharField(max_length=11)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'})) #ke o faka rakhle o somossa nai
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    class Meta:
        
        model = User
        fields = ['first_name', 'last_name','email']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            # print(field)
            self.fields[field].widget.attrs.update(
                {
                    'class':(
                            'appearance-none block w-full bg-gray-200 '
                            'text-gray-700 border border-gray-200 rounded '
                            'py-3 px-4 leading-tight focus:outline-none '
                            'focus:bg-white focus:border-gray-500'
                    )
                }
            )
        
        #jodi user er account thake
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserLibraryAccount.DoesNotExist:
                user_account = None
                user_address = None
            
            if user_account:
                self.fields['reference_code'].initial = user_account.reference_code
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['gender'].initial = user_account.gender
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account , created = UserLibraryAccount.objects.get_or_create(user=user) #jodi account thake taile seta jabe get account e and jodi user na thake taile seta jabe create account e
            user_address , created = UserAddress.objects.get_or_create(user=user)


            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.gender = self.cleaned_data['gender']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()
        return user
          

        
    