from .module.answer import Answer
from .module.badge import Badge
from .module.comment import Comment
from .module.event import Event
from .module.info import Info
from .module.question import Question
from .module.post import Post
from .module.me import Me
from .module.privilege import Privilege
from .module.revision  import Revision
from .module.search    import Search
from .module.suggested_edit import SuggestedEdit
from .module.tag import Tag
from .module.user import User
from .network.network import Network

from .sites import Site


class StackExchangeClient:

    BASE_URL = 'https://api.stackexchange.com'
    VERSION = '2.2'

    def __init__(self, access_token=None, key=None, site=Site.STACKOVERFLOW):
        headers = {'access_token': access_token, 'key': key }
        url = "{}/{}".format(self.BASE_URL, self.VERSION)

        self.answers           = Answer(url, header=headers, site=site)
        self.badges            = Badge(url, header=headers, site=site)
        self.comments          = Comment(url, header=headers, site=site)
        self.events            = Event(url, header=headers, site=site)
        self.info              = Info(url, header=headers, site=site)
        self.me                = Me(url, header=headers, site=site)
        self.posts             = Post(url, header=headers, site=site)
        self.privileges        = Privilege(url, header=headers, site=site)
        self.questions         = Question(url, header=headers, site=site)
        self.revisions         = Revision(url, header=headers, site=site)
        self.search            = Search(url, header=headers, site=site)
        self.suggested_edits   = SuggestedEdit(url, header=headers, site=site)
        self.tags              = Tag(url, header=headers, site=site)
        self.users             = User(url, header=headers, site=site)
        self.network           = Network(url, header=headers)