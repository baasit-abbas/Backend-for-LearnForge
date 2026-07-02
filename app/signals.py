from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import User
from dotenv import load_dotenv
import os
load_dotenv()

@receiver(post_migrate)
def create_admin(sender,**kwargs):
    username = os.getenv('ADMIN_USERNAME')
    email = os.getenv('ADMIN_EMAIL')
    password = os.getenv('ADMIN_PASSWORD')
    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(
            username=username,
            email= email,
            password= password,
            role = User.Role.ADMIN
        )