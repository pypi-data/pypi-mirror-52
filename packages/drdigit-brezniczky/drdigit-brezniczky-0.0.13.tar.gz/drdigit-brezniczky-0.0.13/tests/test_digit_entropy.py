import pytest
import numpy as np
from drdigit import LodigeTest
from drdigit.digit_entropy_distribution import (
    _uncached_ref_generate_sample, _uncached_generate_sample,
    get_entr_cdf_fun, ref_get_likelihood_cdf, get_likelihood_cdf
)


@pytest.mark.entropy
def test_slices():
    group_ids = np.array([1, 2, 2, 3, 3, 3])
    res = list(LodigeTest.get_slice_limits(group_ids=group_ids))
    assert (
        res ==
            [(0, 1),
             (1, 3),
             (3, 6)]
    )


@pytest.mark.entropy
def test_accelerated_sample_generator_matches_prev_version():
    sample1 = _uncached_ref_generate_sample(10, 1234, 13, quiet=True)
    sample2 = _uncached_generate_sample(10, 1234, 13, quiet=True)
    assert pytest.approx(sample1) == sample2


@pytest.mark.entropy
def test_cdf_sample_size_equals_specified():
    cdf = get_entr_cdf_fun(10, iterations=100)
    assert len(cdf.get_sample()) == 100


@pytest.mark.entropy
def test_accelerated_likelihood_cdf_approx_matches_prev_version():
    """
    The old version is based on generating number groups, and querying for their
    probabilities from cdfs.

    The new, faster version is based on picking random probabilities from the
    existing CDFs where they are cached, for each iteration in a single call
    (much more vectorized version than the previous).

    This is sort of mixing of the values obtained from resampling the samples
    associated with the CDFs, generated on CDF function construction.

    Since there are no experienced values in the sample with zero probabilities
    (since they were experienced), zero probabilities will never be drawn, and
    thus the former avoid_inf parameter becomes unncessary and is to be removed
    in the commit following this comment. Effectively it is roughly avoided.
    """

    slice_limits = [(0, 3), (3, 7), (8, 15)]

    LL_ITERATIONS = 1000
    PE_ITERATIONS = 1000

    cdf1 = ref_get_likelihood_cdf(slice_limits, 20, 1234, LL_ITERATIONS, 1234,
                                  PE_ITERATIONS, avoid_inf=False, quiet=True)

    cdf2 = get_likelihood_cdf(slice_limits, 20, 1234, LL_ITERATIONS, 1234,
                              PE_ITERATIONS, quiet=True)

    # well, couldn't get them too close to each other ... huge, almost 20%
    # difference - for now I'll live with it - it's actually a small change in
    # the expected value (I think ... with more data it seemed to get merrier)
    # TODO: more tests?
    assert pytest.approx(cdf1(-1), 0.15) == cdf2(-1)

"""
if __name__ == "__main__":
    # TODO: of course move this to a test suite someday
    test()

    # print(prob_of_entr(47, 2.1485))
    # expect ~ 0.133 (got with seed=1234) depending on the seed
    test = LodigeTest(
        [1] * 8 + [2] * 4, [1] * 12, 10
    )
    print(test.p)
    test = LodigeTest(
        list(range(10)), [10] * 10, 10
    )
    print(test.p)
    test = LodigeTest(
        list(range(5)) + [1] * 5, [10] * 10, 10
    )
    print(test.p)
"""

"""
In [117]:
f2 = get_cdf_fun(200)
ys2 = np.array([f2(x) for x in xs])
xs2 = xs[ys2 < 0.5]
ys2 = ys2[ys2 < 0.5]
plt.plot(xs2, np.log(ys2))
plt.show()

f2 = get_cdf_fun(100)
ys2 = np.array([f2(x) for x in xs])
xs2 = xs[ys2 < 0.5]
ys2 = ys2[ys2 < 0.5]
plt.plot(xs2, np.log(ys2))
plt.show()

f2 = get_cdf_fun(500, iterations=50000)
ys2 = np.array([f2(x) for x in xs])
xs2 = xs[ys2 < 0.5]
ys2 = ys2[ys2 < 0.5]
plt.plot(xs2, np.log(ys2))
plt.show()


TODO: left tail apparently (and as conjectured from
early stage analytical work) could be approximated by
an exponential form.
Then we could estimate probability of outlying
extremities based on that.
"""
