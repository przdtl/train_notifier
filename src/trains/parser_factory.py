from common.parser_factory import ParserFactory

from trains.services.playwright import AbstractTrainParser, TutuTrainParser


class TrainsParserFactory(ParserFactory[AbstractTrainParser]):
    pass


parser_factory = TrainsParserFactory()
parser_factory.register_parser(TutuTrainParser)
