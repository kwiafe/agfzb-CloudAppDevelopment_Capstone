from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    # path for about view
    path('about/', views.about, name='about'),
    # path for contact us view
    path('contact/', views.contact, name='contact'),
    # path for registration

    # path for login
    path('login/', views.custom_login, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),

    path('signup/', views.registration_request, name='signup'),

    path(route='', view=views.get_dealerships, name='index'),

    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for dealer reviews view

    # path for add a review view
    path('add_review/<int:dealer_id>/', views.add_review, name='add_review'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)