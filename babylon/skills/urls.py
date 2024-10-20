from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings    
from . import views  # Import your views here

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('profile/', views.profile, name='profile'),  # User Profile page
    path('create-skill-exchange/', views.create_skill_exchange, name='create_skill_exchange'),  # Create Skill Exchange page
    path('skill-exchanges/', views.skill_exchange_list, name='skill_exchange_list'),  # List all Skill Exchanges
    path('skill-exchanges/<int:exchange_id>/', views.skill_exchange_detail, name='skill_exchange_detail'),  # Skill Exchange Detail page
    path('signup/', views.signup, name='signup'),  # User Signup page
    path('login/', views.login_user, name='login'),  # User Login page
    path('logout/', views.logout_user, name='logout'),
    path('feed/', views.feed, name='feed'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('bartending-matches/', views.find_bartending_matches, name='bartending_matches'),
     path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('exchange/<int:user_id>/', views.exchange_skills, name='exchange_skills'), # User Logout page
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
