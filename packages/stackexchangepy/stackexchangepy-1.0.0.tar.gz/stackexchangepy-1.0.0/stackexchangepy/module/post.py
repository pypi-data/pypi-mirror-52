from stackexchangepy.helpers import format_ids, format_result


class Post:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Posts.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def all(self, **kwargs):
        """
        Returns a list with recent posts on the site, and information about the remaining queries.

        :kwarg page: sets the page from which posts to be returned 
        :kwarg pagesize: sets the size of posts in a page to be returned
        :kwarg fromdate: sets the starting date from which posts to be returned
        :kwarg todate: sets the ending date from which posts to be returned
        :kwarg order: can be `asc`(ascending) or `desc`(descending) /defualt/
        :kwarg min: depents from the type of sort selected, if the selected sort is creation, approval, or rejection
         and the min field is set to some date, then the result will contain all posts with starting date 
         of creation, approval, or rejection respectevely
        :kwarg max: the same as min, but in case of max date
        :kwarg sort: the type of sort, which can be used. Types are creation(default), approval, rejection.
        :return: 2-tuple, first component of it is a list with post objects, second component contains information
        about the remaining queries
        """
        url = "{}/posts".format(self._url)
        result, remaining = format_result(url, name='Post', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def ids(self, ids, **kwargs):
        """
        Returns a list with all posts identified by the given ids, and information about the remaining queries.

        :param ids: it can be provided in couple of ways:
          * as a list of numbers, or list of numbers represented as strings
          * as a string, where numbers are separeted by , or ; or space
        :kwarg page: sets the page from which posts to be returned 
        :kwarg pagesize: sets the size of posts in a page to be returned
        :kwarg fromdate: sets the starting date from which posts to be returned
        :kwarg todate: sets the ending date from which posts to be returned
        :kwarg order: can be `asc`(ascending) or `desc`(descending) /defualt/
        :kwarg min: depents from the type of sort selected, if the selected sort is creation, approval, or rejection
         and the min field is set to some date, then the result will contain all posts with starting date 
         of creation, approval, or rejection respectevely
        :kwarg max: the same as min, but in case of max date
        :kwarg sort: the type of sort, which can be used. Types are creation(default), approval, rejection.
        :return: 2-tuple, first component of it is a list with post objects, second component contains information
        about the remaining queries
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(post_id) for post_id in ids])

        url = "{}/posts/{}".format(self._url, ids)
        result, remaining = format_result(url, name='Post', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def comments(self, ids, **kwargs):
        """
        Returns a list of comments to those comments, which post ids are given, and information about the remaining queries.
      
        :param ids: it can be provided in couple of ways:
          * as a list of numbers, or list of numbers represented as strings
          * as a string, where numbers are separeted by , or ; or space
        :kwarg page: sets the page from which comments to be returned 
        :kwarg pagesize: sets the size of comments in a page to be returned
        :kwarg fromdate: sets the starting date from which comments to be returned
        :kwarg todate: sets the ending date from which comments to be returned
        :kwarg order: can be `asc`(ascending) or `desc`(descending) /defualt/
        :kwarg min: depents from the type of sort selected, if the selected sort is creation, or votes;
          if the sort type is creation, then min field can be a date - the min date, from which the returned comments
          will have
          if the sort is votes, then min field can be a number - the min number of votes, which returned comments 
          can have
        :kwarg max: the same as min, but in case of max date
        :kwarg sort: the type of sort, which can be used. Types are creation(default), approval, rejection.
        :return: 2-tuple, first component of it is a list with post objects, second component contains information
        about the remaining queries
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(post_id) for post_id in ids])

        url = "{}/posts/{}/comments".format(self._url, ids)

        result, remaining = format_result(url, name='PostComment', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def comment(self, post_id, **kwargs):
        """
        Adds a comment to the given by id post.
        
        :param post_id: post's id
        :kwarg body: body of the comment
        :return: 2-tuple, first component of it is the created comment, second component contains information
        about the remaining queries
        """
        url = "{}/posts/{}".format(self._url, post_id)

        result, remaining = format_result(url, name='Post', headers=self._header, params=kwargs, site=self._site, method='post')
        return (result, remaining)

    def revisions(self, ids, **kwargs):
        """
        Returns a list with edited revisions of the comments identified by ids, and information about the remaining queries.

        :param ids: it can be provided in couple of ways:
          * as a list of numbers, or list of numbers represented as strings
          * as a string, where numbers are separeted by , or ; or space
        :kwarg page: sets the page from which posts to be returned 
        :kwarg pagesize: sets the size of posts in a page to be returned
        :kwarg fromdate: sets the starting date from which posts to be returned
        :kwarg todate: sets the ending date from which posts to be returned
        :return: 2-tuple, its first component is a list with edited revisions, and its second component
        is information about the remaining queries
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(post_id) for post_id in ids])
        url = "{}/posts/{}/revisions".format(self._url, ids)

        result, remaining = format_result(url, name='PostEditRevision', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def suggested_edits(self, ids, **kwargs):
        """
        Returns a list with suggested edits of the posts identified by ids,
        and information about the remaining queries.

        :param ids: it can be provided in couple of ways:
          * as a list of numbers, or list of numbers represented as strings
          * as a string, where numbers are separeted by , or ; or space
        :kwarg page: sets the page from which comments to be returned 
        :kwarg pagesize: sets the size of comments in a page to be returned
        :kwarg fromdate: sets the starting date from which comments to be returned
        :kwarg todate: sets the ending date from which comments to be returned
        :kwarg order: can be `asc`(ascending) or `desc`(descending) /defualt/
        :kwarg min: depents from the type of sort selected, if the selected sort is creation, approval, or rejection
         and the min field is set to some date, then the result will contain all comments with starting date 
         of creation, approval, or rejection respectevely
        :kwarg max: the same as min, but in case of max date
        :kwarg sort: the type of sort, which can be used. Types are creation(default), approval, rejection.
        :return: 2-tuple, first component of it is a list with post objects, second component contains information
        about the remaining queries
        :return: 2-tuple, its first component is a list with suggested edits, its second component
        is information about the remaining queries
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(post_id) for post_id in ids])

        url = "{}/posts/{}/suggested-edits".format(self._url, ids)

        result, remaining = format_result(url, name='PostSuggestedEdit', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

