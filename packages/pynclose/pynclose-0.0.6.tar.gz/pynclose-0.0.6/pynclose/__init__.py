
from . import inclose
from . import export
from . import extract


def concepts(infile:str, min_ext:int, min_int:int) -> [(set, set)]:
    import importlib  # TODO: find a way to fix the bug described in run_test_dir/test_reusability_of_search.py
    importlib.reload(inclose)
    csv_file = inclose.run_search(infile, min_ext, min_int)
    yield from extract.from_csv_file(csv_file)
