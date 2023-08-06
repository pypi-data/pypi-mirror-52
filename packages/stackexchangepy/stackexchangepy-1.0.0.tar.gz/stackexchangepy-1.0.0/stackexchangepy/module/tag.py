from stackexchangepy.helpers import format_ids, format_result


class Tag:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Tags.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def all(self, **kwargs):
        """
        Returns the tags found on a site.

        :kwarg page:  from which page tags to be returned
        :kwarg pagesize: how many tags to be returned
        :kwarg fromdate: from which date tags to be returned
        :kwarg todate: to which date tags to be returned
        :kwarg order: in what order, can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `popular` /default/, `activity`, `name`
        :kwarg inname:
        """
        url = "{}/tags".format(self._url)

        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def info(self, tags, **kwargs):
        """
        Returns tag objects representing the tags in {tags} found on the site.

        :param tags:
        :kwarg page:  from which page tags to be returned
        :kwarg pagesize: how many tags to be returned
        :kwarg fromdate: from which date tags to be returned
        :kwarg todate: to which date tags to be returned
        :kwarg order: in what order, can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `popular` /default/, `activity`, `name`
        """
        tags = format_ids(tags) if type(tags) == str else ';'.join(tags)
        
        url = "{}/tags/{}/info".format(self._url, tags)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def moderator_only(self, **kwargs):
        """
        Returns the tags found on a site that only moderators can use.

        :kwarg page:  from which page tags to be returned
        :kwarg pagesize: how many tags to be returned
        :kwarg fromdate: from which date tags to be returned
        :kwarg todate: to which date tags to be returned
        :kwarg order: in what order, can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `popular` /default/, `activity`, `name`
        """
        url = "{}/tags/moderator-only".format(self._url)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def required(self, **kwargs):
        """
        Returns the tags found on a site that fulfill required tag constraints on questions.

        :kwarg page:  from which page tags to be returned
        :kwarg pagesize: how many tags to be returned
        :kwarg fromdate: from which date tags to be returned
        :kwarg todate: to which date tags to be returned
        :kwarg order: in what order, can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `popular` /default/, `activity`, `name`
        :kwarg inname:
        """
        url = "{}/tags/required".format(self._url)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def synonyms(self, **kwargs):
        """
        Returns all tag synonyms found on the site.

        :kwarg page:  from which page tags to be returned
        :kwarg pagesize: how many tags to be returned
        :kwarg fromdate: from which date tags to be returned
        :kwarg todate: to which date tags to be returned
        :kwarg order: in what order, can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `creation` /default/, `applied`, `date`
        """
        url = "{}/tags".format(self._url)

        if 'tags' in kwargs:
          tags = format_ids(tags) if type(tags) == str else ';'.join([tag for tag in tags])
          kwargs.pop('tags')
          url += '/{}/synonyms'.format(tags)
        else:
          url += '/synonyms'

        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def faq(self, tags, **kwargs):
        """
        Returns the frequently asked questions for the given set of tags in {tags}.

        :param tags:
        :kwarg page:
        :kwarg pagesize:
        """
        tags = format_ids(tags) if type(tags) == str else ';'.join([tag for tag in tags])
        url = "{}/tags/{}/faq".format(self._url, tags)
        result, remaining = format_result(url, name='Faq', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def related(self, tags, **kwargs):
        """
        Returns the tags that are most related to those in {tags}.

        :param tags:
        :kwarg page:
        :kwarg pagesize:
        """
        tags = format_ids(tags) if type(tags) == str else ';'.join([tag for tag in tags])
        url = "{}/tags/{}/related".format(self._url, tags)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def top_answers(self, tag, period='all_time', **kwargs):
        """
        Returns the top 20 answerers active in a single tag, of either all-time or the last 30 days.

        :param tag:
        :kwarg period:
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/tags/top-answers/{}".format(self._url, tag, period)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_askers(self, tag, perio='all_time', **kwargs):
        """
        Returns the top 20 askers active in a single tag, of either all-time or the last 30 days.

        :param tag:
        :kwarg period:
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/tags/top-askers/{}".format(self._url, tag, period)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def wikis(self, tags, **kwargs):
        """
        Returns the wikis that go with the given set of tags in {tags}.

        :param tags:
        :kwarg page:
        :kwarg pagesize:
        """
        tags = format_ids(tags) if type(tags) == str else ';'.join([tag for tag in tags])
        url = "{}/tags/{}/wikis".format(self._url, tags)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)