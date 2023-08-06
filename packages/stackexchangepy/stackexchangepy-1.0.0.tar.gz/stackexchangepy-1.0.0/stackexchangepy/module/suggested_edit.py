from stackexchangepy.helpers import format_ids, format_result


class SuggestedEdit:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/SuggestedEdits.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def suggested_edits(self, **kwargs):
        """
        Returns a list with suggested edits in the systems, and information 
        about the remaining queries.

        :kwarg page: the page from which edits to be returned
        :kwarg pagesize: the number of results per page
        :kwarg fromdate: the mininum date from which results to be returned
        :kwarg todate: the maximum date to which results to be returned
        :kwarg order: can be `asc` (ascending), or `desc` (descending) /default/
        :kwarg min: depends from the sort type, if the sort is set to creation, min defines 
        the minimum creation date from which edits to be returned, if sort is set to approvail,
        min will define the minimum approval date from which edits to be returned,
        if sort is set to reject, min defines the minimum recject date from which edits to be returned
        :kwarg max: same as min, but in case for max
        :kwarg sort: the returned result can be sorted by creation (creation_date) /default/,
        approval (approval_date), or rejection(rejection_date)
        :return: 2-tuple, which first component is a list with suggested edits, and its second component
        is information about the remaining queries
        """
        url = "{}/suggested-edits".format(self._url)

        result, remaining = format_result(url, name='SuggestedEdit', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

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
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(s_id) for s_id in ids])
        url = "{}/suggested-edits/{}".format(self._url, ids)
        result, remaining = format_result(url, name='SuggestedEdit', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)