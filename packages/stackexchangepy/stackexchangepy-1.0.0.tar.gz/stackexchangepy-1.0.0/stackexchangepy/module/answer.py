from stackexchangepy.helpers import format_ids, format_result
from stackexchangepy.request import post


class Answer:

  """
  For more information & examples check the official documentation at:
    https://github.com/monzita/stackexchangepy/wiki/Answers.md
  """
  def __init__(self, url, header, site):
    self._url = url
    self._header = header
    self._site = site

  def all(self, **kwargs):
    """
    Returns a tuple-like object, containing a list with all answers in the site, and object, containing
    information about the remaining queries.

    If the user needs specific kind of answers, it can provide more information using keys listed below:
    :kwarg page: returns the answers on a given page
    :kwarg pagesize: returns the number of answers
    :kwarg fromdate:
    :kwarg order: can be ordered by 
            * ascending order (asc) /default choice/, 
            * descending order(desc)
    :kwarg todate:
    :kwarg max:
    :kwarg sort: the returnes answers can be sorted by one of the following ways:
      * activity, which is the default choice
      * creation
      * votes

    :return: returns a 2-tuple, the first element is a list with objects, each of whcih represents an answer,
      and the second is an object, containing information about the number of the remaining queries, which the
      user can use. 
    """
    url = "{}/answers".format(self._url)
    result, remaining = format_result(url, name='Answer', headers=self._header, params=kwargs, site=self._site)
    return (result, remaining)

  def ids(self, ids, **kwargs):
    """
    Returns a tuple-like object, containing a list with answers, which ids are provided by the user, and
    an object, containing the remaining queries of the user.

    If the user needs specific kind of answers, it can provide more information using keys listed below:
    :param ids: can be represented as a string, containig one of the following delimters: `,`;`;`,` `, or
      can be represented as a list with ids.
    :kwarg page: returns the answers on a given page
    :kwarg pagesize: returns the number of answers
    :kwarg fromdate:
    :kwarg order: can be ordered by 
            * ascending order (asc) /default choice/, 
            * descending order(desc)
    :kwarg todate:
    :kwarg max:
    :kwarg min:
    :kwarg sort: the returnes answers can be sorted by one of the following ways:
      * activity, which is the default choice
      * creation
      * votes

    :return: returns a 2-tuple, the first element is a list with objects, each of whcih represents an answer,
      and the second is an object, containing information about the number of the remaining queries, which the
      user can use. 
    """
    ids = format_ids(ids) if type(ids) == str else ';'.join([str(_id) for _id in ids])
    url = "{}/answers/{}".format(self._url, ids)
    result, remaining = format_result(url, name='Answer', headers=self._header, params=kwargs, site=self._site)

    return (result, remaining)

  def accept(self, answer_id, undo=False):
    """
    Accepts an answer, or rejects an accepted answer.

    :param answer_id: the answer id
    :param undo: by default is set to false, but if it's set to true, will undo accepted anser.
    :return: it returns the accepted answer, and the remaining queries.
    """
    url = "{}/answers/{}/accept".format(self._url, answer_id)

    if undo:
      url += "/undo"

    result, remaining = format_result(url, name='Answer', headers=self._header, site=self._site, method_type='post')

    return (result, remaining)

  def comments(self, ids, **kwargs):
    """
    Returns a list with comments, from all answers with the given ids.

    If the user needs specific kind of comments, it can provide more information using keys listed below:
    :param ids: can be represented as a string, containig one of the following delimters: `,`;`;`,` `, or
      can be represented as a list with ids.
    :kwarg page: returns the answers on a given page
    :kwarg pagesize: returns the number of answers
    :kwarg fromdate:
    :kwarg order: can be ordered by 
            * ascending order (asc) /default choice/, 
            * descending order(desc)
    :kwarg todate:
    :kwarg max:
    :kwarg sort: the returnes answers can be sorted by one of the following ways:
      * creation, which is the default choice
      * votes

    :return: returns a 2-tuple, the first element is a list with objects, each of whcih represents a comment,
      and the second is an object, containing information about the number of the remaining queries, which the
      user can use. 
    """
    ids = format_ids(ids) if type(ids) == str else ';'.join([str(_id) for _id in ids])
    
    url = "{}/answers/{}/comments".format(self._url, ids)
    result, remaining = format_result(url, name='Comment', headers=self._header, params=kwargs, site=self._site)
    return (result, remaining)

  def delete(self, answer_id):
    """
    Delets an answer.

    :param answer_id: answer's id
    :return: the status of the query
    """
    url = "{}/answers/{}/delete".format(self._url, answer_id)
    result = post(url, headers=self._header)
    return result.status_code


  def downvote(self, answer_id, undo=False):
    """
    Downvotes an answer, if undo is set to false, or it reverses the action.

    :param answer_id: answer's id
    :param undo: by default is set to false, but if you want to reverse already downvoted answer, then set it
      to true
    """
    url = "{}/answers/{}/downvote".format(self._url, answer_id)

    if undo:
      url += '/undo'

    result, remaining = format_result(url, name='Answer', headers=self._header, site=self._site, method_type='post')
    return (result, remaining)

  def edit(self, answer_id, **kwargs):
    """
    Edits an answer. Returns the edited answer, and the remaining queries.

    :param answer_id: answer's id
    :kwarg body:
    :kwarg comment:
    :return: 2-tuple, containing the edited answer and the remaining queries.
    """
    url = "{}/answers/{}/edit".format(self._url, answer_id)

    result, remaining = format_result(url, name='Answer', headers=self._header, params=kwargs, site=self._site, method_type='post')

    return (result, remaining)

  def flag(self, answer_id, **kwargs):
    """
    Adds a new flag.

    :param answer_id:
    :kwarg option_id:
    :kwarg comment:
    :return: 2-tupe, containing the flagged answer, and the remaining queries.
    """
    url = "{}/answers/{}/flags/add".format(self._url, answer_id)

    result, remaining = format_result(url, name='Flag', headers=self._header, params=kwargs, site=self._site, method_type='post')

    return (result, remaining)


  def flags(self, answer_id):
    """
    Returns a list with available flag options.

    :param answer_id:
    :return: 2-tuple, first element is a list with flag options, the second element is an object with
      the remaining queries
    """
    url = "{}/answers/{}/flasgs/options".format(self._url, answer_id)

    result, remaining = format_result(url, name='Comment', headers=self._header, site=self._site)
    return (result, remaining)

  def questions(self, ids, **kwargs):
    """
    Returns a list of the questions that answers identied by {ids} are on.

  
    If the user needs specific kind of questions, it can provide more information using keys listed below:
    :param ids: can be represented as a string, containig one of the following delimters: `,`;`;`,` `, or
      can be represented as a list with ids.
    :kwarg page: returns the answers on a given page
    :kwarg pagesize: returns the number of answers
    :kwarg fromdate:
    :kwarg order: can be ordered by 
            * ascending order (asc) /default choice/, 
            * descending order(desc)
    :kwarg todate:
    :kwarg max:
    :kwarg sort: the returnes answers can be sorted by one of the following ways:
      * activity, which is the default choice
      * creation
      * votes

    :return: returns a 2-tuple, the first element is a list with objects, each of whcih represents a question,
      and the second is an object, containing information about the number of the remaining queries, which the
      user can use. 
    """
    ids = format_ids(ids) if type(ids) == str else ';'.join([str(_id) for _id in ids])
  
    url = "{}/answers/{}/questions".format(self._url, ids)
    result, remaining = format_result(url, name='Question', headers=self._header, params=kwargs, site=self._site)

    return (result, remaining)


  def upvote(self,answer_id, undo=False):
    """
    Upvotes(or undo) an answer.

    :param answer_id:
    :param undo:
    :return: the (undo) upvoted answer, and the remaining queries represented as 2-tuple 
    """
    url = "{}/answers/{}/upvote".format(self._url, answer_id)

    if undo:
      url += '/undo'

    result, remaining = format_result(url, name='Answer', headers=self._header, site=self._site, method_type='post')

    return (result, remaining)
