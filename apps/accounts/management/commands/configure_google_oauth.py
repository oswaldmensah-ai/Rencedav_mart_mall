from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Create or update the Google OAuth SocialApp from environment variables.'

    def handle(self, *args, **options):
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        if not client_id or not client_secret or client_id == 'your_google_client_id':
            raise CommandError('GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be configured.')

        site_url = settings.SITE_URL.rstrip('/')
        parsed_url = urlparse(site_url)
        domain = parsed_url.netloc or parsed_url.path
        if not domain:
            raise CommandError('SITE_URL must contain a valid domain.')

        site, _ = Site.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={'domain': domain, 'name': settings.SITE_NAME},
        )
        app = SocialApp.objects.filter(provider='google').order_by('id').first()
        if app is None:
            app = SocialApp(provider='google')
        app.name = 'Google'
        app.client_id = client_id
        app.secret = client_secret
        app.key = ''
        app.save()
        SocialApp.objects.filter(provider='google').exclude(pk=app.pk).delete()
        app.sites.set([site])
        self.stdout.write(self.style.SUCCESS('Google OAuth SocialApp configured.'))
