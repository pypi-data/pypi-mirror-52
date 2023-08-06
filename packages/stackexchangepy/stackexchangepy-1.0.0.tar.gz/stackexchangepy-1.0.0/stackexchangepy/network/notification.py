from stackexchangepy.helpers import format_ids, format_result


class Notification:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def all(self, **kwargs):
        """
        Returns a user's notifications.

        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/notifications".format(self._url)
        result, remaining = format_result(url, name='Notification', headers=self._header, params=kwargs)
        return (result, remaining)

    def unread(self, **kwargs):
        """
        Returns a user's unread notifications.

        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/notifications/unread".format(self._url)
        result, remaining = format_result(url, name='Notification', headers=self._header, params=kwargs)
        return (result, remaining)
