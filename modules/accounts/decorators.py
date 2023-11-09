from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from modules.accounts.models import RoleChoices


def superuser_required(
    function=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url="/accounts/login/",
):
    """
    Decorator to restrict access to views for superusers.

    Args:
        function (function, optional): The view function to be decorated. Defaults to None.
        redirect_field_name (str, optional): The name of the redirect field. Defaults to "next".
        login_url (str, optional): The URL to redirect to if the user is not authenticated.
        Defaults to "/accounts/login/".

    Returns:
        function: Decorated view function restricted to superusers.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.role == RoleChoices.SUPERUSER or u.is_superuser),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)

    return actual_decorator


def customer_required(
    function=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url="/accounts/login/",
):
    """
    Decorator to restrict access to views for customers.

    Args:
        function (function, optional): The view function to be decorated. Defaults to None.
        redirect_field_name (str, optional): The name of the redirect field. Defaults to "next".
        login_url (str, optional):
        The URL to redirect to if the user is not authenticated. Defaults to "/accounts/login/".

    Returns:
        function: Decorated view function restricted to customers.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == RoleChoices.CUSTOMER,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)

    return actual_decorator


def farmer_required(
    function=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url="/accounts/login/",
):
    """
    Decorator to restrict access to views for farmers.

    Args:
        function (function, optional): The view function to be decorated. Defaults to None.
        redirect_field_name (str, optional): The name of the redirect field. Defaults to "next".
        login_url (str, optional):
        The URL to redirect to if the user is not authenticated. Defaults to "/accounts/login/".

    Returns:
        function: Decorated view function restricted to farmers.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == RoleChoices.FARMER,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)

    return actual_decorator
