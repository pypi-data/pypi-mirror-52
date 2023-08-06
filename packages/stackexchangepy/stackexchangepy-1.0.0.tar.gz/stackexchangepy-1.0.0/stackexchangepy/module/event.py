from stackexchangepy.helpers import format_result


class Event:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Events.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def get(self, **kwargs):
        """
        Returns a stream of events that have occurred on the site.

        The API considers the following "events":

        posting a question
        posting an answer
        posting a comment
        editing a post
        creating a user

        :kwarg.page: from which page events to be returned
        :kwarg pagesize: how many events to be returned
        :kwarg since: from when events to be returned, must be a valid datetime object
        """
        url = "{}/events".format(self._url)
        result, remaining = format_result(url, name='Event', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)