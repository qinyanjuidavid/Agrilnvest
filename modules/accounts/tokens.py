# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# import six


# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_has_value(self, user, timestamp):
#         return (
#             six.text_type(user.pk)
#             + six.text_type(timestamp)
#             + six.text_type(user.is_active)
#         )


# account_activation_token = TokenGenerator()
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils import timezone


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation.
    """

    def _make_hash_value(self, user):
        """
        Generate a unique hash value for the token.

        Args:
            user (User): The user object for whom the token is generated.
            timestamp (datetime): The timestamp when the token is generated.

        Returns:
            str: Unique hash value for the token.
        """
        return (
            six.text_type(user.pk)
            + six.text_type(user.timestamp)
            + six.text_type(user.is_active)
            + six.text_type(user.email)  # Add more user-specific data if needed
        )

    def check_token_expiry(self, token):
        """
        Check if the token has expired based on the created_at timestamp.

        Args:
            token (Token): The token object to be checked for expiration.

        Returns:
            bool: True if the token is still valid, False if it has expired.
        """
        # Check if the token is expired
        expiration_time = timezone.now() - timezone.timedelta(
            days=1
        )  # Set expiration to 1 day
        return token.created_at > expiration_time

    def make_token(self, user):
        """
        Generate a token for the specified user and set the created_at timestamp.

        Args:
            user (User): The user object for whom the token is generated.

        Returns:
            Token: Token object with the created_at timestamp set.
        """
        # Generate a token and set the created_at timestamp
        token = self._make_hash_value(user)
        return token


account_activation_token = TokenGenerator()
