import os as _os
import sys as _sys


# Python 2 needs to encode Julia strings with unicode as utf-8 before printing
def _sanitize_repr(s):
    if _sys.version_info < (3,):
        s = s.encode('utf-8')
    return s


def _iai_version_less_than(version):
    jleval = _Main.string("Base.thispatch(v\"", _Main.iai_version, "\")",
                          " < ",
                          "Base.thispatch(v\"", version, "\")")
    return _Main.eval(jleval)


def _requires_iai_version(required_iai_version, function_name):
    if _iai_version_less_than(required_iai_version):
        raise RuntimeError(
            "The function `" + function_name + "` in this version of the " +
            "`interpretableai` Python package requires IAI version " +
            required_iai_version + ". Please upgrade your IAI installation " +
            "to use this function.")


from .mixeddata import MixedData


# Configure julia with compiled_modules=False if requested
if 'IAI_DISABLE_COMPILED_MODULES' in _os.environ:  # pragma: no cover
    from julia import Julia
    Julia(compiled_modules=False)


# Load Julia with IAI_DISABLE_INIT to avoid interfering with stdout during load
_os.environ['IAI_DISABLE_INIT'] = 'True'
from julia import Main as _Main
del _os.environ['IAI_DISABLE_INIT']


# Run Julia setup code
_script_dir = _os.path.dirname(_os.path.realpath(__file__))
try:
    _Main.include(_os.path.join(_script_dir, "setup.jl"))
except ImportError as err:
    # Trim Julia stacktrace from message
    msg = str(err).split("\n")[0]
    from future.utils import raise_from
    raise_from(ImportError(msg), None)


# Hack to get a reference to IAI without `import`
import julia as _julia
_IAI = _julia.core.JuliaModuleLoader().load_module("Main.IAI")


# Import Julia modules
from julia import Random as _Random
def set_julia_seed(*args):
    """Set the random seed in Julia to `seed`.

    Julia Equivalent:
    `Random.seed! <https://docs.julialang.org/en/v1/stdlib/Random/index.html#Random.seed!>`

    Examples
    --------
    >>> set_julia_seed(seed)
    """
    return _Random.seed_b(*args)


# Load Julia packages
from .iaibase import *
from .iaitrees import *
from .optimaltrees import *
from .optimpute import *
from .optimalfeatureselection import *


def read_json(filename):
    """Read in a learner or grid saved in JSON format from `filename`.

    Julia Equivalent:
    `IAI.read_json <https://docs.interpretable.ai/IAIBase/stable/reference/#IAI.read_json>`

    Examples
    --------
    >>> read_json(filename)
    """
    def _get_learner_type(jl_obj):
        if _Main.isa(jl_obj, _IAI.OptimalTreeClassifier):
            lnr = OptimalTreeClassifier()
        elif _Main.isa(jl_obj, _IAI.OptimalTreeRegressor):
            lnr = OptimalTreeRegressor()
        elif _Main.isa(jl_obj, _IAI.OptimalTreeSurvivor):
            lnr = OptimalTreeSurvivor()
        elif _Main.isa(jl_obj, _IAI.OptimalTreePrescriptionMinimizer):
            lnr = OptimalTreePrescriptionMinimizer()
        elif _Main.isa(jl_obj, _IAI.OptimalTreePrescriptionMaximizer):
            lnr = OptimalTreePrescriptionMaximizer()
        elif _Main.isa(jl_obj, _IAI.OptimalFeatureSelectionClassifier):
            lnr = OptimalFeatureSelectionClassifier()
        elif _Main.isa(jl_obj, _IAI.OptimalFeatureSelectionRegressor):
            lnr = OptimalFeatureSelectionRegressor()

        return lnr

    jl_obj = _IAI.read_json_convert(filename)

    if _Main.isa(jl_obj, _IAI.GridSearch):
        lnr = _get_learner_type(_IAI.get_learner(jl_obj))
        grid = GridSearch(lnr)
        grid._jl_obj = jl_obj
        return grid
    else:
        lnr = _get_learner_type(jl_obj)
        Learner.__init__(lnr, jl_obj)
        return lnr
