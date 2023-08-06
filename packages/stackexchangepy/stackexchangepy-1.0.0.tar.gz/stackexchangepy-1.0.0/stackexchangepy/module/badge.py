from stackexchangepy.helpers import format_ids, format_result


class Badge:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Badges.md
    """
    def __init__(self, url, header, site):
      self._url = url
      self._header = header
      self._site = site

    def all(self, **kwargs):
        """
        Returns a 2-tuple, containing all the badges in the system, and the remaining queries.

        If the user wants more concrete results, it can provide some filters on the result, specififying the following
        fields:
        :kwarg page: if given, returns all badges from the given page
        :kwarg pagesize: if given, returns # of badges == pagesize
        :kwarg fromdate: returns badges from the given date
        :kwarg todate: returns badges to the given date
        :kwarg order: returns badges in the given order `desc` /default/, `asc`
        :kwarg min: depends from the type of sort
        :kwarg max: depends from the type of sort
        :kwarg sort: returns badges, sorted by the given type of sort, which can be `rank`/default, `name`, `type`
        :kwarg inmane:
        :return: 2-tuple, first element is a list with badge objects, second is information about the remaining queries
        """
        url = "{}/badges".format(self._url)
        result, remaining = format_result(url, name='Badge', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def ids(self, ids, **kwargs):
        """
        Returns a 2-tuple, containing all the badges by given ids in the system, and the remaining queries.

        If the user wants more concrete results, it can provide some filters on the result, specififying the following
        fields:
        :kwarg page: if given, returns all badges from the given page
        :kwarg pagesize: if given, returns # of badges == pagesize
        :kwarg fromdate: returns badges from the given date
        :kwarg todate: returns badges to the given date
        :kwarg order: returns badges in the given order `desc` /default/, `asc`
        :kwarg min: depends from the type of sort
        :kwarg max: depends from the type of sort
        :kwarg sort: returns badges, sorted by the given type of sort, which can be `rank`/default, `name`
        :kwarg inmane:
        :return: 2-tuple, first element is a list with badge objects, second is information about the remaining queries
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(_id) for _id in ids])

        url = "{}/badges/{}".format(self._url, ids)
        result, remaining = format_result(url, name='Badge', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def name(self, **kwargs):
        """
        Returns a 2-tuple, containing all the explicitly named-badges and the remaining queries.

        If the user wants more concrete results, it can provide some filters on the result, specififying the following
        fields:
        :kwarg page: if given, returns all badges from the given page
        :kwarg pagesize: if given, returns # of badges == pagesize
        :kwarg fromdate: returns badges from the given date
        :kwarg todate: returns badges to the given date
        :kwarg order: returns badges in the given order `desc` /default/, `asc`
        :kwarg min: depends from the type of sort
        :kwarg max: depends from the type of sort
        :kwarg sort: returns badges, sorted by the given type of sort, which can be `rank`/default, `name`
        :kwarg inmane:
        :return: 2-tuple, first element is a list with badge objects, second is information about the remaining queries
        """
        url = "{}/badges/name".format(self._url)
        result, remaining = format_result(url, name='NamedBadge', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def recipients(self, **kwargs):
        """
        Returns a 2-tuple, containing all recently awarded badges (or recently awarded badges in the system, constrained to a certain set of badges)
        and the remaining queries.

        If the user wants more concrete results, it can provide some filters on the result, specififying the following
        fields:
        :kwarg page: if given, returns all badges from the given page
        :kwarg pagesize: if given, returns # of badges == pagesize
        :kwarg fromdate: returns badges from the given date
        :kwarg todate: returns badges to the given date
        :return: 2-tuple, first element is a list with badge objects, second is information about the remaining queries
        """
        url = "{}/badges/recipients".format(self._url)

        if 'ids' in kwargs:
          ids = format_ids(ids) if type(ids) == str else ';'.join([str(_id) for _id in ids])
          kwargs.pop('ids')
          url += "/{}".format(ids)

        result, remaining = format_result(url, name='Recipient', headers=self._header,  params=kwargs,site=self._site)
        return (result, remaining)

    def tags(self, **kwargs):
        """
        Returns a 2-tuple, containing all badges that are awarded for participation in specific tags. and the remaining queries.

        If the user wants more concrete results, it can provide some filters on the result, specififying the following
        fields:
        :kwarg page: if given, returns all badges from the given page
        :kwarg pagesize: if given, returns # of badges == pagesize
        :kwarg fromdate: returns badges from the given date
        :kwarg todate: returns badges to the given date
        :kwarg order: returns badges in the given order `desc` /default/, `asc`
        :kwarg min: depends from the type of sort
        :kwarg max: depends from the type of sort
        :kwarg sort: returns badges, sorted by the given type of sort, which can be `rank`/default, `name`
        :kwarg inmane:
        :return: 2-tuple, first element is a list with badge objects, second is information about the remaining queries
        """
        url = "{}/badges/tags".format(self._url)
        result, remaining = format_result(url, name='Tag', headers=self._header,  params=kwargs,site=self._site)
        return (result, remaining)
