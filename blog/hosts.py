from django.conf import settings
from django_hosts import patterns, host


host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'blog', settings.ROOT_URLCONF, name='blog'),
    host(r'(\w+)', 'blog.hostsconfig.urls', name='not-found'),
    # host(r'admin', 'blog.urls.admin_urls', name='admin'),
    
    
)