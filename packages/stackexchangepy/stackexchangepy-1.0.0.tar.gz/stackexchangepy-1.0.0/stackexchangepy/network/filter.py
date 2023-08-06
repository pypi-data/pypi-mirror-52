from stackexchangepy.helpers import format_ids, format_result


class Filter:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def create(self, **kwargs):
        """
        Creates a new filter given a list of includes, 
        excludes, a base filter, and whether 
        or not this filter should be "unsafe".

        :kwarg include:
        :kwarg exclude:
        :kwarg base:
        :kwarg unsafe:
        """
        url = "{}/filters/create".format(self._url)
        result, remaining = format_result(url, name='Error', headers=self._header, method_type='post')
        return (result, remaining)


    def filters(self, filtrs):
        """
        Returns the fields included by the given 
        filters, and the "safeness" of those filters.

        :param filters:
        """
        filtrs = format_id(filtrs) if type(filtrs) == str else ';'.join([filtr for filtr in filtrs])
        url = "{}/filters/{}".format(self._url, filtrs)
        result, remaining = format_result(url, name='Filter', headers=self._header)
        return (result, remaining)
