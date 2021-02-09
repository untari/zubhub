from django.conf import settings
from django.template.loader import render_to_string
from allauth.account.adapter import DefaultAccountAdapter
from django.template import TemplateDoesNotExist
from twilio.rest import Client

from .models import Location, Setting

from creators.tasks import send_text

from allauth.account import app_settings as allauth_settings


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        creator = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        location = Location.objects.get(name=data.get('location'))

        creator.phone = data.get("phone")
        creator.dateOfBirth = data.get('dateOfBirth')
        creator.bio = data.get('bio')
        creator.location = location
        creator.save()

        Setting(creator=creator, subscribe=data.get("subscribe")).save()

        return creator

    def confirm_phone(self, request, phone_number):
        """
        Marks the phone number as confirmed on the db
        """
        phone_number.verified = True
        phone_number.set_as_primary(conditional=True)
        phone_number.save()

    def get_from_phone(self):
        """
        This is a hook that can be overridden to programatically
        set the 'from' phone number for sending phone texts messages
        """
        return settings.DEFAULT_FROM_PHONE

    def render_text(self, template_name, phone, context):
        """
        Renders a text to `text`.  `template_prefix` identifies the
        text that is to be sent, e.g. "account/phone/phone_confirmation"
        """

        from_phone = self.get_from_phone()

        try:
            body = render_to_string(
                template_name,
                context,
                self.request,
            ).strip()
        except TemplateDoesNotExist:
            raise

        return {"to": phone, "from_": from_phone, "body": body}

    def send_text(self, template_name, phone, context):

        client = Client(settings.TWILIO_ACCOUNT_SID,
                        settings.TWILIO_AUTH_TOKEN)
        text = self.render_text(template_name, phone, context)
        client.messages.create(**text)

    def send_confirmation_text(self, request, phoneconfirmation, signup):

        ctx = {
            "user": phoneconfirmation.phone_number.user.username,
            "key": phoneconfirmation.key,
        }

        template_name = "account/phone/phone_confirmation.txt"

        send_text.delay(
            phone=phoneconfirmation.phone_number.phone,
            template_name=template_name,
            ctx=ctx,
        )
