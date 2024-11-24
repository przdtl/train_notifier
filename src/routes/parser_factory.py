from common.parser_factory import ParserFactory

from routes.services.playwright import AbstractRoutesParser, TutuRoutesParser


class RoutesParserFactory(ParserFactory[AbstractRoutesParser]):
    pass


parser_factory = RoutesParserFactory()
parser_factory.register_parser(TutuRoutesParser)
