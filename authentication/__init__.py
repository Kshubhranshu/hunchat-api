import hashids
from django.conf import settings

default_app_config = "authentication.apps.AuthenticationConfig"

HASH_IDS = hashids.Hashids(salt=settings.HASHID_SALT, min_length=12)
