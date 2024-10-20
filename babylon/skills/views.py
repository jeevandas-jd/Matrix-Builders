from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Skill, SkillExchange, Review, Badge, UserBadge
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .database import *

# Homepage view
def home(request):
    return render(request, 'home.html')

# View to create/update user profile


"""def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        skills_offered = request.POST.getlist('skills_offered')
        skills_requested = request.POST.getlist('skills_requested')
        is_professional = request.POST.get('is_professional') == 'on'  # Check if professional checkbox is selected
        hourly_rate = request.POST.get('hourly_rate') if is_professional else None

        # Update profile details
        user_profile.bio = bio
        user_profile.location = location
        user_profile.is_professional = is_professional
        user_profile.hourly_rate = hourly_rate if hourly_rate else None
        user_profile.skills_offered.clear()  # clear the existing skill list
        user_profile.skills_requested.clear()

        # Add new skills
        for skill_id in skills_offered:
            skill = get_object_or_404(Skill, id=skill_id)
            user_profile.skills_offered.add(skill)
        
        for skill_id in skills_requested:
            skill = get_object_or_404(Skill, id=skill_id)
            user_profile.skills_requested.add(skill)

        user_profile.save()
        return redirect('profile')  # Redirect to profile after update

    skills = Skill.objects.all()
    return render(request, 'profile.html', {'user_profile': user_profile, 'skills': skills})
"""
@login_required
@login_required
def profile(request):
    # Attempt to get the user profile
    user_profile = UserProfile.objects.filter(user=request.user).first()

    # Check if the user profile exists
    if user_profile is None:
        # If not, redirect to edit_profile to create one
        messages.info(request, "Please set up your profile.")
        return redirect('edit_profile')

    # Render the profile view if the user profile exists
    return render(request, 'profile.html', {'user_profile': user_profile})
# View to list all available skill exchanges
@login_required
def skill_exchange_list(request):
    exchanges = SkillExchange.objects.filter(status='PENDING')
    return render(request, 'skill_exchange_list.html', {'exchanges': exchanges})

# View to create a skill exchange request
@login_required
@login_required
def create_skill_exchange(request):
    if request.method == 'POST':
        offered_by = UserProfile.objects.get(user=request.user)
        requested_by_id = request.POST.get('requested_by')
        requested_by = get_object_or_404(UserProfile, id=requested_by_id)
        skills_offered = request.POST.getlist('skills_offered')
        skills_requested = request.POST.getlist('skills_requested')
        is_paid_service = 'is_paid_service' in request.POST
        price = request.POST.get('price') if is_paid_service else None

        # Create skill exchange instance
        exchange = SkillExchange.objects.create(
            offered_by=offered_by,
            requested_by=requested_by,
            is_paid_service=is_paid_service,
            price=price if is_paid_service else None
        )

        # Add offered and requested skills
        for skill_id in skills_offered:
            skill = get_object_or_404(Skill, id=skill_id)
            exchange.skills_offered.add(skill)

        for skill_id in skills_requested:
            skill = get_object_or_404(Skill, id=skill_id)
            exchange.skills_requested.add(skill)

        exchange.save()
        return redirect('skill_exchange_list')  # Redirect to skill exchange list

    users = UserProfile.objects.exclude(user=request.user)
    skills = Skill.objects.all()
    return render(request, 'create_skill_exchange.html', {'users': users, 'skills': skills})


