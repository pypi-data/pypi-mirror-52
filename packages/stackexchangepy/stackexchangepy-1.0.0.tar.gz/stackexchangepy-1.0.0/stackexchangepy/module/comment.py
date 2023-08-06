from stackexchangepy.helpers import format_ids, format_result
from stackexchangepy.request import post


class Comment:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Comments.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def all(self, **kwargs):
        """
        Returns a 2-tuple, containing a list with all comments in the site and ifnformation about
        the remaining queries.

        If the user needs specific kind of comments, it can provide more information using keys listed below:
        :kwarg page: returns the comments on a given page
        :kwarg pagesize: returns the number of comments
        :kwarg fromdate:
        :kwarg order: can be ordered by 
                * ascending order (asc) /default choice/, 
                * descending order(desc)
        :kwarg todate:
        :kwarg max:
        :kwarg sort: the returnes comments can be sorted by one of the following ways:
          * creation /default/
          * votes

        :return: returns a 2-tuple, the first element is a list with objects, each of whcih represents a comment,
          and the second is an object, containing information about the number of the remaining queries, which the
          user has. 
        """
        url = "{}/comments".format(self._url)
        result, remaining = format_result(url, name='Comment', headers=self._header,  params=kwargs,site=self._site)
        return (result, remaining)

    def ids(self, ids, **kwargs):
        """
        Returns a 2-tuple, containing a list with comments provided by ids, in the site and ifnformation about
        the remaining queries.

        If the user needs specific kind of comments, it can provide more information using keys listed below:
        :param ids: can be represented as a string, containig one of the following delimters: `,`;`;`,` `, or
          can be represented as a list with ids.
        :kwarg page: returns the comments on a given page
        :kwarg pagesize: returns the number of comments
        :kwarg fromdate:
        :kwarg order: can be ordered by 
                * ascending order (asc) /default choice/, 
                * descending order(desc)
        :kwarg todate:
        :kwarg max:
        :kwarg min:
        :kwarg sort: the returnes comments can be sorted by one of the following ways:
          * creation
          * votes

        :return: returns a 2-tuple, the first element is a list with objects, each of whcih represents a comment,
          and the second is an object, containing information about the number of the remaining queries, which the
          user can use. 
        """
        ids = format_ids(ids) if str(ids) else ';'.join(ids)
        url = "{}/comments/{}".format(self._url, ids)
        result, remaining = format_result(url, name='Comment', headers=self._header,  params=kwargs, site=self._site)
        return (result, remaining)

    def edit(self, comment_id, **kwargs):
        """
        Edits a comment. Returns the edited comment, and the remaining queries.

        :param comment_id: comment's id
        :kwarg body: the new text for the comment
        :kwarg comment: the reason for change
        :return: 2-tuple, containing the edited comment and the remaining queries.
        """
        url = "{}/comments/{}".format(comment_id)
        result, remaining = format_result(url, name='Comment', headers=self._header,  params=kwargs,site=self._site, method='post')
        return (result, remaining)

    def delete(self, comment_id):
        """
        Removes a comment.

        :param comment_id: comment's id
        :return: status of the action
        """
        url = "{}/comments/{}".format(self._url, comment_id)
        result = post(url, headers=self._header)
        return result.status_code

    def flags(self, comment_id):
        """
        Returns a 2-tuple, containing a list with available flags, and information about the remaining queries.

        :param comment_id: comment's id
        """
        url = "{}/comments/{}/flags/options".format(comment_id)
        result, remaining = format_result(url, name='Comment', headers=self._header, site=self._site)
        return (result, remaining)

    def upvote(self, comment_id, undo=False):
        """
        Upvotes a comment /or undoes an upvote/.

        :param comment_id: comment's id
        :kwarg undo: if you upvoted the same comment, and want to undone the action, set undo to true. By
        default is set to false.
        """
        url = "{}/comments/upvote".format(comment_id)

        if undo:
            url += "/undo"

        result, remaining = format_result(url, name='Comment', headers=self._header,  params=kwargs,site=self._site, method='post')
        return (result, remaining)