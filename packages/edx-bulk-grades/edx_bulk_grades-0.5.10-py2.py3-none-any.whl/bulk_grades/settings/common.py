"""
Common Pluggable Django App settings
"""
from __future__ import absolute_import, unicode_literals


def plugin_settings(settings):
    """
    Injects local settings into django settings
    """
    settings.ANALYTICS_API_CLIENT = {
        'url': 'http://host.docker.internal:8000/api/v0',
        'token': 'edx'
    }
