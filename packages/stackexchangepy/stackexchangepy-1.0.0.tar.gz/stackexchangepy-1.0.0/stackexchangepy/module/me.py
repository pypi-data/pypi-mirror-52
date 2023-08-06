from stackexchangepy.helpers import format_result, format_ids


class Me:

    """
    For more information & examples check the official documentation at:
      https://github.com/monzita/stackexchangepy/wiki/Me.md
    """
    def __init__(self, url, header, site):
        self._url = url
        self._header = header
        self._site = site

    def me(self):
        """
        Returns Returns the user associated with the passed access_token.
        """
        url = "{}/me".format(self._url)
        result, remaining = format_result(url, name='MyAnswer', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)


    def answers(self, **kwargs):
        """
        Returns all user's answer on the site.

        :kwarg page: the page from which answers to be returned
        :kwarg pagesize: the number of answers to be returned
        :kwarg fromdate: a datetime object, defining the starting date of answers
        :kwarg todate: a datetime object, defining the ending date of answers
        :kwarg order: can be `asc`, or `desc`
        :kwarg min: depends from the `sort` type, if sort type is set to `activity`, `creation`, `min` can be a datetime object, if it's set to `votes`, `min` can be a number, 
                    defining min number of votes of the returned answers
        :kwarg max: depends from the `sort` type, if sort type is set to `activity`, `creation`, `max` can be a datetime object, if it's set to `votes`, `max` can be a number, 
                    defining max number of votes of the returned answers
        :kwarg sort: can be `activity` /default/, `creation`, `votes`
        :return: 2-tuple, with list of user's answers, and information about remaining queries
        """
        url = "{}/me/answers".format(self._url)
        result, remaining = format_result(url, name='MyAnswer', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def badges(self, **kwargs):
        """
        Returns the badges earned by the user associated with the given access_token.

        :kwarg page: the page from which badges to be returned
        :kwarg pagesize: the number of badges to be returned
        :kwarg fromdate: a datetime object, defining the starting date of badges
        :kwarg todate: a datetime object, defining the ending date of badges
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `rank` /default/, `name`, `type`
        :return:
        """
        url = "{}/me/badges".format(self._url)
        result, remaining = format_result(url, name='MyBadge', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def comments(self, toid=None, **kwargs):
        """
        Returns the comments owned by the user 
        associated with the given access_token.
        
        :kwarg toid: returns the comments owned by the user 
                     associated with the given access_token
                     that are in reply to the user identified by {toId}.
        :kwarg page: the page from which comments to be returned
        :kwarg pagesize: the number of comments to be returned
        :kwarg fromdate: a datetime object, defining the starting date of comments
        :kwarg todate: a datetime object, defining the ending date of comments
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `creation` /default/, `votes`
        :return:
        """
        url = "{}/me/comments".format(self._url)

        if toid:
            url += '/{}'.format(toid)

        result, remaining = format_result(url, name='MyComment', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def favorites(self, **kwargs):
        """
        Returns the questions favorites by the user associated with the given access_token..

        :kwarg page: the page from which questions to be returned
        :kwarg pagesize: the number of questions to be returned
        :kwarg fromdate: a datetime object, defining the starting date of questions
        :kwarg todate: a datetime object, defining the ending date of questions
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity` /default/, `votes`, `creation`, `added`
        :return:
        """
        url = "{}/me/favorites".format(self._url)
        result, remaining = format_result(url, name='MyFavorite', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def mentioned(self, **kwargs):
        """
        Returns the comments mentioning the user associated with the given access_token.

        :kwarg page: the page from which comments to be returned
        :kwarg pagesize: the number of comments to be returned
        :kwarg fromdate: a datetime object, defining the starting date of comments
        :kwarg todate: a datetime object, defining the ending date of comments
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `creation` /default/, `votes`
        :return:
        """
        url = "{}/me/mentioned".format(self._url)
        result, remaining = format_result(url, name='Mention', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def network_activity(self, **kwargs):
        """
        Returns all user's activity on the site.

        :kwarg page: the page from which network activities to be returned
        :kwarg pagesize: the number of network activities to be returned
        :kwarg types:
        :return:
        """
        url = "{}/me/network_activity".format(self._url)
        result, remaining = format_result(url, name='MyNetworkActivity', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def notifications(self, unread=False, **kwargs):
        """
        Returns a user's notifications, given an access_token.

        :kwarg page: from which page notifications to be returned
        :kwarg pagesize: how many notifications to be returned
        :return:
        """
        url = "{}/me/notifications".format(self._url)
        
        if unread:
            url += '/unread'

        result, remaining = format_result(url, name='MyNotification', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def posts(self, **kwargs):
        """
        Returns the posts owned by the user associated with the given access_token.
 
        :kwarg page: the page from which posts to be returned
        :kwarg pagesize: the number of posts to be returned
        :kwarg fromdate: a datetime object, defining the starting date of posts
        :kwarg todate: a datetime object, defining the ending date of posts
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity` /default/, `creation`, `votes`
        :return:
        """
        url = "{}/me/posts".format(self._url)
        result, remaining = format_result(url, name='MyPost', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def privileges(self, **kwargs):
        """
        Returns the privileges the user identified by access_token has.

        :kwarg page: from which page, privileges to be returned
        :kwarg pagesize: how many privileges to be returned
        :return:
        """
        url = "{}/me/privileges".format(self._url)
        result, remaining = format_result(url, name='MyPrivilege', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def questions(self, featured=False, no_answers=False, unaccepted=False, unanswered=False, **kwargs):
        """
        Returns the questions owned by the user associated with the given access_token.
        
        :kwarg featured: returns the questions owned by the user associated 
                            with the given access_token, has active bounties
        :kwarg no_answers: returns the questions owned by the user associated 
                            with the given access_token, 
                            which have no answers.
        :kwarg unaccepted: returns the questions owned by the user associated 
                            with the given access_token that have no accepted answer.
        :kwarg page: the page from which questions to be returned
        :kwarg pagesize: the number of questions to be returned
        :kwarg fromdate: a datetime object, defining the starting date of questions
        :kwarg todate: a datetime object, defining the ending date of questions
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity` /default/, `creation`, `votes`
        :return:
        """
        url = "{}/me/questions".format(self._url)

        if featured:
            url += '/featured'
        elif no_answers:
            url += '/no-answer'
        elif unaccepted:
            url += '/unaccepted'
        elif unanswered:
            url += '/unanswered'

        result, remaining = format_result(url, name='Question', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def reputation(self):
        """
        Returns the reputation changed for the user associated with the given access_token.

        :return:
        """
        url = "{}/me/reputation".format(self._url)
        result, remaining = format_result(url, name='MyReputation', headers=self._header, site=self._site)
        return (result, remaining)

    def reputation_history(self, full=False, **kwargs):
        """
        Returns user's public reputation history.

        :kwarg full: returns user's full reputation history, including private events
        :kwarg page:
        :kwarg pagesize:
        :return:
        """
        url = "{}/me/reputation-history".format(self._url)
        
        if full:
            url += "/full"

        result, remaining = format_result(url, name='MyReputationHistory',  headers=self._header, 
                                           params=kwargs, site=self._site)
        return (result, remaining)

    def suggested_edits(self, **kwargs):
        """
        Returns the suggested edits the user identified by access_token has submitted.

        :kwarg page: the page from which suggested-edits to be returned
        :kwarg pagesize: the number of suggested-edits to be returned
        :kwarg fromdate: a datetime object, defining the starting date of suggested-edits
        :kwarg todate: a datetime object, defining the ending date of suggested-edits
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `creation` /default/, `approval`, `rejection`
        :return:
        """
        url = "{}/me/suggested-edits".format(self._url)
        result, remaining = format_result(url, name='MySuggestedEdit', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def tags(self, **kwargs):
        """
        Returns the tags the user identified by the access_token passed is active in.

        :kwarg page: the page from which tags to be returned
        :kwarg pagesize: the number of tags to be returned
        :kwarg fromdate: a datetime object, defining the starting date of tags
        :kwarg todate: a datetime object, defining the ending date of tags
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `popular` /default/, `activity`, `name`
        :return:
        """
        url = "{}/me/tags".format(self._url)
        result, remaining = format_result(url, name='MyTag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_answers(self, tags, **kwargs):
        """
        
        Returns the top 30 answers the user associated with the given 
        access_token has posted in response to questions with the given tags.


        :kwarg page: the page from which answers to be returned
        :kwarg pagesize: the number of answers to be returned
        :kwarg fromdate: a datetime object, defining the starting date of answers
        :kwarg todate: a datetime object, defining the ending date of answers
        :kwarg order:
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity` /default/, `creation`, `votes`
        :return:
        """
        tags = format_ids(tags) if type(tags) is str else ';'.join(tags)
        url = "{}/me/tags/{}/top-answers".format(self._url, tags)
        result, remaining = format_result(url, name='Answer', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_question(self, tags, **kwargs):
        """
        Returns the top 30 questions the user associated with 
        the given access_token has posted in response to questions with the given tags.

        :kwarg page: the page from which questions to be returned
        :kwarg pagesize: the number of questions to be returned
        :kwarg fromdate: a datetime object, defining the starting date of answers
        :kwarg todate: a datetime object, defining the ending date of answers
        :kwarg order: can be `asc`, or `desc`
        :kwarg min:
        :kwarg max:
        :kwarg sort: can be `activity` /default/, `creation`, `votes`
        :return:
        """
        tags = format_ids(tags) if type(tags) is str else ';'.join(tags)
        url = "{}/me/tags/{}/top-question-tags".format(self._url, tags)
        result, remaining = format_result(url, name='Question', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def top_answer_tags(self, **kwargs):
        """
        Returns the user identified by access_token's top 30 tags by answer score.

        :kwarg page: the page from which tags to be returned
        :kwarg pagesize: the number of tags to be returned
        :return:
        """
        url = "{}/me/top-answer-tags".format(self._url)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)
    
    def top_question_tags(self, **kwargs):
        """
        Returns the user identified by access_token's top 30 tags by question score.

        :kwarg page: the page from which tags to be returned
        :kwarg pagesize: the number of tags to be returned
        :return:
        """
        url = "{}/me/top-question-tags".format(self._url)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)
    
    def top_tags(self, **kwargs):
        """
        Returns the user identified by access_token's top 30 tags by combined question and answer score.

        :kwarg page: the page from which tags to be returned
        :kwarg pagesize: the number of tags to be returned
        :return:
        """
        url = "{}/me/top-tags".format(self._url)
        result, remaining = format_result(url, name='Tag', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def inbox(self, unread=False, **kwargs):
        """
        Returns all user's messages on the site.
 
        :kwarg unread: returns the unread items in the user identified by access_token's inbox
        :kwarg page: from which page items to be returned
        :kwarg pagesize: how many items to be returned
        :return:
        """
        url = "{}/me/inbox".format(self._url)

        if unread:
            url += '/unread'

        result, remaining = format_result(url, name='MyInbox', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)

    def timeline(self, **kwargs):
        """
        Returns a subset of the actions the user identified by the passed access_token has taken on the site.
        
        :kwarg page: from which page items to be returned
        :kwarg pagesize: how many items to be returned
        :kwarg fromdate: from when items to be returned
        :kwarg todate: to when items to be returned
        :return:
        """
        url = "{}/me/timeline".format(self._url)
        result, remaining = format_result(url, name='MyTimeline', headers=self._header, params=kwargs, site=self._site)
        return (result, remaining)