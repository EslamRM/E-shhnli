from registration.backends.default.views import RegistrationView
from .forms import ProfileForm
from .models import Profile


class MyRegistrationView(RegistrationView):

    form_class = ProfileForm

    def register(self, form_class):
        new_user = super(MyRegistrationView, self).register(form_class)
        full_name = form_class.cleaned_data['full_name']
        address_1 = form_class.cleaned_data['address_1']
        address_2 = form_class.cleaned_data['address_2']
        country = form_class.cleaned_data['country']
        state = form_class.cleaned_data['state']
        ZIP = form_class.cleaned_data['ZIP']
        phone_number = form_class.cleaned_data['phone_number']
        new_profile = Profile.objects.create(user=new_user,full_name=full_name,country=country,state=state,ZIP=ZIP,address_2=address_2,address_1=address_1,phone_number=phone_number)
        new_profile.save()
        return new_user