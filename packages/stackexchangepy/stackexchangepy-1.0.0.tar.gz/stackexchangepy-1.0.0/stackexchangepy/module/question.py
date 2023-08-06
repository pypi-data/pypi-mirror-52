from stackexchangepy.helpers import format_ids, format_result
from stackexchangepy.request import post

class Question:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Questions.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def all(self, **kwargs):
        """
        Returns all questions on the site.

        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned questions can be sorted by one of the following ways: 
            `activity` /default/, `creation`, `votes`, `hot`, `week`, `month`
        :kwarg tagged:
        """
        url = "{}/questions".format(self._url)
        result, remaining = format_result(url, name='Question',headers=self._header, 
                                           params=kwargs,  site=self._site)

        return (result, remaining)

    def ids(self, ids, **kwargs):
        """
        Returns the questions identified in {ids}.

        :param ids: questions ids
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity`, `creation`, or `date`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(q_id) for q_id in ids])
        url = "{}/questions/{}".format(self._url, ids)
        result, remaining = format_result(url, name='Question', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def answers(self, ids, **kwargs):
        """
        Returns all asnwers of the questions identified by ids.

        :param ids: question ids
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity`, `creation`, or `date`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(q_id) for q_id in ids])
        url = "{}/questions/{}/answers".format(self._url, ids)
        result, remaining = format_result(url, name='Answer', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def answer(self, question_id, **kwargs):
        """
        Create a new answer on the given question.
        
        :param question_id: question's id
        :kwarg body: answer's text
        """
        url = "{}/questions/{}/answers/add".format(self._url, question_id)
        result, remaining = format_result(url, name='Question', headers=self._header, params=kwargs, 
                                          site=self._site, method_type='post')
        return (result, remaining)

    def close(self, question_id):
        """
        Returns the flag options that make up 
        close reasons that the user identified with an access_token can create for this question.

        :param question_id: question's id
        """
        url = "{}/questions/{}/close/options".format(self._url, question_id)
        result, remaining = format_result(url, name='Option',  headers=self._header, site=self._site)
        
        return (result, remaining)

    def comments(self, ids, **kwargs):
        """
        Returns all comments of the questions identified by id.

        :param ids: question ids
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `creation`, or `date`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(q_id) for q_id in ids])
        url = "{}/questions/{}/comments".format(self._url, ids)
        result, remaining = format_result(url, name='Comment', headers=self._header,params=kwargs,  site=self._site)

        return (result, remaining)

    def delete(self, question_id):
        """
        Deletes a question.

        :param question_id: question's id
        """
        url = "{}/questions/{}/delete".format(self._url, question_id)
        result = post(url, headers=self._header)
        return result.status_code

    def downvote(self, question_id, undo=False):
        """
        Downvotes a question.

        :param question_id: question's id
        :kwarg undo: if set to true, will undo the action
        """
        url = "{}/questions/{}/downvote".format(self._url, question_id)
        
        if undo:
            url += '/undo'

        result, remaining = format_result(url, name='Question', headers=self._header, 
                                          params=kwargs,  site=self._site, method_type='post')

        return (result, remaining)

    def edit(self, question_id, **kwargs):
        """
        Edit an existing question.

        :param question_id: question's id
        :kwarg body: the new body of the question
        :kwarg title: the new title
        :kwarg tags:
        :kwarg comment: reason for the edit
        """
        url = "{}/questions/{}/edit".format(self._url, question_id)
        
        result, remaining = format_result(url, name='Question', headers=self._header, 
                                          params=kwargs,  site=self._site, method_type='post')

        return (result, remaining)

    def favorite(self, question_id, undo=False):
        """
        
        :param question_id: question's id
        :kwarg undo: removes a question from favorites
        """
        url = "{}/questions/{}/favorite".format(self._url, question_id)
        
        if undo:
            url += '/undo'

        result, remaining = format_result(url, name='Question', headers=self._header, 
                                          site=self._site, method_type='post')

        return (result, remaining)

    def flags(self, question_id):
        """
        Returns the different flags, including close reasons, 
        that the user identified with an access_token can create 
        for this question. Available flags vary from post to post 
        and user to user, an app should never assume a particular 
        flag can be created without consulting this method.

        :param question_id: question's id
        """
        url = "{}/questions/{}/flags/options".format(self._url, question_id)
        result, remaining = format_result(url, name='Question', headers=self._header, site=self._site)

        return (result, remaining)

    def flag(self, question_id, **kwargs):
        """
        Casts a flag (including "close votes) against the question identified by id.

        :param question_id: question's id
        :kwarg option_id:
        :kwarg target_site:
        """
        url = "{}/questions/{}/flags/add".format(self._url, question_id)
        result, remaining = format_result(url, name='FlaggedQuestion', headers=self._header, 
                                          site=self._site, method_type="post")

        return (result, remaining)

    def linked(self, ids, **kwargs):
        """
        Returns all questions which link to those questions identified in {ids}

        :param ids: question ids
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity`, `creation`, `votes`, `rank`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(q_id) for q_id in ids])
        url = "{}/questions/{}/linked".format(self._url, ids)
        result, remaining = format_result(url, name='LinkedQuestion', headers=self._header, params=kwargs, 
                                          site=self._site)

        return (result, remaining)

    def related(self, ids, **kwargs):
        """
        Returns questions that the site considers related to those identified by {ids}.

        :param ids: question ids
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity`, `creation`, `votes`, `rank`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(q_id) for q_id in ids])
        url = "{}/questions/{}/linked".format(self._url, ids)
        result, remaining = format_result(url, name='RelatedQuestion', headers=self._header, params=kwargs, site=self._site)

        return (result, remaining)

    def timeline(self, ids, **kwargs):
        """
        Returns a subset of the events that have happened to the questions identified in id.

        :param ids: question ids
        :kwarg page: the # of page, from which events to be returned
        :kwarg pagesize: the # of events to be returned
        :kwarg fromdate: the date from which events to be returned
        :kwarg todate: to which date events to be returned
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(q_id) for q_id in ids])
        url = "{}/questions/{}/timeline".format(self._url, ids)
        result, remaining = format_result(url, name='Event', headers=self._header, 
                                          params=kwargs, site=self._site)

        return (result, remaining)


    def upvote(self, question_id, undo=False):
        """
        Upvotes a question.

        :param question_id: question's id
        :kwarg undo: if set to true, will undo the action
        """
        url = "{}/questions/{}/upvote".format(self._url, question_id)
        
        if undo:
          url += '/undo'

        result, remaining = format_result(url, name='Question', headers=self._header, 
                                          site=self._site, method_type='post')

        return (result, remaining)

    def ask(self, **kwargs):
        """
        Creates a new question.
        
        :kwarg title:
        :kwarg body:
        :kwarg tags:
        """
        url = "{}/questions/add".format(self._url)
        result, remaining = format_result(url, name='Question', headers=self._header, 
                                           params=kwargs, site=self._site, method_type='post')

        return (result, remaining)

    def featured(self, **kwargs):
        """
        Returns all the questions with active bounties in the system.
        

        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity`, `creation`, `votes`
        """
        url = "{}/questions/featured".format(self._url)
        result, remaining = format_result(url, name='Question', headers=self._header, 
                                          params=kwargs, site=self._site)

        return (result, remaining)

    def no_answers(self, **kwargs):
        """
        Returns questions which have received no answers.

        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity`, `creation`, `votes`
        :kwarg tagged:
        """
        url = "{}/questions/no-answers".format(self._url)
        result, remaining = format_result(url, name='Question', headers=self._header, 
                                           params=kwargs, site=self._site)

        return (result, remaining)

    def unanswered(self,my_tags=False, **kwargs):
        """
        
        :kwarg my_tags: returns questions the site 
                        considers to be unanswered, which are within a 
                        user's favorite tags. If a user has not favorites, 
                        their frequented tags are used instead.
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity`, `creation`, `votes`
        :kwarg tagged:
        """
        url = "{}/questions/unanswered".format(self._url)

        if my_tags:
            url += "/my-tags"

        result, remaining = format_result(url, name='Question', headers=self._header, 
                                          params=kwargs, site=self._site)
        return (result, remaining)
