import json

from nameko.web.handlers import http
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy

from session import SessionProvider

class GatewayService:

    name = "gateway_service"

    storage_access_rpc = RpcProxy('storage_service')

    session_provider = SessionProvider()

    @http('POST', '/register')
    def add_user(self, request):
        data = request.json
        result = self.storage_access_rpc.add_user(data['username'], data['password'])
        return result
    
    @http('POST', '/login')
    def get_user(self, request):
        data = request.json
        result = self.storage_access_rpc.get_user(data['username'], data['password'])
        response = ""
        if result:
            session_id = self.session_provider.set_session(result)
            response = Response(str("Logged in as " + result[0]['username']))
            response.set_cookie('sessionID', session_id)
            return response
        else:
            response = Response(str("Account not found, please register!"))
            return response
    
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            session_data = self.session_provider.delete_session(cookies['sessionID'])
            response = Response('User Logged Out')
            return response
        else:
            response = Response('Currently Unable to Log Out')
            return response
        
    @http('POST', '/upload')
    def upload_file(self, request):
        cookies = request.cookies
        if cookies:
            user_data = self.session_provider.get_session(cookies['sessionID'])
            data = request.json
            result = self.storage_access_rpc.upload_file(data['content'], user_data[0]['username'])
            return result
        else:
            response = Response("Log in required to add file! Please log in.")
            return response
        
    @http('POST', '/download')
    def download_file(self, request):
        cookies = request.cookies
        if cookies:
            user_data = self.session_provider.get_session(cookies['sessionID'])
            data = request.json
            result = self.storage_access_rpc.download_file(data['id'], user_data[0]['username'])
            return json.dumps(result)
            # return result
        else:
            response = Response("Log in required to download file! Please log in.")
            return response