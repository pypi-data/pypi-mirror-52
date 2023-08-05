from typing import Tuple, Optional
import warnings
import numpy as np
import scipy.sparse as sp
from scipy.stats import zscore, percentileofscore

from Orange.data import Domain, Table
from Orange.preprocess.preprocess import Preprocess
from Orange.util import Enum


class LogarithmicScale(Preprocess):
    Base = Enum("LogarithmicScale", ("BinaryLog", "NaturalLog", "CommonLog"),
                qualname="LogarithmicScale.Base")
    BinaryLog, NaturalLog, CommonLog = Base

    def __init__(self, base=BinaryLog):
        self.base = base

    def __call__(self, data):
        new_data = data.copy()
        if self.base == LogarithmicScale.BinaryLog:
            new_data.X = np.log2(1 + data.X)
        elif self.base == LogarithmicScale.NaturalLog:
            new_data.X = np.log(1 + data.X)
        elif self.base == LogarithmicScale.CommonLog:
            new_data.X = np.log10(1 + data.X)
        return new_data


class Binarize(Preprocess):
    Condition = Enum("Binarize", ("GreaterOrEqual", "Greater"),
                     qualname="Binarize.Condition")
    GreaterOrEqual, Greater = Condition

    def __init__(self, condition=GreaterOrEqual, threshold=1):
        self.condition = condition
        self.threshold = threshold

    def __call__(self, data):
        new_data = data.copy()
        if self.condition == Binarize.GreaterOrEqual:
            new_data.X = np.where(data.X >= self.threshold, 1, 0)
        elif self.condition == Binarize.Greater:
            new_data.X = np.where(data.X > self.threshold, 1, 0)
        return new_data


class Normalize(Preprocess):
    Method = Enum("Normalize", ("CPM", "Median"),
                  qualname="Normalize.Method")
    CPM, Median = Method

    def __init__(self, method=CPM):
        self.method = method

    def __call__(self, *args):
        raise NotImplementedError

    def normalize(self, *args):
        raise NotImplementedError


class NormalizeSamples(Normalize):
    def __call__(self, data):
        new_data = data.copy()
        new_data.X = self.normalize(data.X)
        return new_data

    def normalize(self, table):
        row_sums = np.nansum(table, axis=1)
        row_sums[row_sums == 0] = 1
        table = table / row_sums[:, None]
        factor = np.nanmedian(row_sums) \
            if self.method == NormalizeSamples.Median else 10 ** 6
        return table * factor


class NormalizeGroups(Normalize):
    def __init__(self, group_var, method=Normalize.CPM):
        super().__init__(method)
        self.group_var = group_var

    def __call__(self, data):
        group_col = data.get_column_view(self.group_var)[0]
        group_col = group_col.astype("int64")
        new_data = data.copy()
        new_data.X = self.normalize(data.X, group_col)
        return new_data

    def normalize(self, table, group_col):
        group_sums = np.bincount(group_col, np.nansum(table, axis=1))
        group_sums[group_sums == 0] = 1
        group_sums_row = np.zeros_like(group_col)
        medians = []
        row_sums = np.nansum(table, axis=1)
        for value, group_sum in zip(np.unique(group_col), group_sums):
            mask = group_col == value
            group_sums_row[mask] = group_sum
            if self.method == NormalizeGroups.Median:
                medians.append(np.nanmedian(row_sums[mask]))
        factor = np.min(medians) \
            if self.method == NormalizeGroups.Median else 10 ** 6
        return table / group_sums_row[:, None] * factor


