from django.conf import settings
from core.regbackend import MyRegistrationView
from django.contrib import admin
from django.urls import path ,include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

urlpatterns = [path('i18n/', include('django.conf.urls.i18n')),]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/register/', MyRegistrationView.as_view(),
         name='registration_register'),
    path('accounts/', include('registration.backends.default.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

