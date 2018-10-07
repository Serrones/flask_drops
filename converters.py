"""
Script criado para customizar conversores de URL. Após isso,
é necessário importar no script principal (app.py), e acrescentar
nossos conversores no app.url_map.converters
"""
from werkzeug.routing import BaseConverter

# Customizar o regex
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
# Receber mais do que um nome na URL separados pelo sinal '+'
class ListConverter(BaseConverter):
    # pega a url e desmembra os usuários, divididos pelo sinal '+'
    def to_python(self, value):
        return value.split('+')
    # pega uma lista e cria uma string ligada por '+' para a URL
    def to_url(self, values):
        return '+'.join(
            BaseConverter(self, item) for item in values
        )
