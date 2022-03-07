from django.db.models.signals import (
    post_save,
    post_migrate)
from django.dispatch import receiver
from accounts.models import (
    User, Administrator, Dealer, Customer, Counties, ResponseTime
)


@receiver(post_save, sender=User)
def create_users(sender, instance, created, *args, **kwargs):
    if created:
        if (instance.role == "Administrator" or
                instance.is_admin or instance.is_staff):
            Administrator.objects.update_or_create(user=instance)
        elif (instance.role == "Dealer"):
            Dealer.objects.update_or_create(user=instance)

        elif (instance.role == "Customer"):
            Customer.objects.update_or_create(
                user=instance
            )


@receiver(post_save, sender=User)
def Create_counties(sender, instance, created, *args, **kwargs):
    if created:
        counties = ["Mombasa", "Kwale", "Kilifi",
                    "Tana River", "Lamu", "Taita Taveta",
                    "Garissa", "Wajir", "Mandera",
                    "Marsabit", "Isiolo""Meru", "Tharaka-Nithi",
                    "Embu", "Kitui", "Machakos", "Makueni",
                    "Nyandarua", "Nyeri", "Kirinyaga", "Murang’a",
                    "Kiambu", "Turkana", "West Pokot",
                    "Samburu", "Trans-Nzoia", "Uasin Gishu",
                    "Elgeyo-Marakwet", "Nandi",
                    "Baringo", "Laikipia", "Nakuru", "Narok",
                    "Kajiado", "Kericho", "Bomet",
                    "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya",
                    "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"
                    ]
        for county in counties:
            if Counties.objects.filter(
               county=county
               ).exists():
                pass
            else:
                Counties.objects.update_or_create(
                    county=county
                )


@receiver(post_save, sender=User)
def Create_response_time(sender, instance, created, *args, **kwargs):
    if created:
        time = [
            "2 Hrs", "6 Hrs", "1 day", "2+ days"
        ]
        for time in time:
            if ResponseTime.objects.filter(response=time).exists():
                pass
            else:
                ResponseTime.objects.update_or_create(
                    response=time
                )
