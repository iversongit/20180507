from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from shopper.models import session


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        if request.path == '/shopapp/login/' or request.path == '/shopapp/regist/':
            return None
        ticket = request.COOKIES.get("ticket")
        if not ticket:
            return HttpResponseRedirect('/shopapp/login/')
        sessions = session.objects.filter(session_data=ticket)
        if sessions:
            request.user = sessions[0].u
            return None
        return HttpResponseRedirect('/shopapp/login/')
