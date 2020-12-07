from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,help_text=_("User"),primary_key=True)
    full_name = models.CharField(max_length=300, help_text=_("Full Name"))
    phone_number = PhoneNumberField(help_text=_("Phone number"))
    address_1 = models.CharField(max_length=500,help_text=_("Address 1"))
    address_2 = models.CharField(max_length=500,help_text=_("Address 2"),blank=True,null=True)
    country = models.CharField(max_length=300,help_text=_("Country"))
    state = models.CharField(max_length=300,help_text=_("State"))
    ZIP = models.CharField(max_length=300,help_text=_("ZIP"))

    class Meta:
        unique_together = ["user", "state", "full_name","country","ZIP"]

    def __str__(self):
        return self.full_name





class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewing', 'Reviewing'),
        ('Reviewed', 'Reviewed'),
        ('Charging', 'Charging'),
    ]
    user = models.ForeignKey(User,models.CASCADE,help_text=_("User"))
    logo_url = models.URLField(blank=True,help_text=_("logo url"))
    title = models.CharField(max_length=300,help_text=_("Title"))
    price = models.CharField(max_length=300,help_text=_("Price"))
    url = models.URLField(help_text=_("Url"),max_length=1000)
    img_url = models.URLField(blank=True,default='default.png',help_text=_("Image Url"),blank=True,null=True)
    category = models.CharField(max_length=300,help_text=_("Category"))
    color = models.CharField(max_length=300,help_text=_("Color"),blank=True,null=True)
    size = models.CharField(max_length=300,help_text=_("size"),blank=True,null=True)
    Qty = models.IntegerField(help_text=_("Qty"))
    statue = models.CharField(max_length=300,choices=STATUS_CHOICES,help_text=_("Statue"),default='Pending')
    promo = models.CharField(max_length=500, help_text=_('Promo Code'),blank=True,null=True)

    def __str__(self):
        return "%s -- request -- %s" % (self.user.profile.full_name, self.title)

class CommercialOrder(models.Model):
    user = models.ForeignKey(User,models.CASCADE,help_text=_("User"))
    title = models.CharField(max_length=300,help_text=_("Title"))
    quantity = models.IntegerField(default=1,help_text=_("Quantity"))
    price = models.CharField(max_length=300,help_text=_("Price"))
    details = models.TextField(help_text=_("Details"))
    file = models.FileField(upload_to='files/',help_text=_("Details File"),blank=True,null=True)

    def __str__(self):
        return "%s -- commercial order -- %s" % (self.user.profile.full_name, self.title)

class Calculator(models.Model):
    user = models.ForeignKey(User, models.CASCADE, help_text=_("User"))
    order = models.ForeignKey(Order, models.CASCADE, help_text=_("Order"))
    OnlinePrice = models.CharField(max_length=100,help_text=_('Online Price'),default=_('Calculating'))
    Customs = models.CharField(max_length=100,help_text=_('Customs'),default=_('Calculating'))
    VAT = models.CharField(max_length=100,help_text=_('VAT'),default=_('Calculating'))
    EShhnliFees = models.CharField(max_length=100,help_text=_('E-Shhnli Fees'),default=_('Calculating'))
    IntShipping = models.CharField(max_length=100,help_text=_('Int-Shipping'),default=_('Calculating'))
    DeliveryFees = models.CharField(max_length=100,help_text=_('Delivery Fees'),default=_('Calculating'))
    Subtotal = models.CharField(max_length=100,help_text=_('Subtotal'),default=_('Calculating'))
    Discount = models.CharField(max_length=100,help_text=_('Discount'),default=_('Calculating'))
    Total = models.CharField(max_length=100,help_text=_('Total'),default=_('Calculating'))

    def __str__(self):
        return "%s -- calculate order -- %s" % (self.user.profile.full_name, self.order.title)


class Subscribtion(models.Model):
    Platinum = 1
    More_Discount = 2
    No_Limits = 3
    SUB_CHOICES = (
        ('Platinum' , 'Platinum'),
        ('More_Discount' , 'More Discount'),
        ('No_Limits' , 'No Limits'),
    )
    user = models.ForeignKey(User, models.CASCADE, help_text=_("User"))
    subscribe = models.CharField(max_length=50,help_text=_("Subscribe"),choices=SUB_CHOICES)

    class Meta:
        unique_together = ["user", "subscribe"]


    def __str__(self):
        return "(%s) Subscribed to (%s Package)" % (self.user.username, self.subscribe)
