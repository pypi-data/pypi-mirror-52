from stackexchangepy.helpers import format_ids, format_result
from stackexchangepy.request import post


class App:

    def __init__(self, url, header):
        self._url = url
        self._header = header

    def de_authenticate(self, tokens, **kwargs):
        """

        Passing valid access_tokens to this method 
        causes the application that created them 
        to be de-authorized by the user associated
         with each access_token. This will remove 
         the application from their apps tab, and 
         cause all other existing access_tokens to 
         be destroyed.

        :param tokens:
        :kwarg page:
        :kwarg pagesize:
        """
        tokens = format_id(tokens) if type(tokens) == str else ';'.join([token for token in tokens])
        url = "{}/apps/{}/de-authenticate".format(self._url, tokens)
        result, remaining = format_result(url, name='App', headers=self._header, params=kwargs, method_type='post')
        return (result, remaining)