class Standardize(Preprocess):
    def __init__(self, lower_bound=None, upper_bound=None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __call__(self, data):
        new_data = data.copy()
        with np.errstate(invalid="ignore"):
            new_data.X = np.nan_to_num(zscore(data.X))
        if self.lower_bound is not None or self.upper_bound is not None:
            np.clip(new_data.X, self.lower_bound, self.upper_bound, new_data.X)
        return new_data


class SelectMostVariableGenes(Preprocess):
    Method = Enum("SelectMostVariableGenes",
                  ("Dispersion", "Variance", "Mean"),
                  qualname="SelectMostVariableGenes.Method")
    Dispersion, Variance, Mean = Method

    def __init__(self, method=Dispersion, n_genes=1000, n_groups=20):
        self.method = method
        self.n_genes = n_genes
        self.n_groups = n_groups if n_groups and n_groups > 1 else 1

    def __call__(self, data):
        n_groups = min(self.n_groups, len(data.domain.attributes))
        mean = np.nanmean(data.X, axis=0)
        variance = np.nanvar(data.X, axis=0)
        percentiles = [percentileofscore(mean, m) for m in mean]
        _, bins = np.histogram(percentiles, n_groups)
        bin_indices = np.digitize(percentiles, bins, True)
        # Right limit is treated differently in histogram and digitize
        # See https://github.com/numpy/numpy/issues/4217
        bin_indices[bin_indices == 0] = 1

        zscores = np.zeros_like(mean)
        for group in range(n_groups):
            group_indices, = np.where(bin_indices == group + 1)
            if self.method == SelectMostVariableGenes.Dispersion:
                group_mean = mean[group_indices]
                group_scores = np.divide(
                    variance[group_indices], group_mean,
                    out=np.zeros_like(group_mean), where=group_mean != 0
                )
            elif self.method == SelectMostVariableGenes.Variance:
                group_scores = variance[group_indices]
            elif self.method == SelectMostVariableGenes.Mean:
                group_scores = mean[group_indices]

            with np.errstate(invalid="ignore"):
                zscores[group_indices] = zscore(group_scores)

        indices = np.argsort(np.nan_to_num(zscores))[-self.n_genes:]
        return self._filter_columns(data, indices)

    @staticmethod
    def _filter_columns(data, indices):
        indices = sorted(indices)
        domain = data.domain
        attrs, cls, metas = domain.attributes, domain.class_vars, domain.metas
        domain = Domain(tuple(np.array(attrs)[indices]), cls, metas)
        return data.transform(domain)


class DropoutWarning(Warning):
    pass


class DropoutGeneSelection(Preprocess):
    def __init__(self, n_genes=None, decay=1, x_offset=5, y_offset=0.02,
                 threshold=0, at_least=0):
        self.n_genes = n_genes
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.decay = decay
        self.threshold = threshold
        self.at_least = at_least

    def __call__(self, data: Table) -> Table:
        zero_rate, mean_expr = self.detection(data.X)
        selected = self.select_genes(zero_rate, mean_expr)
        if sum(selected) < self.n_genes:
            warnings.warn(f"{sum(selected)} genes selected", DropoutWarning)
        return self.filter_columns(data, selected)

    def detection(self, table: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        mask = table > self.threshold
        if sp.issparse(table):
            zero_rate = 1 - np.squeeze(np.array(mask.mean(axis=0)))
            A = table.multiply(mask)
            A.data = np.log2(A.data)
            mean_expr = np.zeros_like(zero_rate) * np.nan
            detected = zero_rate < 1
            detected_mean = np.squeeze(np.array(A[:, detected].mean(axis=0)))
            mean_expr[detected] = detected_mean / (1 - zero_rate[detected])
        else:
            zero_rate = 1 - np.mean(mask, axis=0)
            mean_expr = np.zeros_like(zero_rate) * np.nan
            detected = zero_rate < 1
            mean_expr[detected] = np.nanmean(
                np.where(table[:, detected] > self.threshold,
                         np.log2(table[:, detected]), np.nan), axis=0)

        low_detection = np.array(np.sum(mask, axis=0)).squeeze()
        zero_rate[low_detection < self.at_least] = np.nan
        mean_expr[low_detection < self.at_least] = np.nan
        return zero_rate, mean_expr

    def select_genes(self, zero_rate: np.ndarray,
                     mean_expr: np.ndarray) -> np.ndarray:
        args = (mean_expr, zero_rate)
        return self.__get_selected(*args) if self.n_genes is None \
            else self.__bisection(*args)

    def __bisection(self, mean_expr, zero_rate):
        low, up = 0, 10
        for t in range(100):
            selected = self.__get_selected(mean_expr, zero_rate)
            if np.sum(selected) == self.n_genes:
                break
            elif np.sum(selected) < self.n_genes:
                up = self.x_offset
                self.x_offset = (self.x_offset + low) / 2
            else:
                low = self.x_offset
                self.x_offset = (self.x_offset + up) / 2
        return selected

    def __get_selected(self, mean_expr, zero_rate):
        nonan = ~np.isnan(zero_rate)
        sel = np.zeros_like(zero_rate).astype(bool)
        x = mean_expr[nonan]
        y = self.y(x, self.decay, self.x_offset, self.y_offset)
        sel[nonan] = (zero_rate[nonan] > y)
        return sel

    @staticmethod
    def y(x, decay, x_offset, y_offset):
        return np.exp(-decay * (x - x_offset)) + y_offset

    @staticmethod
    def filter_columns(data: Table, mask: np.ndarray) -> Table:
        domain = data.domain
        return data.transform(Domain(tuple(np.array(domain.attributes)[mask]),
                                     domain.class_vars,  domain.metas))
