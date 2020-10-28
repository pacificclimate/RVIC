import cProfile
import io
import pstats

from rvic.core.pycompat import py3


def run_test(rvic_module, config, np=None):
    pr = cProfile.Profile()
    pr.enable()

    try:
        if np:
            rvic_module(config, np)
        else:
            rvic_module(config)
        test_outcome = "Passed"
    except Exception as e:
        test_outcome = "Failed: {0}".format(e)

    pr.disable()
    if py3:
        s = io.StringIO()
    else:
        s = io.BytesIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()

    print("".center(100, "-"))
    print(".....Printing Profile Information.....".center(100))
    print("".center(100, "-"))
    print(s.getvalue())
    print("".center(100, "-"))

    print(f"\ttest_convert: {0}".format(test_outcome))

    assert test_outcome == "Passed"
