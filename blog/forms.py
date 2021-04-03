from django import forms
from django.db.models import fields
from .models import Post, BedRequest

PREGNANT=[('Yes', 'Yes'), ('No', 'No')]
WEIGHT = [('light', 'till 30'), ('medium', 'from 30 to 70'), ('heavy', "above 70")]
GENDER = [('Male', 'Male'),('Female', 'Female'), ('Other', 'Other')]
CITY = [('Mumbai', 'Mumbai'), ('Pune', 'Pune'), ('Nagpur', 'Nagpur'), ('Delhi', 'Delhi'), ('Noida', 'Noida'), ('Chandigarh', 'Chandigarh'), ('Amritsar', 'Amritsar')]
BOOKING = [(1, 'Allow Covid Bed Registration'),(2, 'Allow Bed Registration'), (3, 'Delete Entry')]
SCHEME = [('Life Insurance', 'Life Insurance'), ('Govt. Scheme','Govt. Scheme'), ('MSME Loan','MSME Loan')]
AREA =[('Andheri','Andheri'),('Worli','Worli'),('Bandra','Bandra'),('Breach Candy','Breach Candy'),('Thane','Thane'),('Ghatkopar','Ghatkopar'),('Friends Colony','Friends Colony'),('Hinjawadi','Hinjwadi'),('Chandini Chowk','Chandani Chowk')]
TYPE = [('Dedicated covid hospital', 'Dedicated covid hospital'), ('Dedicated covid health center','Dedicated covid health center'), ('Covid care center','Covid care center')]


class PostForm(forms.ModelForm):
    name =forms.CharField()
    content=forms.Textarea()
    type = forms.CharField(widget=forms.Select(choices=TYPE))
    
    proof=forms.ImageField(label="Address Proof")
    covid_cap=forms.IntegerField(label='Number of covid beds?')
    norm_cap = forms.IntegerField(label='Number of normal beds?')
    city = forms.CharField(widget=forms.Select(choices=CITY))
    area = forms.CharField(widget=forms.Select(choices=AREA))
    address = forms.Textarea()
    img1 = forms.ImageField(required=False)
    img2 = forms.ImageField(required=False)
    img3 = forms.ImageField(required=False)
    class Meta:
        model = Post
        fields = ['name', 'content', 'type', 'proof', 'covid_cap', 'norm_cap', 'city', 'area',
                   'address', 'img1', 'img2', 'img3'
                 ]

class BedForm(forms.ModelForm):
    aadhar_number =forms.IntegerField()
    phone_number =forms.IntegerField()
    email = forms.EmailField()
    name=forms.CharField(label='What is your name?')
    address=forms.CharField(label='What is your Address?')
    # proof=forms.ImageField()
    city=forms.CharField(label='What is your City?', widget=forms.Select(choices=CITY))
    pin_code =forms.IntegerField()
    gender=forms.CharField(label='What is your gender?',widget=forms.Select(choices=GENDER))
    age =forms.IntegerField()
    co_mobidity=forms.CharField(label='What are your comobidity?',widget=forms.Select(choices=PREGNANT))
    ambulance_required=forms.CharField(label='Do you require an ambulance?',widget=forms.Select(choices=PREGNANT))
    scheme=forms.CharField(label='Scheme to apply for',widget=forms.Select(choices=SCHEME))

    # preferance=forms.CharField(label='What is your gender?',widget=forms.Select(choices=GENDER))
    # health_centre=forms.CharField(label='What is your gender?',widget=forms.Select(choices=GENDER))
    # district=forms.CharField(max_length=10)
    # Hospital=forms.CharField(max_length=10, label='Nearby hospitals?')

    tested = forms.CharField(label='Was your COVID test positive?',widget=forms.Select(choices=PREGNANT))

    # is_donor = forms.BooleanField(required=False)

    symptoms = forms.Textarea()

    class Meta:
        model= BedRequest
        fields=('aadhar_number', 'name', 'email', 'phone_number', 'address' , 'city', 'pin_code',  'age', 'gender', 
             'co_mobidity', 'ambulance_required', 'scheme', 'tested','symptoms'
        #   'proof',
        )

class Booking(forms.ModelForm):
    choice=forms.CharField(widget=forms.Select(choices=BOOKING))
    class Meta:
        model= Post
        fields = ["choice"]

class Search(forms.ModelForm):
    search=forms.CharField()
    class Meta:
        model= Post
        fields = ["search"]

