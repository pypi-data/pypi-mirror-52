import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches
from matplotlib.axes import Axes
import matplotlib.ticker as mtick
import scipy.stats as st
from typing import List, Tuple


def _get_full_filename(fingerprint_dir: str, filename: str):
    if fingerprint_dir != "":
        if not os.path.exists(fingerprint_dir):
            os.mkdir(fingerprint_dir)
        full_filename = os.path.join(fingerprint_dir, filename)
    else:
        full_filename = filename
    return full_filename


def _gaussian_kde_smoothed_points(
    x, y,
    xmin, xmax, nx,
    ymin, ymax, ny,
    weights=None
):
    # based on
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html
    # X, Y = np.mgrid([xmin:xmax:(nx)j, ymin:ymax:(ny)j])
    X, Y = np.mgrid[xmin:xmax:(nx)*1j, ymin:ymax:(ny)*1j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values, weights=weights)
    Z = np.reshape(kernel(positions).T, X.shape)
    return Z


def _get_2d_hist_input(party_votes: List[int], valid_votes: List[int],
                       registered_voters: List[int],
                       zoom_onto: bool=False, weighted=False) -> \
                      Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert election data & settings to abstract histogram input.

    Useful for e.g. for the construction of 2D histograms: x, y, weights,
    bins where x, y, weights are the obvious observation data, bins is a tuple
    of x and y histogram interval limits given the zoom_onto parameter.
    """
    bins = [np.arange(0, 1, 0.01), np.arange(0, 1, 0.01)]
    party_votes = np.array(party_votes)
    valid_votes = np.array(valid_votes)
    registered_voters = np.array(registered_voters)

    if zoom_onto:
        bins[1] = 0.4 * bins[1]

    weights = None if not weighted else party_votes

    is_included = valid_votes != 0
    included_valid_votes = valid_votes[is_included]
    x = included_valid_votes / registered_voters[is_included]
    y = party_votes[is_included] / included_valid_votes
    included_weights = weights[is_included]

    return x, y, included_weights, bins


def _get_kde_smoothed_2d_histogram(x: np.ndarray, y: np.ndarray,
                                   weights: np.ndarray) -> np.ndarray:
    x = np.array(x)
    y = np.array(y)
    weights = np.array(weights)

    xmin, ymin = 0, 0
    xmax, ymax = 1, 1

    Z = _gaussian_kde_smoothed_points(
        x, y,
        xmin, xmax, 100,
        ymin, ymax, 100,
        weights=weights
    )

    Z = np.rot90(Z)

    return Z


def _normalize_hist_2d(hist: np.ndarray):
    shape = hist.shape
    as_vec = hist.reshape(shape[0] * shape[1])
    max_v = max(as_vec)
    min_v = min(as_vec)
    if min_v != 0:  # this will typically be zero
        hist = hist - min_v
    if max_v != min_v:
        hist = hist / (max_v - min_v)
    return hist


def _joint_normalize_hist_2ds(hists: List[np.ndarray]) -> List[np.ndarray]:
    as_vecs = [h.reshape(np.prod(h.shape)) for h in hists]
    max_v = max([max(v) for v in as_vecs])
    min_v = min([min(v) for v in as_vecs])
    if max_v == min_v and min_v == 0:
        return hists

    if min_v != 0:  # this will typically be zero
        hists = [h - min_v for h in hists]
    if max_v != min_v:
        hists = [h / (max_v - min_v) for h in hists]

    return hists


def _get_histogram_2d(x: np.ndarray, y: np.ndarray, weights: np.ndarray,
                      bins: Tuple[List[float], List[float]],
                      use_kde: bool) -> Tuple[np.ndarray]:
    # # normalize the weights, bearing in mind that a weight of 1 means no change
    # weights = len(weights) / sum(weights) * weights

    if not use_kde:
        ans, _, _ = np.histogram2d(x, y, bins, weights=weights, density=True)
        return ans
    else:
        ans = _get_kde_smoothed_2d_histogram(x, y, weights)
    # this case requires further normalization, some vis. methods (like
    # matplotlib's hist2d) do that by default otherwise
    #
    # hand implemented to avoid dependence on scikit-learn as would be suggested
    # in
    # https://stackoverflow.com/questions/21030391/how-to-normalize-an-array-in-numpy
    ans = _normalize_hist_2d(ans)
    return ans


def _plot_smoothed_hist_2d(x, y, weights=None, axes=None):
    # TODO: add norm_to_unit=False?
    new_plot = axes is None
    if not new_plot:
        dest = axes
    else:
        _, dest = plt.subplots(figsize=[8, 8])

    try:
        Z = _get_kde_smoothed_2d_histogram(x, y, weights)

        # some alternative color maps to consider: magma, ocean, bone, coolwarm
        dest.imshow(
            Z, cmap="viridis",
            extent=[0, 1, 0, 1]
        )

        if new_plot:
            plt.show()
    finally:
        if new_plot:
            plt.close()


def _apply_electoral_fingerprint_axes(axes: Axes):
    axes.set_xlabel("Turnout")
    axes.set_ylabel("Vote share")

    perc_fmt = mtick.PercentFormatter(xmax=1)
    # https://stackoverflow.com/questions/31357611/format-y-axis-as-percent
    # (almost :) )
    axes.xaxis.set_major_formatter(perc_fmt)
    axes.yaxis.set_major_formatter(perc_fmt)


def _save_fingerprint(fingerprint_dir, filename, quiet):
    if filename is not None:
        full_filename = _get_full_filename(fingerprint_dir, filename)
        plt.savefig(full_filename)
        if not quiet:
            print("plot saved as %s" % full_filename)


def plot_fingerprint(party_votes: List[int], valid_votes: List[int],
                     registered_voters: List[int], title: str,
                     filename: str=None, weighted: bool=True,
                     zoom_onto: bool=False, fingerprint_dir: str="",
                     quiet: bool=False, axes: Axes=None,
                     use_kde: bool=True):
    """
    Plot electoral fingerprint (a 2D histogram).
    Originally recommended to be used in conjunction with the winner party.

    :param party_votes: Array like of number of votes cast on the party
        depicted.
    :param valid_votes: Array like of valid votes (ballots) cast.
    :param registered_voters: Array like of all voters eligible to vote.
    :param title: Plot title.
    :param filename: Filename to save the plot under, None to prevent saving.
        A .png extension seems to work ;) Must not be used in conjunction with
        axes.
    :param weighted: Whether to use the number of votes won as a weight on the
        histogram.
    :param zoom_onto: Boolean, allows to magnify the plot by a factor of 5/2
        over the y axis (vote share).
    :param fingerprint_dir: Directory to save the fingerprint plot to.
    :param quiet: Whether to show the resulting plot, False prevents it.
    :param axes: MatPlotLib axes to plot onto. If left as None, a new plot will
        be generated. Must not be used in conjunction with filename.
    :param use_kde: Whether to use a default (Gaussian) kernel density
        estimation to smooth the plot. See scipy.stats.gaussian_kde for more.
        No finer grain control is available over the parameters at the minute.
    :return: None
    """
    # TODO: zooming in the KDE case

    assert filename is None or axes is None

    if axes is not None:
        dest = axes
    else:
        _, dest = plt.subplots()

    x, y, weights, bins = _get_2d_hist_input(
        party_votes, valid_votes, registered_voters, zoom_onto, weighted
    )
    try:
        # mainly for the KDE case, which does not tolerate NaNs, but neither is
        # the other case less correct if NaNs are removed, so...
        if use_kde:
            _plot_smoothed_hist_2d(x, y, weights=weights, axes=dest)
        else:
            dest.hist2d(
                x, y,
                bins=bins,
                weights=weights
            )
        dest.set_title(title)

        _apply_electoral_fingerprint_axes(dest)

        _save_fingerprint(fingerprint_dir, filename, quiet)
        if not quiet and axes is None:
            plt.show()
    finally:
        if axes is None:
            plt.close()


def _plot_comparative(values1: np.ndarray, values2: np.ndarray, axes: Axes):
    col1 = np.array([0.0, 0.5, 1.0])
    col2 = np.array([1.0, 0.5, 0.0])

    def colorize_intensity_matrix(matrix, col):
        return np.array([
            [col * value for value in row]
            for row in matrix
        ])

    map = (colorize_intensity_matrix(values1, col1) +
           colorize_intensity_matrix(values2, col2))
    axes.imshow(map, extent = [0, 1, 0, 1])


def _apply_legend(dest: Axes, legend_strings: List[str]):
    blue_patch = mpatches.Patch(color='blue', label=legend_strings[0])
    red_patch = mpatches.Patch(color='red', label=legend_strings[1])
    bbox=(1.5, 1.)
    dest.legend(handles=[blue_patch, red_patch], loc=1,bbox_to_anchor=bbox)


def _hist_sum(h: np.ndarray):
    return sum(h.reshape(np.prod(h.shape)))


def _histogram_asym_diff_in_votes(h1: np.ndarray, h2: np.ndarray,
                                  sum_votes1: float, sum_votes2: float,
                                  normalize: bool) -> Tuple[List[np.ndarray],
                                                            List[float]]:

    # utilize votes as invariant quantities
    h1 = h1 * sum_votes1 / _hist_sum(h1)
    h2 = h2 * sum_votes2 / _hist_sum(h2)

    diff = h1 - h2

    h1 = diff.copy()
    h1[h1 < 0] = 0
    h2 = -diff
    h2[h2 < 0] = 0
    # the last (2nd) one need not be calculated, as the "total of subtotals" is
    # the "total of totals"
    new_sum1 = _hist_sum(h1)
    if normalize:
        # joint normalization allows for mamtaining comparability
        h1, h2 = _joint_normalize_hist_2ds([h1, h2])
    return [h1, h2], [new_sum1, -((sum_votes1 - sum_votes2) - new_sum1)]


def plot_overlaid_fingerprints(party_votes: List[List[int]],
                               valid_votes: List[List[int]],
                               registered_voters: List[List[int]],
                               title: str=None,
                               filename: str=None, weighted: bool=True,
                               zoom_onto: bool=False, fingerprint_dir: str="",
                               quiet: bool=False, axes: Axes=None,
                               comparison_mode="asym_diff",
                               use_kde: bool=True,
                               legend_strings=None,
                               normalize_diffs=True) -> \
        Tuple[List[np.ndarray], List[float], List[float]]:
    """
    Plot multiple (currently this must be 2, i.e. k = 2) electoral fingerprints
    alpha blended onto the same chart, so that they can be visually compared in
    this way. Part of the input is effectively the n data points known.

    Currently they are plotted in a blue vs. red style. (Sorry colorblind
    people, something should happen to remedy this.)

    :param party_votes: Array like of number of votes cast on the party
        depicted. Size: k x n.
    :param valid_votes: Array like of valid votes (ballots) cast. Size: k x n.
    :param registered_voters: Number of voters registered. Size: k x n.
    :param title: Plot title.
    :param filename: Filename to save the plot under, None to prevent saving.
        A .png extension seems to work ;) Must not be used in conjunction with
        axes.
    :param weighted: Whether to use the number of votes won as a weight on the
        histogram.
    :param zoom_onto: Boolean, allows to magnify the plot by a factor of 5/2
        over the y axis (vote share).
    :param fingerprint_dir: Directory to save the fingerprint plot to.
    :param quiet: Whether to show the resulting plot, False prevents it.
    :param axes: MatPlotLib axes to plot onto. If left as None, a new plot will
        be generated. Must not be used in conjunction with filename.
    :param comparison_mode: Either "asym_diff" or "union", further modes are to
        be implemented.
        The visualization is similar to overlaid blue+red bitplanes, except that
        there is a grey halftone mixed in each bitplane
        (RGB = (1.0, 0.5, 0.0) vs (0, 0.5, 1.0)).

        "union" is a simple overlay (blue+red turning white where overlaps,
        "asym_diff" is a simple difference of the interpolated votes per cell,
            positive being left in the first, (absolutes of the) negative values
            in the second histogram bitplane.
    :param use_kde: Whether to use a default (Gaussian) kernel density
        estimation to smooth the plot. See scipy.stats.gaussian_kde for more.
        No finer grain control is available over the parameters at the minute.
    :param legend_strings: Strings to display in the optional legend for each
        fingerprint color, in the order they are listed in the vote data lists.
    :return: A tuple of the (weighted, normalized) list of histograms, a
        list of how many party votes these histograms represent, and a list of
        the party vote percentages per each histogram.
    """

    assert len(party_votes) == 2
    assert len(valid_votes) == 2
    assert len(registered_voters) == 2
    assert comparison_mode in ["union", "asym_diff"]
    assert legend_strings is None or len(legend_strings) == 2

    zipped = zip(party_votes, valid_votes, registered_voters)
    if axes is not None:
        dest = axes
    else:
        _, dest = plt.subplots()

    try:
        hists = []
        vote_shares = []
        for act_party_votes, act_valid_votes, act_registered_voters in zipped:
            vote_shares.append(sum(act_party_votes) / sum(act_valid_votes))
            # get abstract histogram input
            x, y, w, bins = _get_2d_hist_input(act_party_votes, act_valid_votes,
                                               act_registered_voters,
                                               zoom_onto, weighted)
            # calculate histogram values
            hist = _get_histogram_2d(x, y, w, bins, use_kde)

            hists.append(hist)

        sum_votes = [sum(party_votes[0]), sum(party_votes[1])]
        if comparison_mode == "asym_diff":
            # joint normalized (i.e. visually comparable) histogram of the
            # difference of vote distribution histograms
            hists, sum_votes = _histogram_asym_diff_in_votes(
                hists[0], hists[1], sum_votes[0], sum_votes[1], normalize_diffs
            )

        _plot_comparative(hists[0], hists[1], dest)
        _apply_electoral_fingerprint_axes(dest)
        if title is not None:
            dest.set_title(title)

        if legend_strings is not None:
            _apply_legend(dest, legend_strings)

        _save_fingerprint(fingerprint_dir, filename, quiet)

        if not quiet and axes is None:
            plt.show()
    finally:
        if axes is None:
            plt.close()

    return hists, sum_votes, vote_shares


def plot_explanatory_fingerprint_responses(filename: str=None,
                                           quiet: bool=False,
                                           fontsize=12) -> None:
    """
    Plot a fingerprint explanation chart, optionally save/don't show it.
    Election fingerprints may be difficult to take in at first.

    :param filename: The figure is saved under this filename as an image if
        specified.
    :param quiet: Whether to avoid showing the plot.
    :param fontsize: Experimentally found that 15 is a good fit for a plot of
        pyplot.rcparams["figure.figsize"] = [9, 7], the default value seemed to
        work with the default plot size.
    :return:
    """
    fig, ax = plt.subplots()
    try:
        ax.set_title("Some responses of the election\n"
                     "fingerprint of a party to impacts",
                     fontsize=fontsize)
        ax.set_xlabel("Turnout")
        ax.set_ylabel("Vote share")
        perc_fmt = mtick.PercentFormatter(xmax=1)
        ax.xaxis.set_major_formatter(perc_fmt)
        ax.yaxis.set_major_formatter(perc_fmt)

        ax.text(0.75, 0.65,
                "+ votes\nof this\n"
                "\u21D2\n"
                "+ share\n+ turnout",
                fontsize=fontsize)
        ax.text(0.75, 0.15,
                "+ votes\nof other(s)\n"
                "\u21D2\n"
                "- share\n+ turnout",
                fontsize=fontsize)
        ax.text(0.1, 0.65,
                "- votes\nof other(s)\n"
                "\u21D2\n"
                "+ share\n- turnout",
                fontsize=fontsize)
        ax.text(0.1, 0.15,
                "- votes\nof this\n"
                "\u21D2\n"
                "- share\n- turnout",
                fontsize=fontsize)

        ax.text(0.40, 0.8, "\\\u263A/ party", fontsize=fontsize * 1.2)
        ax.text(0.40, 0.2, "/\u2639\\ party", fontsize=fontsize * 1.2)

        for dx in[-0.1, 0.1]:
            for dy in [-0.1, 0.1]:
                ax.arrow(0.5 + dx / 2, 0.5 + dy / 2, dx, dy,
                         head_width=0.025, head_length=0.025)

        if filename is not None:
            plt.savefig(filename)
            if not quiet:
                print("plot saved as %s" % filename)
        if not quiet:
            plt.show()
    finally:
        plt.close()


def plot_explanatory_fingerprint_dynamics(filename: str=None,
                                          quiet: bool=False) -> None:
    """
    Paint plots which demonstrate how a point of an electoral fingerprint plot
    exactly moves when impacted by e.g. removal/addition/replacement of votes.

    This should give an impression of what certain shapes of patches might
    represent.

    :param filename: The figure is saved under this filename as an image if
        specified.
    :param quiet: Whether to avoid showing the plot.
    :return:
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    try:
        _apply_electoral_fingerprint_axes(ax1)
        x = np.arange(0.01, 1, 0.01)
        for vote_share in np.arange(0.05, 0.95, 0.1):
            y = vote_share / x
            is_ok = y < 1
            ax1.plot(x[is_ok], y[is_ok], color="blue")

        ax1.set_title("Fixed party votes, others' vary")

        r = 1E+6
        for o in 1E+6 * np.arange(0.1, 0.9, 0.1):
            p = np.arange(0, 100, 0.01) * o
            is_ok = (p + o) <= r

            vote_share = p / (p + o)
            turnout = (p + o) / r
            ax2.plot(turnout[is_ok], vote_share[is_ok], color="blue")
        _apply_electoral_fingerprint_axes(ax2)
        ax2.set_title("Others' fixed, the party's votes vary")

        r = 1E+6
        for v in r * np.arange(0.1, 1.1, 0.2):
            t = np.arange(0, 1, 0.01)  # parameter
            # p + o = v
            p = t * v
            o = (1 - t) * v

            is_ok = (p + o) <= r

            vote_share = p / v
            turnout = (o + p) / r   # to get a vector
            ax3.plot(turnout[is_ok], vote_share[is_ok], color="blue")
        _apply_electoral_fingerprint_axes(ax3)
        ax3.set_title("Party's votes swapped with others'")

        for vote_share in np.arange(0, 1.1, 0.2):
            turnout = np.arange(0, 1.01, 0.01)  # parameter
            ax4.plot(turnout, [vote_share] * len(turnout), color="blue")
        _apply_electoral_fingerprint_axes(ax4)
        ax4.set_title("Party equally popular everywhere")

        plt.tight_layout()
        if filename is not None:
            plt.savefig(filename)
            if not quiet:
                print("plot saved as %s" % filename)
        if not quiet:
            plt.show()
    finally:
        plt.close()


def plot_animated_fingerprints(party_votes: List[int],
                               valid_votes: List[int],
                               registered_voters: List[int],
                               frame_inclusions: List[List[bool]],
                               title: str,
                               filename: str=None,
                               weighted: bool=True,
                               zoom_onto: bool=False,
                               fingerprint_dir: str="", quiet: bool=False,
                               interval: int=200,
                               frame_title_exts: List[str]=None):

    """
    Can be used to plot an animated .gif showing how the distribution of votes
    changes over various subsets of the electoral wards involved. Technically,
    if party_votes, valid_votes, registered_voters are considered columns, the
    subsets boil down to various selections of the rows, specified by the
    frame_inclusions parameter.

    For the description of the rest of the parameters see plot_fingerprint().

    :param frame_inclusions: An array-like of row filters, each specifying a
        frame. Each row filter is just an array-like of booleans telling to
        include the nth row whenever the nth value is True.
    :param axes: axes to plot to, None to create a new plot.
    :param interval: animation interval to elapse between frames, in millisecs.
    :param frame_title_exts: Optional array-like of frame-specific text to
        display on each frame, such as a frame index. Currently it appears in
        the top left hand corner.
        This parameter is experimental and might change.
    :return: None
    """

    """
    based on
    https://eli.thegreenplace.net/2016/drawing-animated-gifs-with-matplotlib/
    """
    fig, ax = plt.subplots()  # type: object, Axes

    def update(frame_index):
        include = frame_inclusions[frame_index]
        plot_fingerprint(
            party_votes[include], valid_votes[include],
            registered_voters[include], title,
            weighted=weighted, zoom_onto=zoom_onto,
            quiet=True, axes=ax
        )
        if frame_title_exts is not None:
            t = ax.text(0.1, 0.9, frame_title_exts[frame_index], color="white")
            t.set_bbox(dict(facecolor='black', alpha=1, edgecolor='black'))

    fig.set_tight_layout(True)
    anim = FuncAnimation(fig, update,
                         frames=list(range(len(frame_inclusions))),
                         interval=interval)
    if filename != "":
        full_filename = _get_full_filename(fingerprint_dir, filename)
        anim.save(full_filename, dpi=80, writer='imagemagick')
    if not quiet:
        plt.show()


if __name__ == "__main__":
    rv = np.random.uniform(20, 40, 300)
    vv = rv * np.random.uniform(0.6, 0.8, 300)
    pv = vv * np.random.uniform(0.6, 0.8, 300)

    rv2 = np.random.uniform(20, 40, 300)
    vv2 = rv2 * np.random.uniform(0.6, 0.8, 300)
    pv2 = vv2 * np.random.uniform(0.6, 0.7, 300)

    fig, [ax1, ax2] = plt.subplots(1, 2)

    plot_fingerprint(
        party_votes=pv,
        valid_votes=vv,
        registered_voters=rv,
        title="title1",
        use_kde=True,
        axes=ax1
    )
    plot_overlaid_fingerprints(
        party_votes=[pv, pv2],
        valid_votes=[vv, vv2],
        registered_voters=[rv, rv2],
        title="title1",
        use_kde=True,
        axes=ax2
    )
    plt.tight_layout()

    plt.show()
