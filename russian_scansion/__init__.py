from .poetry_alignment import PoetryStressAligner
from .udpipe_parser import UdpipeParser
from .phonetic import Accents


from importlib import resources
from importlib.resources import files


def create_rpst_instance(models_dir: str=None) -> PoetryStressAligner:
    """
    This function loads all the necessary models and dictionaries,
    creates an RPST instance with default settings and returns it.

    By default the models and dictionary are loaded from module installation directory.
    You can path the path to this directory explicitly via `models_dir`.
    """
    models_dir = files("russian_scansion.models")
    #print('\nDEBUG@12 models_dir={}\n'.format(models_dir.joinpath('').__str__()))

    parser = UdpipeParser()
    parser.load(models_dir.joinpath('').__str__())

    accents = Accents(device="cpu")
    accents.load_pretrained(str(models_dir.joinpath('accentuator')))

    aligner = PoetryStressAligner(parser, accents, model_dir=str(models_dir.joinpath('scansion_tool')))
    aligner.max_words_per_line = 14

    return aligner
