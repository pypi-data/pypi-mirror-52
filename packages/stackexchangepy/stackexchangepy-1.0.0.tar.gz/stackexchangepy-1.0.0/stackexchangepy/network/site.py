from stackexchangepy.helpers import format_result


class Site:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def all(self, **kwargs):
        """
        Returns all sites in the network.

        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/sites".format(self._url)
        result, remaining = format_result(url, name='Site', headers=self._header, params=kwargs)
        return (result, remaining)

      