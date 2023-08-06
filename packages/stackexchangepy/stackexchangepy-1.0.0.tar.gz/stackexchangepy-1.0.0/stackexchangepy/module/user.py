from stackexchangepy.helpers import format_ids, format_result


class User:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Users.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def all(self, **kwargs):
        """
        Returns all users in the site.

        :kwarg page:  the # of page, from which users to be returned
        :kwarg pagesize: the # of users to be returned
        :kwarg fromdate: the date from which users to be returned
        :kwarg todate: to which date users to be returned
        :kwarg order: the order in which users to be returned, 
        can be `asc`(ascending) , or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned users can be sorted by one of the following ways:
                     `reputation` /default/, `creation`, `name`, or `modified`
        """
        url = "{}/users".format(self._url)
        result, remaining = format_result(url, name='User', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def ids(self, ids, **kwargs):
        """
        Returns the users identified by ids.

        :param ids: users ids
        :kwarg page:  the # of page, from which users to be returned
        :kwarg pagesize: the # of users to be returned
        :kwarg fromdate: the date from which users to be returned
        :kwarg todate: to which date users to be returned
        :kwarg order: the order in which users to be returned, 
        can be `asc`(ascending) , or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned users can be sorted by one of the following ways:
                     `reputation` /default/, `creation`, `name`, or `modified`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}".format(self._url, ids)

        result, remaining = format_result(url, name='User', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def answers(self, ids, **kwargs):
        """
        Returns the answers the users in {ids} have posted.

        :param ids: users ids
        :kwarg page: the # of page, from which answers to be returned
        :kwarg pagesize:  the # of answers to be returned
        :kwarg fromdate: the date from which answers to be returned
        :kwarg todate: the date to which answers to be returned
        :kwarg order: he order in which answers to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned answers can be sorted by one of the 
                    following ways: `activity` /default/, `creation`, `votes`

        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/answers".format(self._url, ids)

        result, remaining = format_result(url, name='UserAnswer', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def badges(self, ids, **kwargs):
        """
        Returns the badges the users in {ids} have earned.

        :param ids: users ids
        :kwarg page: the # of page, from which badges to be returned
        :kwarg pagesize: the # of badges to be returned
        :kwarg fromdate: the date from which badges to be returned
        :kwarg todate: to which date badges to be returned
        :kwarg order: the order in which badges to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned answers can be sorted by one of the 
                    following ways: `rank` /default/, `name`, `type`, `awarded`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/badges".format(self._url, ids)

        result, remaining = format_result(url, name='Badge', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def comments(self, ids, toid=None, **kwargs):
        """
        Returns the comments posted by users in {ids}.

        :param ids: users ids
        :kwarg toid: returns the comments that the users in {ids} have 
                    posted in reply to the single user identified in {toid}.
        :kwarg page: the # of page, from which comments to be returned
        :kwarg pagesize: the # of comments to be returned
        :kwarg fromdate: the date from which comments to be returned
        :kwarg todate: to which date comments to be returned
        :kwarg order: the order in which comments to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned comments can be sorted by one of 
                        the following ways: `creation` /default/, `votes`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/comments/{}".format(self._url, ids, toid)

        if toid is not None:
            url += '/{}'.format(toid)

        result, remaining = format_result(url, name='Comment', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def favorites(self, ids, **kwargs):
        """
        Returns the questions that users in {ids} have favorited.

        :param ids: users ids
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned questions can be sorted by one of the  
                    following ways: `activity` /default/, `creation`, `votes`, `added`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/favorites".format(self._url, ids)

        result, remaining = format_result(url, name='UserFavorite', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def mentioned(self, ids, **kwargs):
        """
        Returns all the comments that the users in {ids} were mentioned in.

        :param ids: 
        :kwarg page: the # of page, from which comments to be returned
        :kwarg pagesize:  the # of comments to be returned
        :kwarg fromdate: the date from which comments to be returned
        :kwarg todate: to which date comments to be returned
        :kwarg order: the order in which comments to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned comments can be sorted 
                    by one of the following ways: `creation` /default/, `votes`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/mentioned".format(self._url, ids)

        result, remaining = format_result(url, name='Mention', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def network_activity(self, user_id, **kwargs):
        """
        Returns a summary of a user's activity across the Stack Exchange network, given their account_id.

        :param user_id: user's id
        :kwarg page: the # of page, from which activity to be returned
        :kwarg pagesize: the # of activity to be returned
        :kwarg fromdate: the date from which activity to be returned
        :kwarg todate: to which date activity to be returned
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/network-activity".format(self._url, user_id)

        result, remaining = format_result(url, name='NetworkActivity', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def notifications(self, user_id, unread=False, **kwargs):
        """
        Returns a user's notifications.

        :param user_id: user's id
        :kwarg undread: returns a user's unread notifications
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/users/{}/notifications".format(self._url, user_id)

        if unread:
          url += "/unread"

        result, remaining = format_result(url, name='Notification', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def posts(self, ids, **kwargs):
        """
        Returns the posts the users in {ids} have posted.

        :param ids: users ids
        :kwarg page: the # of page, from which posts to be returned
        :kwarg pagesize: the # of posts to be returned
        :kwarg fromdate: the date from which posts to be returned
        :kwarg todate: to which date posts to be returned
        :kwarg order:  the order in which posts to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned posts can be sorted by 
                    one of the following ways: `activity` /default/, `creation`, `votes`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/posts".format(self._url, ids)

        result, remaining = format_result(url, name='NetworkActivity', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def privileges(self, user_id, **kwargs):
        """
        Returns the privileges a user has.

        :param ids:
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/users/{}/privileges".format(self._url, user_id)

        result, remaining = format_result(url, name='Privilege', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def questions(self, ids, featured=False, no_answers=False, 
                   unaccepted=False, unanswered=False, **kwargs):    
        """
        Returns the questions asked by the users in {ids}

        :param ids: users ids
        :kwarg featured: returns the questions on which the users in {ids} have active bounties
        :kwarg no_answers: returns the questions asked by the users in {ids} which have no answers
        :kwarg unaccepted: returns the questions asked by the users in {ids} which 
                            have at least one answer, but no accepted answer
        :kwarg unanswered: returns the questions asked by the users in {ids} 
                            which the site considers unanswered, while still having at least one answer posted
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize:  the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date posts to be returned
        :kwarg order: the order in which questions to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort:returned questions can be 
                    sorted by one of the following ways: `activity` /default/, `creation`, `votes`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/questions".format(self._url, ids)

        if unaccepted:
            url += "/unaccepted"
        elif featured:
            url += "/featured"
        elif no_answers:
            url += "/no_answers"
        elif unanswered:
            url += "/unanswered"

        result, remaining = format_result(url, name='Question', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def reputation(self, ids, **kwargs):
        """ 
        Returns a subset of the reputation changes for users in {ids}.

        :param ids: users ids
        :kwarg page:
        :kwarg pagesize:
        :kwarg fromdate:
        :kwarg todate:
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/reputation".format(self._url, ids)

        result, remaining = format_result(url, name='Reputation', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def reputation_history(self, ids, full=False, **kwargs):
        """
        Returns users' public reputation history.

        :param ids: users ids
        :kwarg full: returns a user's full reputation history, including private events
        :kwarg page:
        :kwarg pagesize:
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/reputation-history".format(self._url, ids)

        if full:
            url += "/full"

        result, remaining = format_result(url, name='ReputationHistory', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def suggested_edits(self, ids, **kwargs):
        """
        Returns the suggested edits that the users in {ids} have submitted.

        :param ids:
        :kwarg page: the # of page, from which edits to be returned
        :kwarg pagesize:  the # of edits to be returned
        :kwarg fromdate: the date from which edits to be returned
        :kwarg todate: to which date posts to be returned
        :kwarg order: the order in which edits to be returned, 
                        can be `asc`(ascending) /default/, or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort:returned edits can be 
                    sorted by one of the following ways: `creation` /default/, `approval`, `rejection`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/suggested-edits".format(self._url, ids)

        result, remaining = format_result(url, name='SuggestedEdit', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def tags(self, ids, **kwargs):
        """
        Returns the tags the users identified in {ids} have been active in.

        :param ids: users ids
        :kwarg page: the # of page, from which tags to be returned
        :kwarg pagesize: the # of tags to be returned
        :kwarg fromdate: the date from which tags to be returned
        :kwarg todate: to which date tags to be returned
        :kwarg order: the order in which tags to be returned, can be `asc`(ascending), or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned tags can be sorted by one of the 
                    following ways: `popular` /default/, `activity`, `name`
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])
        url = "{}/users/{}/tags".format(self._url, ids)

        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_answers(self, user_id, tags, **kwargs):
        """
        Returns the top 30 answers a user has posted in response to questions with the given tags.

        :param user_id: user's id
        :param tags:
        :kwarg page: the # of page, from which answers to be returned
        :kwarg pagesize: the # of answers to be returned
        :kwarg fromdate: the date from which answers to be returned
        :kwarg todate: to which date answers to be returned
        :kwarg order: the order in which answers to be returned, 
                        can be `asc`(ascending), or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned answers can be sorted by one of the 
                    following ways: `activity` /default/, `creation`, `votes`
        """
        tags = format_ids(tags) if type(tags) == str else ';'.join([tag for tag in tags])
        url = "{}/users/{}/top-answers/{}".format(self._url, user_id, tags)

        result, remaining = format_result(url, name='Answer', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_questions(self, user_id, tags, **kwargs):
        """
        Returns the top 30 questions a user has asked with the given tags.

        :param user_id: user's id
        :param tags:
        :kwarg page: the # of page, from which questions to be returned
        :kwarg pagesize: the # of questions to be returned
        :kwarg fromdate: the date from which questions to be returned
        :kwarg todate: to which date questions to be returned
        :kwarg order: the order in which questions to be returned, can be `asc`(ascending), or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned questions can be sorted by 
                    one of the following ways: `activity` /default/, `creation`, `votes`
        """
        tags = format_ids(tags) if type(tags) == str else ';'.join([tag for tag in tags])
        url = "{}/users/tags/{}/top-questions/{}".format(self._url, tags)

        result, remaining = format_result(url, name='Question', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_question_tags(self, user_id, **kwargs):
        """
        Returns a single user's top tags by question score.

        :param user_id: user's id
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/users/{}/top-question-tags".format(self._url, user_id)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_answer_tags(self, user_id, **kwargs):
        """
        Returns a single user's top tags by answer score.

        :param user_id: user's id
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/users/{}/top-answer-tags".format(self._url, user_id)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_tags(self, user_id, **kwargs):
        """
        Returns a single user's top tags by combined question and answer score.

        :param user_id: user's id
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/users/{}/top-tags".format(self._url, user_id)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def timeline(self, ids, **kwargs):
        """
        Returns a subset of the actions the users in {ids} have taken on the site.

        :param ids:
        :kwarg page:
        :kwarg pagesize:
        :kwarg fromdate:
        :kwarg todate:
        """
        ids = format_ids(ids) if type(ids) == str else ';'.join([str(user_id) for user_id in ids])

        url = "{}/users/{}/timeline".format(self._url, ids)

        result, remaining = format_result(url, name='Timeline', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def moredators(self, elected=False, **kwargs):
        """
        Returns those users on a site who can exercise moderation powers.

        :kwarg elected: returns those users on a site who both have moderator powers, and were actually elected
        :kwarg page:  the # of page, from which users to be returned
        :kwarg pagesize: the # of users to be returned
        :kwarg fromdate: the date from which users to be returned
        :kwarg todate: to which date users to be returned
        :kwarg order: the order in which users to be returned, 
        can be `asc`(ascending) , or `desc`(descending) order.
        :kwarg min:
        :kwarg max:
        :kwarg sort: returned users can be sorted by one of the following ways:
                     `reputation` /default/, `creation`, `name`, or `modified`
        """
        url = "{}/users/moderators".format(self._url)

        if elected:
            url += "/elected"

        result, remaining = format_result(url, name='User', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def inbox(self, user_id, unread=False, **kwargs):
        """
        Returns a user's inbox.

        :param user_id:
        :kwarg unread: returns the unread items in a user's inbox.
        :kwarg page:
        :kwarg pagesize:
        """
        url = "{}/users/{}/inbox".format(self._url, user_id)

        if unread:
            url += "/unread"

        result, remaining = format_result(url, name='Inbox', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)
