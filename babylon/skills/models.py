from django.contrib.auth.models import User
from django.db import models

# Skill model that categorizes the skills available for barter
class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Profile model for the user with additional details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    skills_offered = models.ManyToManyField(Skill, related_name='users_offering', blank=True)
    skills_requested = models.ManyToManyField(Skill, related_name='users_requesting', blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)
    is_professional = models.BooleanField(default=False)  # New field to identify professionals
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # For paid professionals
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def has_skill(self, skill):
        return self.skills_offered.filter(id=skill.id).exists()


    def __str__(self):
        return self.user.username
# Model for skill exchange proposals between two users
"""class SkillExchange(models.Model):
    OFFER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

    offered_by = models.ForeignKey(UserProfile, related_name='offerer', on_delete=models.CASCADE)
    requested_by = models.ForeignKey(UserProfile, related_name='requester', on_delete=models.CASCADE)
    skills_offered = models.ManyToManyField(Skill, related_name='offered_skills')
    skills_requested = models.ManyToManyField(Skill, related_name='requested_skills')
    status = models.CharField(max_length=20, choices=OFFER_STATUS_CHOICES, default='PENDING',null=False)
    is_paid_service = models.BooleanField(default=False)  # New field for paid services
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Price for paid exchanges
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.offered_by} <--> {self.requested_by} ({self.status})"
        
"""

class SkillExchange(models.Model):
    initiator = models.ForeignKey(User, related_name='initiated_exchanges', on_delete=models.CASCADE, default=1)
    target = models.ForeignKey(User, related_name='targeted_exchanges', on_delete=models.CASCADE, default=1)  # Set default user ID for 'target'
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.initiator.username} wants to exchange skills with {self.target.username}"

# Review model for post-exchange feedback
class Review(models.Model):
    exchange = models.OneToOneField(SkillExchange, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(UserProfile, related_name='reviews_given', on_delete=models.CASCADE)
    reviewee = models.ForeignKey(UserProfile, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review from {self.reviewer} to {self.reviewee}"

# Gamification badges for users based on activity
class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    users = models.ManyToManyField(UserProfile, related_name='badges', blank=True)

    def __str__(self):
        return self.name
   
# Tracking the badges earned by users
class UserBadge(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} earned {self.badge} on {self.awarded_at}"
