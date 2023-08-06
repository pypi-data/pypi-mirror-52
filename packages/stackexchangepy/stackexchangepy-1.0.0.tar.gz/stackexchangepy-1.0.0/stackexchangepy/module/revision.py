from stackexchangepy.helpers import format_ids, format_result


class Revision:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Revisions.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def ids(self, ids, **kwargs):
        """

        :param ids:
        :kwarg page:
        :kwarg pagesize:
        :kwarg fromdate:
        :kwarg todate:
        :kwarg order:
        :kwarg min:
        :kwarg max:
        :kwarg sort:
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(rev_id) for rev_id in ids])

        url = "{}/revisions/{}".format(self._url, ids)

        result, remaining = format_result(url, name='Revision', headers=self._header, params=kwargs, 
                                           site=self._site)

        return (result, remaining)