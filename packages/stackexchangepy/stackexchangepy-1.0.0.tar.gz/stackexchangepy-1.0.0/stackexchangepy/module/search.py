from stackexchangepy.helpers import format_ids, format_result


class Search:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Search.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def search(self, advanced=False, excerpts=False, **kwargs):
        """

        :kwarg advanced:
        :kwarg excerpts:
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
        url = "{}/search".format(self._url)

        if advanced:
            url += '/advanced'
        elif excerpts:
            url += '/excerpts'

        result, remaining = format_result(url, name='SearchResult', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def similar(self, **kwargs):
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
        url = "{}/similar"

        result, remaining = format_result(url, name='SearchResult', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)