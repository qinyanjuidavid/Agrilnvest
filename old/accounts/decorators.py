from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def administrator_required(function=None,
                           redirect_field_name=REDIRECT_FIELD_NAME,
                           login_url="/accounts/login/"):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == "Administrator" or u.is_admin == True,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator


def customer_required(function=None,
                      redirect_field_name=REDIRECT_FIELD_NAME,
                      login_url="/accounts/login/"):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == "Customer",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator


def dealer_required(function=None,
                    redirect_field_name=REDIRECT_FIELD_NAME,
                    login_url="/accounts/login/"):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == "Dealer",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator
