from stackexchangepy.helpers import format_result


class Error:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def all(self, **kwargs):
        """
        Returns the various error codes that can 
        be produced by the API.

        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/errors".format(self._url)
        result, remaining = format_result(url, name='Error', headers=self._header, params=kwargs)
        return (result, remaining)

    def by_id(self, error_id):
        """
        This method allows you to generate an error.
        
        :param error_id:
        """
        url = "{}/errors/{}".format(self._url, error_id)
        result, remaining = format_result(url, name='Error', headers=self._header)
        return (result, remaining)
