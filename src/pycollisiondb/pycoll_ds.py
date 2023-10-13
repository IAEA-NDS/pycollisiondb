import json
import logging

from pyvalem.reaction import Reaction as PVReaction
import numpy as np
from pyqn.units import Units

logger = logging.getLogger(__name__)

MAX_DATAPOINTS_FOR_MARKERS = 20


class PyCollDataSetValidationError(Exception):
    pass


class PyCollDataSet:
    def __init__(self, filepath=None):
        self.dataset_ready = False
        self.is_valid = None
        self.filepath = filepath
        self.metadata = None
        if filepath is not None:
            self.read_dataset()

    def __repr__(self):
        if not self.metadata:
            return "<Uninitialized PyCollDataSet>"
        qid, reaction = self.metadata["qid"], self.metadata["reaction"]
        return f"{qid}: {reaction}"

    def read_dataset(self, filepath=None):
        if filepath is not None:
            self.filepath = filepath

        logger.debug(f"Reading dataset data from {self.filepath}...")
        with open(self.filepath) as fi:
            self.metadata = json.loads(fi.readline())
            assert fi.readline()[:4] == "----"
            self._read_xy(fi)
        self.dataset_ready = True
        logger.debug(f"{self.n} data points read in.")

        strict = not ("COM" in self.metadata["process_types"])
        self.reaction = PVReaction(self.metadata["reaction"], strict=strict)

    def _read_xy(self, fi):
        unc_perc = self.metadata.get("unc_perc")
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

    def print_values(self):
        columns = self.metadata["columns"]
        header = (
            f"{columns[0]['name']} / {columns[0]['units']} "
            f"{columns[1]['name']} / {columns[1]['units']}"
        )
        data_table = [header]
        for x, y in zip(self.x, self.y):
            data_table.append(f"{x} {y}")
        return "\n".join(data_table)

    def plot_dataset(self, ax, use_latex=False, label_axes=False, **kwargs):
        try:
            label_fields = kwargs.pop("label")
        except KeyError:
            label_fields = ("qid", "reaction")

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

        label = ", ".join([self._get_label(k) for k in label_fields])
        line.set_label(label)

        if label_axes:
            self.label_axes(ax, use_latex)

    def label_axes(self, ax, use_latex=False):
        columns = self.metadata["columns"]
        if use_latex:
            x_units = Units(columns[0]["units"])
            y_units = Units(columns[1]["units"])
            ax.set_xlabel(columns[0]["name"] + "/" + f"${x_units.latex}$")
            ax.set_ylabel(columns[1]["name"] + "/" + f"${y_units.latex}$")
        else:
            x_units = columns[0]["units"]
            y_units = columns[1]["units"]
            ax.set_xlabel(columns[0]["name"] + "/" + x_units)
            ax.set_ylabel(columns[1]["name"] + "/" + y_units)

    def _get_label(self, metadata_key):
        if metadata_key in ("qid", "reaction"):
            return self.metadata[metadata_key]

        if metadata_key in ("process_types", "refs"):
            return ",".join(self.metadata[metadata_key].keys())

    def convert_units(self, column_name, to_units):
        def _get_data_arrays(column_name):
            columns = self.metadata["columns"]
            if columns[0]["name"] == column_name:
                return columns[0], self.x, None, None
            elif columns[1]["name"] == column_name:
                return columns[1], self.y, self.unc_lo, self.unc_hi
            else:
                raise ValueError(f"No such column: {column_name}")

        column, arr, unc_lo, unc_hi = _get_data_arrays(column_name)
        from_units = column.get("units")
        from_units = Units(from_units)
        to_units = Units(to_units)
        fac = from_units.conversion(to_units)
        arr *= fac
        if unc_lo is not None:
            unc_lo *= fac
        if unc_hi is not None:
            unc_hi *= fac
        column["units"] = str(to_units)

    def validate(self, raise_exception=False):
        self.validation_messages = []

        def raise_or_report(msg):
            if raise_exception:
                raise PyCollDataSetValidationError(msg)
            self.validation_messages.append(msg)

        if not self.dataset_ready:
            raise_or_report("Dataset not ready for validation: no data!")

        def x_is_monotonic():
            return np.all(np.diff(self.x) > 0)

        def y_is_nonnegative():
            return np.all(self.y >= 0)

        if not x_is_monotonic():
            raise_or_report("x-data not monotonic!")

        if not y_is_nonnegative():
            raise_or_report("y-data not non-negative!")

        if self.validation_messages:
            self.is_valid = False
            return False

        self.is_valid = True
        return True
