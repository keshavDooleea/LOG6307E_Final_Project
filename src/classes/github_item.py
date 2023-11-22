from dataclasses import dataclass

@dataclass
class GitHubItem:
    message: str
    chatgptSharing: str

    def __init__(self, message, chatgptSharing):
        self.message = message
        self.chatgptSharing = chatgptSharing

    def getItem(self):
        return {
            'message': self.message,
            'chatgptSharing': self.chatgptSharing
        }