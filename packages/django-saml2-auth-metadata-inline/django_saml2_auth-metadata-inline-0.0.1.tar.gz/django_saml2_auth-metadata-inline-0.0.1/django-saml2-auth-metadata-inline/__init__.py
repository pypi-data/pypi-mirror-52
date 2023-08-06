from django.conf import settings

__version__ = '0.0.1'

from django_saml2_auth.plugins.metadata import MetadataPlugin


class DefaultMetadataHandler(MetadataPlugin):
    NAME = 'INLINE'

    def get_metadata(self):
        if 'METADATA_XML_STRING' in settings.SAML2_AUTH:
            return {
                'inline': [settings.SAML2_AUTH['METADATA_XML_STRING']]
            }


