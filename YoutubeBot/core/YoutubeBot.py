import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from config.settings import api_version, api_service_name
from core.Channel import YTChannel


class YoutubeBot:
    def __init__(self, client_secrets_file, scopes):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.youtube = self.get_authorization()
        self.channel = self.get_channel()

    def get_authorization(self):
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes)
        credentials = flow.run_console()
        return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    def get_channel(self, username=None):
        print('getchannel')
        request = self.youtube.channels().list(
            part="snippet",
            mine=False if username else True,
            forUsername=username
        )
        response = request.execute()
        user = response.get('items')[0]
        return YTChannel(username=user.get('snippet').get('title'),
                         channel_id=user.get('id'))

    def get_chat_messages(self):
        request = self.youtube.liveChatMessages().list(
            liveChatId=self.channel.id,
            part="snippet"
        )
        return request.execute()