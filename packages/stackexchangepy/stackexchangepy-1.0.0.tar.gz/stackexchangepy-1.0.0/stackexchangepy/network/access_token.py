from stackexchangepy.helpers import format_ids, format_result
from stackexchangepy.request import post


class AccessToken:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def invalidate(self, tokens, **kwargs):
        """
        Immediately expires the access tokens passed. This method 
        is meant to allow an application to discard any active access tokens 
        it no longer needs.

        :param tokens: up to 20 tokens, represented 
                        as a list, or string, separated with `;`.
        :kwarg page:
        :kwarg pagesize:
        """
        tokens = format_id(tokens) if type(tokens) == str else ';'.join(tokens)
        url = "{}/access-tokens/{}/invalidate".format(self._url, tokens)
        result, remaining = format_result(url, name='AccessToken', headers=self._header, method_type='post')
        return (result, remaining)

    def access_tokens(self, tokens, **kwargs):
        """
        Reads the properties for a set of access tokens.

        :param tokens:
        :kwarg page:
        :kwarg pagesize:
        """
        tokens = format_id(tokens) if type(tokens) == str else ';'.join(tokens)
        url = "{}/access-tokens/{}/invalidate".format(self._url, tokens)
        result, remaining = format_result(url, name='AccessToken', headers=self._header, params=kwargs)
        return (result, remaining)