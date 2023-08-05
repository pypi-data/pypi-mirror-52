from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from djoser.conf import settings as djoser_settings
from djoser.utils import decode_uid

import graphene


from .serializers import PasswordResetConfirmRetypeSerializer
from .utils import send_activation_email, send_password_reset_email

UserModel = get_user_model()

class Register(graphene.Mutation):
    """
    Mutation to register a user
    """
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_repeat = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, password, password_repeat):
        if password == password_repeat:
            try:
                user = UserModel.objects.create(
                    email=email,
                    is_active=False
                    )
                user.set_password(password)
                user.save()
                if djoser_settings.SEND_ACTIVATION_EMAIL:
                    send_activation_email(user, info.context)
                return Register(success=bool(user.id))
            # TODO: specify exception
            except Exception:
                errors = ["email", "Email already registered."]
                return Register(success=False, errors=errors)
        errors = ["password", "Passwords don't match."]
        return Register(success=False, errors=errors)


class Activate(graphene.Mutation):
    """
    Mutation to activate a user's registration
    """
    class Arguments:
        token = graphene.String(required=True)
        uid = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, token, uid):

        try:
            uid = decode_uid(uid)
            user = UserModel.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                return Activate(success=False, errors=['stale token'])
                pass
            user.is_active = True
            user.save()
            return Activate(success=True, errors=None)

        except Exception:
            return Activate(success=False, errors=['unknown user'])


class ResetPassword(graphene.Mutation):
    """
    Mutation for requesting a password reset email
    """

    class Arguments:
        email = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, email):
        try:
            user = UserModel.objects.get(email=email)
            send_password_reset_email(info.context, user)
            return ResetPassword(success=True)
        except Exception:
            return ResetPassword(success=True)


class ResetPasswordConfirm(graphene.Mutation):
    """
    Mutation for requesting a password reset email
    """

    class Arguments:
        uid = graphene.String(required=True)
        token = graphene.String(required=True)
        email = graphene.String(required=True)
        new_password = graphene.String(required=True)
        re_new_password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, uid, token, email, new_password, re_new_password):
        serializer = PasswordResetConfirmRetypeSerializer(data={
            'uid': uid,
            'token': token,
            'email': email,
            'new_password': new_password,
            're_new_password': re_new_password,
        })
        if serializer.is_valid():
            serializer.user.set_password(serializer.data['new_password'])
            serializer.user.save()
            return ResetPasswordConfirm(success=True, errors=None)
        else:
            return ResetPasswordConfirm(
                success=False, errors=[serializer.errors])


class DeleteAccount(graphene.Mutation):
    """
    Mutation to delete an account
    """
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, password):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
        elif is_authenticated and not email == info.context.user.email:
            errors = ['forbidden']
        elif not info.context.user.check_password(password):
            errors = ['wrong password']
        else:
            info.context.user.delete()
            return DeleteAccount(success=True)
        return DeleteAccount(success=False, errors=errors)
