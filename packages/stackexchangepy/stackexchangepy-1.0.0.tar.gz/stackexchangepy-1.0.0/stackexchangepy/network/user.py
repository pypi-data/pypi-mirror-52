from stackexchangepy.helpers import format_result


class User:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def associated(self, ids, **kwargs):
        """
        Returns all of a user's associated 
        accounts, given their account_ids in {ids}.

        :param ids: users ids
        :kwarg page:
        :kwarg pagesize:
        :kwarg types:
        """
        ids = format_id(ids) if type(ids) == str else ';'.join([str(acc_id) for acc_id in ids])
        url = "{}/users/{}/associated".format(self._url, ids)
        result, remaining = format_result(url, name='AssociatedAccount', headers=self._header, params=kwargs)
        return (result, remaining)

    def merges(self, ids, **kwargs):
        """
        Returns a record of merges that have occurred 
        involving the passed account ids.

        :param ids: users ids
        :kwarg page:
        :kwarg pagesize:
        """
        ids = format_id(ids) if type(ids) == str else ';'.join([str(acc_id) for acc_id in ids])
        url = "{}/users/{}/merges".format(self._url, ids)
        result, remaining = format_result(url, name='Merge', headers=self._header, params=kwargs)
        return (result, remaining)
