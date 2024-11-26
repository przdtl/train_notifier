from common.parser_factory import ParserFactory

from tickets.services.playwright import AbstractTicketsParser, TutuTicketsParser


class TrainsParserFactory(ParserFactory[AbstractTicketsParser]):
    pass


parser_factory = TrainsParserFactory()
parser_factory.register_parser(TutuTicketsParser)
