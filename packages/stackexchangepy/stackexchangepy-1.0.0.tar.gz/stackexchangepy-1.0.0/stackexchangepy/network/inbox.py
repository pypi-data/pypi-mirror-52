from stackexchangepy.helpers import format_result


class Inbox:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def inbox(self, unread=False, **kwargs):
        """
        Returns the fields included by the given filters, 
        and the "safeness" of those filters.

        :kwarg unread:
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/users/inbox".format(self._url)

        if unread:
            url += "/unread"

        result, remaining = format_result(url, name='Message', headers=self._header, params=kwargs)
        return (result, remaining)