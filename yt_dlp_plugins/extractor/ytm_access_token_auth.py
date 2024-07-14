from yt_dlp.extractor.youtube import YoutubeIE
from yt_dlp.networking import Request

# ⚠ The class name must end in "IE"
class YoutubeMusicAccessTokenAuthHandlerIE(YoutubeIE, plugin_name='yt_access_token'):

    def _inject_auth_header(self, request: Request):
        self.write_debug("Injecting auth header")
        # These are only require for cookies and interfere with OAuth2
        request.headers.pop('X-Goog-PageId', None)
        request.headers.pop('X-Goog-AuthUser', None)
        # In case user tries to use cookies at the same time
        if 'Authorization' in request.headers:
            self.report_warning(
                'Youtube cookies have been provided, but OAuth2 is being used.'
                ' If you encounter problems, stop providing Youtube cookies to yt-dlp.')
            request.headers.pop('Authorization', None)
            request.headers.pop('X-Origin', None)

        # Not even used anymore, should be removed from core...
        request.headers.pop('X-Youtube-Identity-Token', None)

        authorization_header = {'Authorization': f'{self.auth}'}
        request.headers.update(authorization_header)

    def _perform_login(self, username, password):
        self.write_debug("Performing login YTM Accesstoken")
        self.auth = password

    def _create_request(self, *args, **kwargs):
        request = super()._create_request(*args, **kwargs)
        self._inject_auth_header(request)
        return request