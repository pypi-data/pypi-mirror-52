from stackexchangepy.helpers import format_result


class Info:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Info.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def get(self):
        """
        Returns a 2-tuple, containing a collection of statistics about the site & 
        information about the remainign queries.
        """
        url = "{}/info".format(self._url)
        result, remaining = format_result(url, name='Info', headers=self._header, site=self._site)
        return (result, remaining)