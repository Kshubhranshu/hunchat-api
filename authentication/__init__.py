from django.conf import settings

import hashids


default_app_config = "authentication.apps.AuthenticationConfig"

HASH_IDS = hashids.Hashids(salt=settings.HASHID_SALT, min_length=12)
