from stackexchangepy.helpers import format_result


class Privilege:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Privileges.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def get(self, **kwargs):
        """
        Returns all privileges, available on the site.

        :kwarg page: from which page privileges to be returned
        :kwarg pagesize: the number of privileges per page
        :return: 2-tuple, its first component is a list with privileges, its second component is information
          about the remaining queries
        """
        url = "{}/privileges".format(self._url)

        result, remaining = format_result(url, name='Privilege', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)