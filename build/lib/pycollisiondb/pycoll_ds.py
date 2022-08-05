import json
import logging

from pyvalem.reaction import Reaction as PVReaction
import numpy as np

logger = logging.getLogger(__name__)

MAX_DATAPOINTS_FOR_MARKERS = 20


class PyCollDataSet:
    def __init__(self, filepath=None):
        self.filepath = filepath
        if filepath is not None:
            self.read_dataset()

    def read_dataset(self, filepath=None):
        if filepath is not None:
            self.filepath = filepath

        logger.debug(f"Reading dataset data from {self.filepath}...")
        with open(self.filepath) as fi:
            self.metadata = json.loads(fi.readline())
            assert fi.readline()[:4] == "----"
            self._read_xy(fi)
        logger.debug(f"{self.n} data points read in.")

        strict = not ("COM" in self.metadata["process_types"])
        self.reaction = PVReaction(self.metadata["reaction"], strict=strict)

    def _read_xy(self, fi):
        unc_perc = self.metadata["json_data"].get("unc_perc")
        lines = fi.readlines()

        self.n = len(lines)
        self.x, self.y, self.unc_lo, self.unc_hi = np.zeros((4, self.n))
        for i, line in enumerate(lines):
            fields = line.split()
            self.x[i] = float(fields[0])
            yfields = fields[1].split(":")
            self.y[i] = float(yfields[0])
            if len(yfields) > 1:
                if len(yfields) == 2:
                    self.unc_lo[i] = self.unc_hi[i] = yfields[1]
                else:
                    self.unc_lo[i], self.unc_hi[i] = yfields[1:]
            elif unc_perc:
                if unc_perc == 100:
                    # Don't let round-off leak non-zero values into ymin.
                    self.unc_lo[i] = self.unc_hi[i] = self.y[i]
                else:
                    self.unc_lo[i] = self.unc_hi[i] = self.y[i] * unc_perc / 100

    def plot_dataset(self, ax, use_latex=False, **kwargs):
        def get_error_bounds():
            ymin = (self.y - self.unc_lo)[::-1]
            if all(ymin <= 0):
                ymin = np.ones_like(ymin) * np.min(self.y[self.y > 0]) * 0.5
            ymax = self.y + self.unc_hi
            return ymin, ymax

        def add_error_bounds():
            px = np.append(self.x, self.x[::-1])
            ymin, ymax = get_error_bounds()
            py = np.append(ymax, ymin)
            ax.fill_between(px, py, alpha=0.1)

        def points_plot():
            if not any(self.unc_lo):
                (line,) = ax.plot(self.x, self.y, ls="", marker="o", **kwargs)
                return line

            yerr = (self.unc_lo, self.unc_hi)
            errorbar_container = ax.errorbar(
                self.x, self.y, yerr, ls="", marker="o", capsize=4
            )
            return errorbar_container.lines[0]

        def line_plot():
            (line,) = ax.plot(self.x, self.y, **kwargs)
            return line

        draw_line = self.n > MAX_DATAPOINTS_FOR_MARKERS
        if draw_line:
            line = line_plot()
            add_error_bounds()
        else:
            line = points_plot()

        ax.set_yscale("log")

        if use_latex:
            s_reaction = f"${self.reaction.latex}$"
        else:
            s_reaction = str(self.reaction)
        line.set_label(self.metadata["qid"] + ": " + s_reaction)
