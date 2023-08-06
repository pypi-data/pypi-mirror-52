# django-saml2-auth-metadata-inline
A plugin to support inline metadata configuration in django-saml2-auth

# Introduction

By default, django-saml2-auth only supports metadata from a local file or a remote URL.  The underlying library supports
"inline" metadata i.e. a string in the settings file.  This makes it possible to follow the [12factor]() 
methodology because an environment variable can be used to provide this "inline" data.

# Example

In settings.py:

    INSTALLED_APPS += (
        ...
        'django_saml2_auth',
        # ensure the plugin is loaded
        'django_saml2_auth_metadata_inline',
        ...
    )
    
    
    
    # this is the "usual" config object from django-saml2-auth
    SAML2_AUTH = {
        'DEFAULT_NEXT_URL': '/',
        'PLUGINS': {
            # use this package in lieu of DEFAULT metadata plugin (or list both) 
            'METADATA': ['INLINE'],
        }
        # plugin looks for configuraiton here
        'METADATA_XML_STRING':  os.environ.get('SAML_CONFIG')
    }
