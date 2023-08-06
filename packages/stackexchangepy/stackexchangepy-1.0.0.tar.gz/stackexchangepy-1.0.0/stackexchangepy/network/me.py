from stackexchangepy.helpers import format_ids, format_result


class Me:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def associated(self, **kwargs):
        """
        Returns a user's notifications.

        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/me/associated".format(self._url)
        result, remaining = format_result(url, name='AssociatedAccount', headers=self._header, params=kwargs)
        return (result, remaining)

    def merges(self, **kwargs):
        """
        Returns a record of merges that have occurred 
        involving the user.

        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/me/merges".format(self._url)
        result, remaining = format_result(url, name='Merge', headers=self._header, params=kwargs)
        return (result, remaining)
