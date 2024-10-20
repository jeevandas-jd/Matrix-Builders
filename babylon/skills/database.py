from .models import UserProfile, Skill

class Database:
    def get_users(self):
        # Return all user profiles
        return UserProfile.objects.all()

    def get_skills(self):
        # Return all skills
        return Skill.objects.all()

    def has_skill(self, user, skill):
        # Check if a user has a specific skill
        return user.skills_offered.filter(id=skill.id).exists()
