from .access_token import AccessToken
from .app import App
from .error import Error
from .filter import Filter
from .inbox import Inbox
from .me import Me
from .notification import Notification
from .site import Site
from .user import User

class Network:

  def __init__(self, url, header):
    self.acess_tokens   = AccessToken(url, header)
    self.apps           = App(url, header)
    self.errors         = Error(url, header)
    self.filters        = Filter(url, header)
    self.inbox          = Inbox(url, header)
    self.me             = Me(url, header)
    self.notifications  = Notification(url, header)
    self.sites          = Site(url, header)
    self.users          = User(url, header)