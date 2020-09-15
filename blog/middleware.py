from django.utils.translation import ugettext as _
from django.utils import translation


class LangSessionMiddletware:
    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # if not request.session.get('lang'):
        #     request.session['lang'] = 'en'
        #     maybe in future

        translation.activate('ar')
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
