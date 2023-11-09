from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from modules.accounts.models import Constants, RoleChoices, SuperUser, TrackingModel

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    """
    Signal receiver function to create user profiles
    when a new user is created.

    Args:
        sender (User): The sender of the signal.
        instance (User): The instance of the User model being saved.
        created (bool): Indicates whether the user instance was just created.
        **kwargs: Additional keyword arguments passed to the function.
    """
    if created:
        if (
            instance.role == RoleChoices.SUPERUSER
            or instance.is_superuser
            or instance.is_staff
        ):
            SuperUser.objects.get_or_create(user=instance)


@receiver(pre_save)
def set_added_by_updated_by(sender, instance, **kwargs):
    """
    Signal handler to set added_by and updated_by fields before
    saving the object.

    Args:
        sender (Type): The model class.
        instance: The instance of the model.
        **kwargs: Additional keyword arguments passed to the function.
    """
    if issubclass(sender, TrackingModel):
        if hasattr(instance, "request") and instance.request.user.is_authenticated:
            user = (
                instance.request.user
            )  # Obtain the current user from the request object
        else:
            user = None  # If request or user is not available, set to None or handle as needed

        print("User----> ", user)
        # Check if the instance is being created (not updated) and set added_by
        if instance._state.adding and not instance.added_by:
            instance.added_by = user

        # Always set updated_by before saving
        instance.updated_by = user


@receiver(pre_save)
def set_updated_flag(sender, instance, **kwargs):
    """
    Signal handler to set the updated_flag field before saving the object.

    Args:
        sender (Type): The model class.
        instance: The instance of the model.
        **kwargs: Additional keyword arguments passed to the function.
    """
    if (
        isinstance(instance, TrackingModel)
        and not instance._state.adding
        and not instance.updated_by
    ):
        instance.updated_flag = Constants.YES

        # Get the current user making the update
        user = instance.request.user if hasattr(instance, "request") else None

        # Set the updated_by field
        instance.updated_by = user