# View to handle skill exchange details and updates
@login_required
def skill_exchange_detail(request, exchange_id):
    exchange = get_object_or_404(SkillExchange, id=exchange_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        exchange.status = status
        exchange.save()

        return redirect('skill_exchange_detail', exchange_id=exchange.id)

    return render(request, 'skill_exchange_detail.html', {'exchange': exchange})

# View to leave a review after a completed exchange
@login_required
def leave_review(request, exchange_id):
    exchange = get_object_or_404(SkillExchange, id=exchange_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        # Check if the review already exists
        if not Review.objects.filter(exchange=exchange).exists():
            review = Review.objects.create(
                exchange=exchange,
                reviewer=UserProfile.objects.get(user=request.user),
                reviewee=exchange.requested_by if request.user != exchange.requested_by.user else exchange.offered_by,
                rating=rating,
                feedback=feedback
            )
            review.save()
        
        return redirect('skill_exchange_list')

    return render(request, 'leave_review.html', {'exchange': exchange})

# View for badges
@login_required
def badges(request):
    user_profile = UserProfile.objects.get(user=request.user)
    badges = user_profile.badges.all()
    return render(request, 'badges.html', {'badges': badges})


# Signup view
"""def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome, {username}! Your account has been created.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        errors = []

        # Custom validation logic
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        if password != password_confirm:
            errors.append("Passwords do not match.")
        
        # Additional custom password validation can be added here if needed

        # If there are errors, show them
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'signup.html', {'username': username})

        # If validation passes, create the user
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('login')  # Redirect to login page after successful signup

    return render(request, 'signup.html')

# Login view
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')

# Logout view
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required




def feed(request):
    try:
        # Get all user profiles except the current logged-in user
        all_profiles = UserProfile.objects.exclude(user=request.user)

        context = {
            'profiles': all_profiles
        }

        return render(request, 'feed.html', context)

    except Exception as e:
        print(f"Error in feed view: {e}")
        return render(request, '404.html', status=404)

@login_required



def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    all_skills = Skill.objects.all()  # Fetch all skills

    if request.method == 'POST':
        bio = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        skills_offered = request.POST.getlist('skills_offered')  # Get list of skills offered
        skills_requested = request.POST.getlist('skills_requested')  # Get list of skills requested
        profile_photo = request.FILES.get('profile_photo')  # Get the uploaded image file

        # Update user profile fields
        user_profile.bio = bio
        user_profile.location = location

        # Clear existing skills and add new ones
        user_profile.skills_offered.clear()
        for skill_id in skills_offered:
            skill = get_object_or_404(Skill, id=skill_id)
            user_profile.skills_offered.add(skill)

        user_profile.skills_requested.clear()
        for skill_id in skills_requested:
            skill = get_object_or_404(Skill, id=skill_id)
            user_profile.skills_requested.add(skill)

        if profile_photo:
            user_profile.profile_photo = profile_photo  # Update the profile photo

        user_profile.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user_profile': user_profile, 'all_skills': all_skills})


def find_bartending_matches(request):
    try:
        bartending_skill = Skill.objects.get(name="Bartending")
        
        # Users offering bartending skills
        users_offering_bartending = UserProfile.objects.filter(
            skills_offered=bartending_skill
        ).exclude(user=request.user)

        # Users requesting bartending skills
        users_requesting_bartending = UserProfile.objects.filter(
            skills_requested=bartending_skill
        ).exclude(user=request.user)

        # Prepare the context with both sets of users
        context = {
            'offering_bartending': users_offering_bartending,
            'requesting_bartending': users_requesting_bartending,
        }
        
        return render(request, 'bartending_matches.html', context)

    except Exception as e:

        print(e)
        # If the 'Bartending' skill does not exist in the database
        return redirect("home")

class RecommendationModel:
    def __init__(self, skill_matrix):
        self.skill_matrix = skill_matrix

    def FindSimilarUser(self, user_id, top_n=5):
        user_vector = self.skill_matrix[user_id].reshape(1, -1)
        similarities = cosine_similarity(self.skill_matrix, user_vector).flatten()
        # Ensure you don't exceed the bounds of the array
        similar_indices = np.argsort(-similarities)[1:top_n + 1]
        return similar_indices, similarities[similar_indices][:top_n]


class matchservice:
    def __init__(self, db):
        self.db = db
        self.model = RecommendationModel(self.load_matrix())

    def load_matrix(self):
        users = self.db.get_users()
        skills = self.db.get_skills()
        skill_matrix = np.array([[user.has_skill(skill) for skill in skills] for user in users])
        print(f"Number of users: {len(users)}")  # Debugging line
        print(f"Skill matrix shape: {skill_matrix.shape}")
        return skill_matrix
    def find_matches_for_user(self, user_id):
        similar_users, scores = self.model.FindSimilarUser(user_id)
        print(f"Found similar users: {similar_users}")  # Debugging line
        print(f"Scores: {scores}")  # Debugging line
        matches = [{"user_id": user, "score": score} for user, score in zip(similar_users, scores)]
        return matches


def find_bartending_matches(request):
    try:
        # Get the current user's profile or return a 404 if not found
        print("hello 1")
        user_profile = get_object_or_404(UserProfile, user=request.user)
        print("hello 2")
        db=Database()
        print("hello 3")
        # Initialize matchservice using the UserProfile objects directly
        matcher = matchservice(db)  # No need to pass a db instance
        print("hello 4")
        user_id = user_profile.id
        print("hello 5")
        
        # Find matches for the current user
        matches = matcher.find_matches_for_user(user_id)
        print("hello 6")

        print("model run successfully!!")

        print(matches)
        print("hello 7")

        # Fetch matched profiles based on matched user IDs
        matched_profiles = UserProfile.objects.filter(id__in=[match['user_id'] for match in matches])
        print("hello 8")

        # Prepare context for rendering
        context = {
            'matched_profiles': matched_profiles,
            'matches': matches
        }

        return render(request, 'bartending_matches.html', context)

    except Exception as e:
        print(e)
        return render(request, '404.html', status=404)
def profile_view(request, user_id):
    profile = get_object_or_404(UserProfile, user_id=user_id)

    context = {
        'profile': profile
    }
    
    return render(request, 'profile.html', context)

def exchange_skills(request, user_id):
    target_profile = get_object_or_404(UserProfile, user_id=user_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        # Example logic to create a skill exchange record
        skill_exchange = SkillExchange.objects.create(
            initiator=user_profile.user,
            target=target_profile.user,
            status="Pending"
        )
        skill_exchange.save()
        return redirect('profile_view', user_id=user_id)

    return render(request, 'exchange_skills.html', {'profile': target_profile})