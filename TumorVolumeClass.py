# Tumor volume module for loading, ana,yzing, summarizing, and ploting tumor volume data.
#
# Acknowledgements: Source code inspired by the PDXNet Consortium and the following publications:
#    Systematic Establishment of Robustness and Standards in Patient-Derived Xenograft
#         Experiments and Analysis Cancer Res (2020) 80 (11): 2286–2297
#    PDXNet portal: patient-derived Xenograft model, data, workflow and tool discovery
#         NAR Cancer, Volume 4, Issue 2, June 2022
#    Assessment of Patient-Derived Xenograft Growth and Antitumor Activity:
#         The NCI PDXNet Consensus, Mol Cancer Ther (2024) 23 (7): 924–938
#

# To Do

# Import modules

# Utilities
import copy
import logging
import os
import re
from pathlib import Path

# Data
import pandas as pd
import numpy as np
from scipy.stats import sem
from typing import Optional

# Computation
import math
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

# Visualization
import matplotlib.pyplot as plt


# Set up logger
# Create logs directory if it does not exist
os.makedirs("logs", exist_ok=True)
log_file = os.path.join("logs", "app.log")
logging.basicConfig(
    level=logging.INFO,                  # Set level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),   # Log to file
        logging.StreamHandler()          # Log to console
    ]
)

logger = logging.getLogger(__name__)

# Utility
def sanitize_column_names(column_name:str):
    """
    Make a column name safe by replacing spaces and non-alphanumeric characters.

    Args:
        column_name: The original column name

    Returns:
        A sanitized column string
    """
    # Replace spaces with underscores
    safe_name = column_name.replace(' ', '_')

    # Keep only alphanumeric characters, underscores, hyphens, and dots
    safe_name = re.sub(r'[^\w\-.]', '_', safe_name)

    # Remove multiple consecutive underscores
    safe_name = re.sub(r'_+', '_', safe_name)

    # Remove leading/trailing underscores
    safe_name = safe_name.strip('_')

    return safe_name.lower()
def pad_number(s: str, width: int = 3) -> str:
    """
    Finds the single number in the string and pads it with leading zeros
    so that it has length = width.
    """
    return re.sub(r"(\d+)", lambda m: m.group(1).zfill(width), s)
def pad_all_numbers(s: str, min_width: int = 4) -> str:
    """
    Pads every numeric substring in the input string so that
    each one has at least min_width digits.
    Larger numbers keep their original length.
    """

    def repl(match):
        num = match.group(0)
        width = max(min_width, len(num))
        return num.zfill(width)

    return re.sub(r"\d+", repl, s)
def column_print(string_list:list, number_of_columns: int = 2, space: int = 5, indent="     ", sort_list = False):
    """
    Utility printing XML component summaries to the command line

    :param string_list: A list of strings that describe information stored in the annotation file
    :param number_of_columns: The number of columns to use when printing the list
    :param space: The space between columns
    :return: None is returned
    """
    # Pad strings to the same length and calculate the number of rows to print
    width = max([len(string) for string in string_list])+space
    string_list = [string.ljust(width) for string in string_list]
    if sort_list:
        string_list.sort()
    num_complete_rows = len(string_list)//number_of_columns
    remaining_entries = len(string_list)%number_of_columns

    # Use logger utility to write rows to the command line
    for r in range(num_complete_rows):
        start = r * number_of_columns
        end   = start + number_of_columns
        logger.info(indent+" ".join(string_list[start:end]))
    if remaining_entries > 0:
        logger.info(indent+" ".join(string_list[num_complete_rows * number_of_columns:]))
def write_title_list(variable_name:str, value_list:list):
    logger.info(f"{variable_name}: {', '.join(value_list)}")

# Main class
class TumorVolumeTimeSeriesClass():
    # Init
    def __init__(self, time_day:Optional[np.ndarray], tumor_volume:Optional[np.ndarray],
                 tumor_weigth:Optional[np.ndarray]=None, contributor:str|None = None, arm:str|None = None,
                 study_group:str|None = None, study:str|None = None, pdx_id:str|None = None,
                 tumor:str|None=None, disease_type:str|None=None, matched_controls:str|None=None,
                 volume_units="mm^3", weight_units="mg"):

        # Class variables
        # Tumor volume time series variables
        self.time_day:Optional[np.ndarray] = time_day.copy()
        self.tumor_volume:Optional[np.ndarray] = tumor_volume.copy()
        if tumor_weigth is not None:
            self.tumor_weight:Optional[np.ndarray] = tumor_weigth.copy()

        # Save units
        self.volume_units = volume_units
        self.weight_units = weight_units

        # Descriptions
        self.contributor:str|None = contributor
        self.arm:str|None = arm
        self.study_group:str|None = study_group
        self.study:str|None = study
        self.pdx_id:str|None = pdx_id
        self.tumor:str|tumor = tumor
        self.disease_type:str|disease_type = disease_type
        self.matched_controls:str|matched_controls = matched_controls

        # Compute variables
        self.num_points = len(time_day)
        self.max_day = max(self.time_day)
        self.auc, self.normalized_auc = self.compute_auc()


        # Transforms
        self.tv_transform_options = ["No Transform", "Percent Change", "Prop. Vol. Change", "Percent Prgress/Regress"]
        self.tv_transform_dict = {"No Transform":self.tv_to_tv,
                                  "Percent Change":self.tv_percent_change,
                                  "Prop. Vol. Change":self.tv_proportion_volume_change,
                                  "Percent Prgress/Regress":self.tv_percent_prog_regres_endpoint}
        self.tv_transform_str = "No Transform"
        self.tv_transform_f = self.tv_to_tv

        # Objective Response
        # Objective Response Definition
        # "CR":#08306B # Deep Blue, "PR":#2171B5 # Blue, "SD":#BDBDBD # Gray, "PD":#D94801 # Red-Orange
        self.default_response_color = "#CCCCCC"
        self.objective_response_names = {
            "CR": "Complete Response",
            "PR": "Partial Response",
            "SD": "Stable Disease",
            "PD": "Progressive Disease",
            "" : "Not Defined"}
        self.objective_response_colors: dict[str, str] = \
            {"CR": "#08306B",
             "PR": "#2171B5",
             "SD": "#BDBDBD",
             "PD": "#D94801"}
        self.objective_response_colors[""] = self.default_response_color

        self.CR_THRESH = -99.0
        self.PR_THRESH = -30.0
        self.PD_THRESH = 20.0

        self.is_complete_response = lambda x: x <= self.CR_THRESH
        self.is_partial_response = lambda x: self.CR_THRESH < x <= self.PR_THRESH
        self.is_stable_disease = lambda x: self.PR_THRESH < x < self.PD_THRESH
        self.is_progressive_disease = lambda x: x >= self.PD_THRESH

    # Transform functions
    def tv_to_tv(self, tumor_volume_data_list:np.ndarray)->np.ndarray:
        tv_to_tv:np.ndarray  = tumor_volume_data_list
        return tv_to_tv
    def tv_percent_change(self, tumor_volume_data_list:np.ndarray)->np.ndarray:
        tv_per_change:np.ndarray  = tumor_volume_data_list
        vo = tv_per_change[0]
        tv_per_change = 100.0*(tv_per_change-vo)/vo
        return tv_per_change
    def tv_proportion_volume_change(self, tumor_volume_data_list:np.ndarray)->np.ndarray:
        log2_change = tumor_volume_data_list.copy()
        vo = log2_change[0]  # baseline volume
        log2_change =  np.log2(log2_change/vo)
        return log2_change
    def tv_percent_prog_regres_endpoint(self, tumor_volume_data_list:np.ndarray)->np.ndarray:
        pct_change = tumor_volume_data_list.copy()
        vo = pct_change[0]
        pct_change = ((pct_change - vo) / vo) * 100
        return pct_change

    # Compute
    def compute_auc(self, compute_day: int | None = None)->tuple[float,float]:
        """
        Compute AUC and normalized AUC for tumor volume data.

        Parameters
        ----------
        compute_day : int or None
            If provided, compute AUC only up to this day.
            Otherwise compute full AUC.
        """

        # No data?
        if self.time_day is None or len(self.time_day) == 0:
            return math.nan, math.nan

        # Determine the day limit
        if compute_day is None:
            cutoff_day = self.time_day[-1]
        else:
            cutoff_day = compute_day

        # Determine maximum usable index
        # Find first index where time >= cutoff_day
        idx_list = [i for i, t in enumerate(self.time_day) if t >= cutoff_day]

        if len(idx_list) == 0:
            # cutoff beyond end of data → use full series
            max_index = len(self.time_day)
        else:
            # use the first index where time crosses the cutoff
            max_index = idx_list[0] + 1  # +1 so slicing includes this point

        # Slice data up to max_index
        t = np.array(self.time_day[:max_index])
        v = np.array(self.tumor_volume[:max_index])

        # Compute AUC
        auc = np.trapezoid(v, t)

        # Normalized AUC per day
        time_duration = t[-1] - t[0] if len(t) > 1 else math.nan
        normalized_auc = auc / time_duration if time_duration > 0 else math.nan

        return auc, normalized_auc
    def compute_percent_change_tumor_volume(self, compute_day: int | None = None) -> tuple[float, float]:
        """
        Compute percent change in tumor volume from baseline.

        Parameters
        ----------
        compute_day : int or None
            If provided, compute percent change up to this day.
            Otherwise compute percent change to the final timepoint.

        Returns
        -------
        tuple[float, float]
            (percent change, percent change normalized per day)
        """

        # No data?
        if self.time_day is None or len(self.time_day) == 0:
            return math.nan, math.nan

        # Determine the day limit
        if compute_day is None:
            cutoff_day = self.time_day[-1]
        else:
            cutoff_day = compute_day

        # Determine maximum usable index
        idx_list = [i for i, t in enumerate(self.time_day) if t >= cutoff_day]

        if len(idx_list) == 0:
            max_index = len(self.time_day)
        else:
            max_index = idx_list[0] + 1

        # Slice data up to max_index
        t = np.array(self.time_day[:max_index])
        v = np.array(self.tumor_volume[:max_index])

        # Check validity - need at least 2 points and positive initial volume
        if len(v) < 2 or v[0] <= 0 or np.isnan(v[0]):
            return math.nan, math.nan

        # Compute percent change: (final - initial) / initial * 100
        percent_tv_change = 100 * (v[-1] - v[0]) / v[0]

        # Normalized percent change per day
        time_duration = t[-1] - t[0]
        if time_duration <= 0:
            return math.nan, math.nan

        normalized_percent_tv_change = percent_tv_change / time_duration

        return percent_tv_change, normalized_percent_tv_change
    def compute_objective_response(self, compute_day:int|None = None) -> str:
        percent_tumor_volume_change, _ = self.compute_percent_change_tumor_volume(compute_day)
        if self.is_complete_response(percent_tumor_volume_change)==True:
            return "CR"
        elif self.is_partial_response(percent_tumor_volume_change)==True:
            return "PR"
        elif self.is_stable_disease(percent_tumor_volume_change)==True:
            return "SD"
        elif self.is_progressive_disease(percent_tumor_volume_change)==True:
            return "PD"
        else:
            # No category matched – optional fallback
            return ""

    # Summary
    def summary(self)->str:
        # Set values after check
        contributor = 'Not Set' if self.contributor is None else self.contributor
        arm = 'Not Set' if self.arm is None else self.arm
        study = 'Not Set' if self.study is None else self.study
        pdx_id = 'Not Set' if self.pdx_id is None else self.pdx_id

        class_str = f'TV Time Series: pdx_id: {pdx_id}, contributor: {contributor}, arm: {arm}, study: {study}, num points: {self.num_points}'
        return class_str

    # Visualize
    def plot(self, figsize=(8, 5), volume_label="Tumor Volume", volume_units="mm^3",
             weight_label="Weight", weight_units="mg", title=None, plot_weight=True,
             tv_transform_str="No Transform"):
        """
        Plot tumor volume and optional tumor weight over time in separate subplots.

        Parameters
        ----------
        figsize : tuple
            Size of the matplotlib figure.
        volume_label : str
            Label for the tumor volume axis.
        weight_label : str
            Label for the tumor weight axis.
        title : str or None
            Optional custom title. If None, a title is built from metadata.
        plot_weight : bool
            Whether to plot tumor weight data (if available). Default is True.
        """

        import matplotlib.pyplot as plt

        if self.time_day is None or self.tumor_volume is None:
            raise ValueError("time_day and tumor_volume must not be None")

        # Determine if we should plot weight
        has_weight = (hasattr(self, "tumor_weight") and
                      self.tumor_weight is not None and
                      plot_weight)

        # Create subplots with height ratio of 1:3 (weight:volume)
        if has_weight:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True,
                                           gridspec_kw={'height_ratios': [5, 1]})
        else:
            fig, ax1 = plt.subplots(figsize=figsize)

        # Plot weight if available and requested (on top)
        if has_weight:
            weight_label_str = f'{weight_label} ({weight_units})'
            ax2.plot(self.time_day, self.tumor_weight, marker="s", color="black")
            ax2.set_ylabel(weight_label_str)
            ax2.minorticks_on()
            ax2.grid(True, alpha=0.3)
            ax2.grid(True, which='minor', alpha=0.15, linestyle=':')
            ax2.tick_params(which='minor', labelleft=False, labelbottom=False)

        # Get data and transform if required
        data_transform_f = self.tv_transform_dict[tv_transform_str]
        tv_local_data = data_transform_f(self.tumor_volume)

        # Plot tumor volume (on bottom or alone)
        ax1.plot(self.time_day, tv_local_data, marker="o", color="tab:blue")
        ax1.set_xlabel("Time (days)")
        volumelabel_str = f"{volume_label} ({volume_units})"
        if not volume_units:
            volumelabel_str = f"{volume_label}"
        ax1.set_ylabel(volumelabel_str)
        ax1.minorticks_on()
        ax1.grid(True, alpha=0.3)
        ax1.grid(True, which='minor', alpha=0.15, linestyle=':')
        ax1.tick_params(which='major', labelleft=True, labelbottom=True)

        # Build title from metadata if not provided
        if title is None:
            parts = []
            if self.study is not None:
                parts.append(f"Study: {self.study}")
            if self.study_group is not None:
                parts.append(f"Group: {self.study_group}")
            if self.pdx_id is not None:
                parts.append(f"PDX ID: {self.pdx_id}")
            if self.arm is not None:
                parts.append(f"Arm: {self.arm}")
            if self.contributor is not None:
                parts.append(f"Contributor: {self.contributor}")

            title = " | ".join(parts) if parts else "Tumor Time Series"

        fig.suptitle(title)

        plt.tight_layout()
        plt.show()

    # Class functions
    def __str__(self):
        return self.summary()
class TumorVolumeStudyClass():
    # Data structure for storing, analysisng, and plotting study data
    def __init__(self, study_id:str, arm_col:list[str], id_col:list[str], tumor_col:list[str],
                      study_tv_time_dict:dict[str, TumorVolumeTimeSeriesClass]):

        # Create dictionary for holding data
        self.study_id:str = study_id
        self.arm_col = arm_col.copy()
        self.id_col = id_col.copy()
        self.tumor_col = tumor_col.copy()
        self.study_tv_time_dict = copy.deepcopy(study_tv_time_dict)
        self.study_arms_dict:dict[str,list]|None = None

        # Summarize values
        self.unique_arms = list(set(self.arm_col))
        self.unique_ids = list(set(self.id_col))

        # Create arms diction
        study_arms_dict = {}
        for arm in self.unique_arms:
            arm_ids = list(set([id_col[i] for i, id in enumerate(arm_col) if id == arm]))
            study_arms_dict[arm] = arm_ids
        self.study_arms_dict = study_arms_dict

        # Transforms
        self.tv_transform_options = ["No Transform", "Percent Change", "Prop. Vol. Change", "Percent Prgress/Regress"]
        self.tv_transform_dict = {"No Transform": self.tv_to_tv,
                                  "Percent Change": self.tv_percent_change,
                                  "Prop. Vol. Change": self.tv_proportion_volume_change,
                                  "Percent Prgress/Regress": self.tv_percent_prog_regres_endpoint}
        self.tv_transform_reccomended_labels = ["Tumor Volume", "Percent Change", f"% Change from $V_0$",
                                                r"$\log_2(V/V_0)$", f"% Progress/Regress from $V_0$"]
        self.tv_transform_str = "No Transform"
        self.tv_transform_f = self.tv_to_tv

        # Objective Response Definition
        # "CR":#08306B # Deep Blue, "PR":#2171B5 # Blue, "SD":#BDBDBD # Gray, "PD":#D94801 # Red-Orange
        self.objective_response_names = {"CR":"Complete Response", "PR":"Partial Response", "SD":"Stable Disease",
            "PD":"Progressive Disease"}
        self.objective_response_colors:dict[str,str] = {
            "CR": "#FECA57", # sunny yellow
            "PR": "#96CEB4", # mint green
            "SD": "#00D2D3", # cyan
            "PD": "#45B7D1"  # sky blue
        }
        self.default_response_color = "#CCCCCC"
        self.objective_response_colors[""] = self.default_response_color

    # Transform functions
    def tv_to_tv(self, tumor_volume_data_list: np.ndarray) -> np.ndarray:
        tv_to_tv: np.ndarray = tumor_volume_data_list
        return tv_to_tv
    def tv_percent_change(self, tumor_volume_data_list: np.ndarray) -> np.ndarray:
        tv_per_change: np.ndarray = tumor_volume_data_list
        vo = tv_per_change[0]
        tv_per_change = 100.0 * (tv_per_change - vo) / vo
        return tv_per_change
    def tv_proportion_volume_change(self, tumor_volume_data_list: np.ndarray) -> np.ndarray:
        log2_change = tumor_volume_data_list.copy()
        vo = log2_change[0]  # baseline volume
        log2_change = np.log2(log2_change / vo)
        return log2_change
    def tv_percent_prog_regres_endpoint(self, tumor_volume_data_list: np.ndarray) -> np.ndarray:
        pct_change = tumor_volume_data_list.copy()
        vo = pct_change[0]
        pct_change = ((pct_change - vo) / vo) * 100
        return pct_change

    # Computation
    def compute_event_time(self, time_day, volume, delta=1.0, cutoff=None):
        # Compute the event time for one mouse
        """
        Event defined as tumor volume increasing by factor (1+delta)
        or exceeding 'cutoff'. Returns (event_time, event_flag).
        """
        if len(volume) == 0:
            return None, 0

        baseline = volume[0]
        doubling_threshold = baseline * (1 + delta)

        for t, v in zip(time_day, volume):
            if v >= doubling_threshold:
                return t, 1
            if cutoff is not None and v >= cutoff:
                return t, 1

        # Censored at last time point
        return time_day[-1], 0
    def build_survival_data(self, delta=1.0, cutoff=None):
        # Build per-arm survival data
        """
        Returns: {arm: {"time": [...], "event": [...]}}
        """
        result = {}

        for arm in self.unique_arms:
            times = []
            events = []

            for mouse_id in self.study_arms_dict[arm]:
                ts = self.study_tv_time_dict.get(mouse_id)
                if ts is None:
                    continue

                t, e = self.compute_event_time(
                    ts.time_day,
                    ts.tumor_volume,
                    delta=delta,
                    cutoff=cutoff
                )

                if t is not None:
                    times.append(t)
                    events.append(e)

            result[arm] = {"time": np.array(times), "event": np.array(events)}

        return result
    def compute_numbers_at_risk(self, survival_dict, grid_points=10):
        # Compute numbers at risk for all arms at shared time grid
        """
        Returns:
            time_grid: array of time points
            risk_table: {arm: array[num at risk at each time point]}
        """
        all_times = np.concatenate([survival_dict[a]["time"] for a in survival_dict])
        t_grid = np.linspace(0, np.max(all_times), grid_points)

        risk_table = {}

        for arm in survival_dict:
            t = survival_dict[arm]["time"]
            e = survival_dict[arm]["event"]

            at_risk = []
            for tg in t_grid:
                still_at_risk = np.sum(t >= tg)
                at_risk.append(still_at_risk)

            risk_table[arm] = np.array(at_risk)

        return t_grid, risk_table
    def compute_logrank_pvalue(self, survival_dict):
        # Log-rank p-value comparing all arms
        arms = list(survival_dict.keys())

        # pairwise combine into multi-arm log-rank
        time_arrays = [survival_dict[a]["time"] for a in arms]
        event_arrays = [survival_dict[a]["event"] for a in arms]

        # lifelines supports k-sample test
        from lifelines.statistics import multivariate_logrank_test
        labels = np.concatenate([[i] * len(time_arrays[i]) for i in range(len(arms))])
        all_times = np.concatenate(time_arrays)
        all_events = np.concatenate(event_arrays)

        results = multivariate_logrank_test(
            all_times,
            labels,
            event_observed=all_events
        )

        return results.p_value

    # Summary
    def summarize(self):
        # Write summary to log file

        # Write unique lists
        logger.info('')
        logger.info(f'Study id: {self.study_id}')
        unique_arm_str = f'unique_arms: ' + ', '.join(self.unique_arms)
        logger.info(unique_arm_str)
        unique_ids_str = f'unique_ids: ' + ', '.join(self.unique_ids)
        logger.info(unique_ids_str)
        logger.info(f'Arm:')
        for arm in self.unique_arms:
            logger.info(f'     {arm}: ' + ', '.join(self.study_arms_dict[arm]))

    # Visualization
    def plot_spider(self, figsize=(10, 6),
                    volume_label="Tumor Volume", volume_units="mm^3", weight_label="Weight", weight_units="mg",
                    title=None, plot_weight=True, show_individual=True, show_aggregate=True, aggregate_sem=True,
                    error_bars=False, aggregate_marker=None, tv_transform_str="No Transform"):
        """
        Spider plot for tumor volume study data with optional aggregation curves.

        Parameters
        ----------
        show_individual : bool
            Plot each individual mouse time series (spider lines).
        show_aggregate : bool
            Plot per-arm mean curves.
        aggregate_sem : bool
            Shade SEM around the mean curves (ignored if error_bars=True).
        error_bars : bool
            Display error bars at each time point instead of shaded region.
        aggregate_marker : str or None
            Marker style for aggregate plots (e.g., 'o', 's', '^', 'D').
            If None, no markers are shown on aggregate lines.
        plot_weight : bool
            Whether to include weight subplot.
        tv_transform_str : str
            Transform to apply to tumor volume data. Options: "No Transform",
            "Percent Change", "Prop. Vol. Change", "Percent Prgress/Regress"
        """

        # Validate data
        if not self.study_tv_time_dict:
            raise ValueError("No time-series data available.")

        # Get transform function
        if tv_transform_str not in self.tv_transform_dict:
            raise ValueError(f"Invalid transform: {tv_transform_str}. Options: {self.tv_transform_options}")
        tv_transform_f = self.tv_transform_dict[tv_transform_str]

        # Determine if any time-series contains weight
        has_weight_data = any(
            hasattr(ts, "tumor_weight") and ts.tumor_weight is not None
            for ts in self.study_tv_time_dict.values()
        )
        has_weight = plot_weight and has_weight_data

        # Color per arm
        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        arm_colors = {arm: color_cycle[i % len(color_cycle)]
                      for i, arm in enumerate(self.unique_arms)}

        # Create figure
        if has_weight:
            fig, (ax_vol, ax_w) = plt.subplots(
                2, 1, figsize=figsize, sharex=True,
                gridspec_kw={'height_ratios': [4, 1]}
            )
        else:
            fig, ax_vol = plt.subplots(figsize=figsize)
            ax_w = None

        # Storage for aggregation - now using dictionaries keyed by time point
        arm_time_vol = {arm: {} for arm in self.unique_arms}
        arm_time_wgt = {arm: {} for arm in self.unique_arms}

        # ================================
        # 1. PLOT INDIVIDUAL TIME SERIES
        # ================================
        for arm in self.unique_arms:
            color = arm_colors[arm]

            for mouse_id in self.study_arms_dict[arm]:

                ts = self.study_tv_time_dict.get(mouse_id)
                if ts is None or ts.time_day is None or ts.tumor_volume is None:
                    continue

                # Apply transform to tumor volume data
                transformed_volume = tv_transform_f(ts.tumor_volume)

                # Store for aggregation by time point
                for t, v in zip(ts.time_day, transformed_volume):
                    if t not in arm_time_vol[arm]:
                        arm_time_vol[arm][t] = []
                    arm_time_vol[arm][t].append(v)

                # Spider (volume)
                if show_individual:
                    ax_vol.plot(ts.time_day,
                                transformed_volume,
                                marker="o",
                                alpha=0.7,
                                linewidth=1.0,
                                color=color)

                # Weight
                if has_weight and hasattr(ts, "tumor_weight") and ts.tumor_weight is not None:
                    for t, w in zip(ts.time_day, ts.tumor_weight):
                        if t not in arm_time_wgt[arm]:
                            arm_time_wgt[arm][t] = []
                        arm_time_wgt[arm][t].append(w)

                    if show_individual:
                        ax_w.plot(ts.time_day,
                                  ts.tumor_weight,
                                  marker="s",
                                  alpha=0.7,
                                  linewidth=1.0,
                                  color=color)

        # ================================
        # 2. MEAN / AGGREGATE CURVES
        # ================================
        if show_aggregate:
            for arm in self.unique_arms:
                color = arm_colors[arm]

                if len(arm_time_vol[arm]) == 0:
                    continue

                # Sort time points and compute statistics
                time_points = sorted(arm_time_vol[arm].keys())
                mean_vol = []
                sem_vol = []

                for t in time_points:
                    values = np.array(arm_time_vol[arm][t])
                    mean_vol.append(np.mean(values))
                    if aggregate_sem:
                        sem_vol.append(sem(values))

                mean_vol = np.array(mean_vol)
                sem_vol = np.array(sem_vol) if aggregate_sem else None

                # Plot mean tumor volume curve
                if error_bars and aggregate_sem:
                    # Error bars style (always with markers)
                    ax_vol.errorbar(time_points, mean_vol,
                                    yerr=sem_vol,
                                    marker='o' if aggregate_marker is None else aggregate_marker,
                                    markersize=6,
                                    linewidth=2.8,
                                    capsize=4,
                                    capthick=2,
                                    color=color)
                else:
                    # Line style (with optional markers)
                    ax_vol.plot(time_points, mean_vol,
                                marker=aggregate_marker,
                                markersize=6 if aggregate_marker else None,
                                linewidth=2.8,
                                color=color)

                    # SEM shading
                    if aggregate_sem and sem_vol is not None:
                        ax_vol.fill_between(time_points,
                                            mean_vol - sem_vol,
                                            mean_vol + sem_vol,
                                            color=color,
                                            alpha=0.25)

                # Weight aggregation
                if has_weight and len(arm_time_wgt[arm]) > 0:
                    time_points_w = sorted(arm_time_wgt[arm].keys())
                    mean_w = []
                    sem_w = []

                    for t in time_points_w:
                        values = np.array(arm_time_wgt[arm][t])
                        mean_w.append(np.mean(values))
                        if aggregate_sem:
                            sem_w.append(sem(values))

                    mean_w = np.array(mean_w)
                    sem_w = np.array(sem_w) if aggregate_sem else None

                    if error_bars and aggregate_sem:
                        # Error bars style (always with markers)
                        ax_w.errorbar(time_points_w, mean_w,
                                      yerr=sem_w,
                                      marker='s' if aggregate_marker is None else aggregate_marker,
                                      markersize=6,
                                      linewidth=2.8,
                                      capsize=4,
                                      capthick=2,
                                      color=color)
                    else:
                        # Line style (with optional markers)
                        ax_w.plot(time_points_w, mean_w,
                                  marker=aggregate_marker,
                                  markersize=6 if aggregate_marker else None,
                                  linewidth=2.8,
                                  color=color)

                        if aggregate_sem and sem_w is not None:
                            ax_w.fill_between(time_points_w,
                                              mean_w - sem_w,
                                              mean_w + sem_w,
                                              color=color,
                                              alpha=0.25)

        # ================================
        # 3. AXIS FORMATTING
        # ================================
        # Adjust label based on transform
        volume_label_str = f"{volume_label} ({volume_units})"
        if not volume_units:
            volume_label_str = f"{volume_label}"

        ax_vol.set_ylabel(volume_label_str)
        ax_vol.set_xlabel("Time (days)")
        ax_vol.minorticks_on()
        ax_vol.grid(True, alpha=0.3)
        ax_vol.grid(True, which='minor', linestyle=':', alpha=0.15)

        # Add horizontal line at 0 for transformed data
        if tv_transform_str != "No Transform":
            ax_vol.axhline(y=0, color='k', linestyle='--', alpha=0.3, linewidth=1)

        # Legend for arms
        legend_handles = []
        legend_labels = []
        for arm, color in arm_colors.items():
            h, = ax_vol.plot([], [], color=color, linewidth=3, label=arm)
            legend_handles.append(h)
            legend_labels.append(arm)
        ax_vol.legend(legend_handles, legend_labels, title="Arms")

        # Weight subplot formatting
        if has_weight:
            weight_label_str = f"{weight_label} ({weight_units})"
            ax_w.set_ylabel(weight_label_str)
            ax_w.minorticks_on()
            ax_w.grid(True, alpha=0.3)
            ax_w.grid(True, which='minor', linestyle=':', alpha=0.15)

        # ================================
        # 4. TITLE
        # ================================
        if title is None:
            title = f"Tumor Volume Study: {self.study_id}"
            if tv_transform_str != "No Transform":
                title += f" ({tv_transform_str})"

        fig.suptitle(title)
        plt.tight_layout()
        plt.show()
    def plot_event_free_survival(self, delta=1.0, cutoff=None, figsize=(10, 8),
                                 title="Event-Free Survival (Tumor Volume Doubling)",
                                 show_number_at_risk_plot=True, show_at_risk_table=False):
        """
        Three-panel figure:
        - Top: Kaplan–Meier event-free survival curves + p-value
        - Middle: Arm labels only (aligned with the numbers-at-risk table)
        - Bottom: Numbers at risk table
        """

        # -----------------------------------------------------
        # Compute survival data
        # -----------------------------------------------------
        survival = self.build_survival_data(delta=delta, cutoff=cutoff)
        t_grid, risk_table = self.compute_numbers_at_risk(survival)
        p_val = self.compute_logrank_pvalue(survival)

        # -----------------------------------------------------
        # Figure with THREE rows
        # -----------------------------------------------------
        fig = plt.figure(figsize=figsize)

        # Setup subplot proportions
        show_kaplan_meier_curve = True  # axis linked to km has to be true
        km_subplot_proportion = 4.0 if show_kaplan_meier_curve == True else 0
        num_at_risk_plot_proportion = 1.0 if show_number_at_risk_plot == True else 0
        at_risk_table_proportion = 0.6 if show_at_risk_table == True else 0

        # Determine number of subplots
        num_of_subplots = int(show_kaplan_meier_curve)+int(show_number_at_risk_plot)+int(show_at_risk_table)

        # Set up height proportions
        height_ratios = []
        if show_kaplan_meier_curve:
            height_ratios.append(km_subplot_proportion)
        if show_number_at_risk_plot:
            height_ratios.append(num_at_risk_plot_proportion)
        if show_at_risk_table:
            height_ratios.append(at_risk_table_proportion)
        gs = fig.add_gridspec(num_of_subplots, 1,
                              height_ratios=height_ratios, hspace=0.15)

        current_sub_plot = 0
        if show_kaplan_meier_curve == True:
            ax_km = fig.add_subplot(gs[current_sub_plot])
            current_sub_plot += 1
        if show_number_at_risk_plot == True:
            ax_labels = fig.add_subplot(gs[current_sub_plot], sharex=ax_km)
            current_sub_plot += 1
        if show_at_risk_table == True:
            ax_risk = fig.add_subplot(gs[current_sub_plot], sharex=ax_km)

        # -----------------------------------------------------
        # KM curves
        # -----------------------------------------------------

        km = KaplanMeierFitter()
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        arm_colors = {arm: colors[i % len(colors)] for i, arm in enumerate(self.unique_arms)}

        for arm in self.unique_arms:
            km.fit(survival[arm]["time"], survival[arm]["event"], label=arm)
            km.plot_survival_function(ax=ax_km, ci_show=False, color=arm_colors[arm], linewidth=2)

        ax_km.set_ylabel("Event-Free Probability")
        ax_km.set_title(f"{title}\nP-value = {p_val:.4g}")
        ax_km.grid(True, alpha=0.3)

        # Hide top and right spines
        for spine in ["right", "left"]:
            ax_km.spines[spine].set_visible(False)

        # # force whole-number x-ticks
        max_t = int(t_grid[-1])
        # step = 5 if max_t > 5 else 1
        # ax_km.set_xticks(np.arange(0, max_t + 1, step))
        # ax_km.set_xlim(-0.5, max_t + 0.5)
        # ax_km.get_xmajorticklabels()

        # Set major tick labels using the built-in function
        #ax_km.set_xticklabels([f"{int(x)}" for x in ax_km.get_xticks()])
        # ax_km.tick_params(axis='x', which='major', labelsize=10)

        #-----------------------------------------------------
        # Middle panel: AT-RISK LINE PLOTS
        # -----------------------------------------------------
        if show_number_at_risk_plot  == True:
            ax_labels.set_ylabel("Number at Risk")
            ax_labels.set_ylim(0-0.76, max(max(risk_table[arm]) for arm in self.unique_arms) * 1.1+0.5)

            # Plot line for each arm showing numbers at risk over time
            for arm in self.unique_arms:
                ax_labels.plot(t_grid, risk_table[arm],
                               color=arm_colors[arm],
                               linewidth=2,
                               marker='none',
                               markersize=4,
                               label=arm)

            ax_labels.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
            ax_labels.grid(True, alpha=0.3, axis='y')
            ax_labels.legend(loc='best', framealpha=0.9)

            # Hide top and right spines
            for spine in ["right", "left"]:
                ax_labels.spines[spine].set_visible(False)

            # Match x-axis limits with KM plot
            ax_labels.set_xlim(-0.5, max_t + 0.5)



        # -----------------------------------------------------
        # Bottom panel: NUMBERS AT RISK
        # -----------------------------------------------------
        if show_at_risk_table == True:
            ax_risk.set_yticks(range(len(self.unique_arms)))
            ax_risk.set_yticklabels(self.unique_arms)
            ax_risk.set_xlabel("Time (days)")
            ax_risk.set_xlim(-0.5, max_t + 0.5)
            ax_risk.set_ylim(-0.6, len(self.unique_arms))

            # Clear spines except left
            for spine in ["right", "left"]:
                ax_risk.spines[spine].set_visible(False)

            # Plot the numbers at risk
            for i, arm in enumerate(self.unique_arms):
                # invisible line to preserve alignment
                ax_risk.plot(t_grid, [i] * len(t_grid), alpha=0)

                for x, y_val in zip(t_grid, risk_table[arm]):
                    ax_risk.text(x, i, f"{y_val}", ha="center", va="center", fontsize=10)

            ax_risk.grid(False)

        plt.show()
    def plot_auc_bar(self, compute_day: int | None = None, figsize=(12, 6), sort_descending=True,
                     control_arms=("control", "vehicle", "placebo"), bar_alpha=0.85,
                     bar_edgecolor="black", show_bar_labels=False, title="AUC by Arm", color_cycle=None,
                     show_axis_labels:bool=True, plot_normalized_auc=False, show_legend:bool=True):
        """
        Vertical bar plot of AUC values for each time-series.
        Controls are plotted first, followed by experimental arms.

        Parameters
        ----------
        compute_day : int or None
            Compute AUC up to max_day if provided.
        sort_descending : bool
            Sort AUC values within each arm.
        show_bar_labels : bool
            If True, display numeric AUC above each bar.
        control_arms : tuple
            Arms considered control and plotted first.
        """

        # -------------------------------------------
        # 1. COLLECT AUC PER ARM
        # -------------------------------------------
        unique_arms = list(set(self.arm_col))
        auc_dict = {}

        for arm in unique_arms:
            ts_ids = self.study_arms_dict[arm]
            arm_auc = []

            for ts_id in ts_ids:
                ts = self.study_tv_time_dict[ts_id]
                auc_val, normalized_auc = ts.compute_auc(compute_day=compute_day)
                if plot_normalized_auc:
                    arm_auc.append((ts_id, normalized_auc))
                else:
                    arm_auc.append((ts_id, auc_val))

            arm_auc.sort(key=lambda x: x[1], reverse=sort_descending)
            auc_dict[arm] = arm_auc

        # -------------------------------------------
        # 2. ARM ORDERING
        # -------------------------------------------
        controls = [a for a in unique_arms if a.lower() in control_arms]
        experimental = [a for a in unique_arms if a not in controls]
        ordered_arms = controls + experimental

        # -------------------------------------------
        # 3. COLOR MAP FOR ARMS
        # -------------------------------------------
        if color_cycle is None:
            color_cycle = list(plt.cm.tab10.colors)

        arm_colors = {
            arm: color_cycle[i % len(color_cycle)]
            for i, arm in enumerate(ordered_arms)
        }

        # -------------------------------------------
        # 4. FLATTEN BAR DATA
        # -------------------------------------------
        bar_x_positions = []
        bar_heights = []
        bar_colors = []
        bar_labels = []  # mouse IDs only (no arm)

        idx = 0
        for arm in ordered_arms:
            color = arm_colors[arm]
            for ts_id, auc_val in auc_dict[arm]:
                bar_x_positions.append(idx)
                bar_heights.append(auc_val)
                bar_colors.append(color)
                bar_labels.append(str(ts_id))  # no arm name

                idx += 1

        # -------------------------------------------
        # 5. PLOT
        # -------------------------------------------
        fig, ax = plt.subplots(figsize=figsize)

        ax.bar(
            bar_x_positions,
            bar_heights,
            color=bar_colors,
            alpha=bar_alpha,
            edgecolor=bar_edgecolor
        )

        # Tick labels (mouse IDs only)
        if show_axis_labels:
            ax.set_xticks(bar_x_positions)
            ax.set_xticklabels(bar_labels, rotation=75, ha='right', fontsize=8)
        else:
            ax.set_xticks([])
            ax.set_xticklabels([])

        # Add labels and titles
        y_label = "AUC" if not plot_normalized_auc else "Normalized AUC"
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.grid(True, axis='y', alpha=0.3)

        # -------------------------------------------
        # 6. OPTIONAL: Annotate Bars with AUC Values
        # -------------------------------------------
        if show_bar_labels:
            for x, h in zip(bar_x_positions, bar_heights):
                ax.text(x, h, f"{h:.1f}", ha='center', va='bottom', fontsize=8)

        # -------------------------------------------
        # 7. LEGEND FOR ARMS
        # -------------------------------------------
        if show_legend:
            handles = [plt.Line2D([], [], color=arm_colors[a], lw=8)
                       for a in ordered_arms]
            ax.legend(handles, ordered_arms, title="Arms", loc="best")

        plt.tight_layout()
        plt.show()
    def plot_percent_tumor_vol_change_bar(self, compute_day: int | None = None, figsize=(12, 6), sort_descending=True,
                     control_arms=("control", "vehicle", "placebo"), bar_alpha=0.85,
                     bar_edgecolor="black", show_bar_labels=False, title="Tumor Volume change (%)", color_cycle=None,
                     show_axis_labels:bool=True, plot_normalized_tv_change=False, show_legend:bool=True):
        """
        Vertical bar plot of AUC values for each time-series.
        Controls are plotted first, followed by experimental arms.

        Parameters
        ----------
        compute_day : int or None
            Compute AUC up to max_day if provided.
        sort_descending : bool
            Sort AUC values within each arm.
        show_bar_labels : bool
            If True, display numeric AUC above each bar.
        control_arms : tuple
            Arms considered control and plotted first.
        """

        # -------------------------------------------
        # 1. COLLECT AUC PER ARM
        # -------------------------------------------
        unique_arms = list(set(self.arm_col))
        vol_change_dict = {}

        for arm in unique_arms:
            ts_ids = self.study_arms_dict[arm]
            vol_change_list = []

            for ts_id in ts_ids:
                ts = self.study_tv_time_dict[ts_id]
                tv_change_val, normalized_tv_change_val = ts.compute_percent_change_tumor_volume(compute_day=compute_day)
                if plot_normalized_tv_change == True:
                    vol_change_list.append((ts_id, normalized_tv_change_val))
                else:
                    vol_change_list.append((ts_id, tv_change_val))

            vol_change_list.sort(key=lambda x: x[1], reverse=sort_descending)
            vol_change_dict[arm] = vol_change_list

        # -------------------------------------------
        # 2. ARM ORDERING
        # -------------------------------------------
        controls = [a for a in unique_arms if a.lower() in control_arms]
        experimental = [a for a in unique_arms if a not in controls]
        ordered_arms = controls + experimental

        # -------------------------------------------
        # 3. COLOR MAP FOR ARMS
        # -------------------------------------------
        if color_cycle is None:
            color_cycle = list(plt.cm.tab10.colors)

        arm_colors = {
            arm: color_cycle[i % len(color_cycle)]
            for i, arm in enumerate(ordered_arms)
        }

        # -------------------------------------------
        # 4. FLATTEN BAR DATA
        # -------------------------------------------
        bar_x_positions = []
        bar_heights = []
        bar_colors = []
        bar_labels = []  # mouse IDs only (no arm)

        idx = 0
        for arm in ordered_arms:
            color = arm_colors[arm]
            for ts_id, tv_change_val in vol_change_dict[arm]:
                bar_x_positions.append(idx)
                bar_heights.append(tv_change_val)
                bar_colors.append(color)
                bar_labels.append(str(ts_id))  # no arm name

                idx += 1

        # -------------------------------------------
        # 5. PLOT
        # -------------------------------------------
        fig, ax = plt.subplots(figsize=figsize)

        ax.bar(
            bar_x_positions,
            bar_heights,
            color=bar_colors,
            alpha=bar_alpha,
            edgecolor=bar_edgecolor
        )

        # Tick labels (mouse IDs only)
        if show_axis_labels:
            ax.set_xticks(bar_x_positions)
            ax.set_xticklabels(bar_labels, rotation=75, ha='right', fontsize=8)
        else:
            ax.set_xticks([])
            ax.set_xticklabels([])

        # Add labels and titles
        y_label = "Tumor Volume Change (%)" if not plot_normalized_tv_change else "Normalized Volume Change (%)"
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.grid(True, axis='y', alpha=0.3)

        # -------------------------------------------
        # 6. OPTIONAL: Annotate Bars with AUC Values
        # -------------------------------------------
        if show_bar_labels:
            for x, h in zip(bar_x_positions, bar_heights):
                ax.text(x, h, f"{h:.1f}", ha='center', va='bottom', fontsize=8)

        # -------------------------------------------
        # 7. LEGEND FOR ARMS
        # -------------------------------------------
        if show_legend:
            handles = [plt.Line2D([], [], color=arm_colors[a], lw=8)
                       for a in ordered_arms]
            ax.legend(handles, ordered_arms, title="Arms", loc="best")

        plt.tight_layout()
        plt.show()
    def plot_vol_change_as_objective_response_bar(self, compute_day: int | None = None, figsize=(12, 6),
                    sort_descending=True, control_arms=("control", "vehicle", "placebo"), bar_alpha=0.85,
                    bar_edgecolor="black", show_bar_labels=False, title="Tumor Volume change (%)", color_cycle=None,
                    show_axis_labels: bool = True, show_legend: bool = True, y_range:list|None = None):

        # -------------------------------------------------------
        # 1. Collect volume changes per arm
        # -------------------------------------------------------
        unique_arms = list(set(self.arm_col))
        vol_change_dict = {}
        response_code_dict = {}

        for arm in unique_arms:
            ts_ids = self.study_arms_dict[arm]
            vol_change_list = []
            resp_code_list = []

            for ts_id in ts_ids:
                ts = self.study_tv_time_dict[ts_id]
                tv_change_val, _ = ts.compute_percent_change_tumor_volume(compute_day=compute_day)
                value = tv_change_val

                # ---- GET OBJECTIVE RESPONSE CATEGORY --------------------
                # INSERT YOUR LOGIC HERE:
                response_code = ts.compute_objective_response(compute_day)
                # response_code must be one of: "CR","PR","SD","PD"
                # ---------------------------------------------------------

                vol_change_list.append((ts_id, value))
                resp_code_list.append((ts_id, response_code))

            # sort both lists by the TV change value
            vol_change_list.sort(key=lambda x: x[1], reverse=sort_descending)
            # match ordering for response code
            sorted_resp_list = [(ts_id, next(r for t, r in resp_code_list if t == ts_id))
                                for ts_id, _ in vol_change_list]

            vol_change_dict[arm] = vol_change_list
            response_code_dict[arm] = sorted_resp_list

        # -------------------------------------------------------
        # 2. Arm ordering (controls first)
        # -------------------------------------------------------
        controls = [a for a in unique_arms if a.lower() in control_arms]
        experimental = [a for a in unique_arms if a not in controls]
        ordered_arms = controls + experimental

        # -------------------------------------------------------
        # 3. Flatten
        # -------------------------------------------------------
        bar_x_positions = []
        bar_heights = []
        bar_colors = []
        bar_labels = []
        arm_ranges = {}  # for the top subplot: arm name spans

        idx = 0
        for arm in ordered_arms:
            start_idx = idx

            # Add space before each arms
            if idx > 0:
                idx += 1  # 1 empty bar
            start_idx = idx

            for (ts_id, tv_val), (_, resp_code) in zip(
                    vol_change_dict[arm], response_code_dict[arm]):
                bar_x_positions.append(idx)
                bar_heights.append(tv_val)
                bar_colors.append(self.objective_response_colors[resp_code])
                bar_labels.append(str(ts_id))

                idx += 1

            arm_ranges[arm] = (start_idx, idx - 1)

        # -------------------------------------------------------
        # 4. Create figure with 2 subplots (top labels + bars)
        # -------------------------------------------------------
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()

        # -------------------------------------------------------
        # 6. BAR PLOT
        # -------------------------------------------------------
        ax.bar(
            bar_x_positions,
            bar_heights,
            color=bar_colors,
            alpha=bar_alpha,
            edgecolor=bar_edgecolor
        )

        if show_axis_labels:
            ax.set_xticks(bar_x_positions)
            ax.set_xticklabels(bar_labels, rotation=75, ha='right', fontsize=8)
        else:
            ax.set_xticks([])

        y_label = "Tumor Volume Change (%)"
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.grid(True, axis='y', alpha=0.3)

        # -------------------------------------------------------
        # 7. Optional bar labels
        # -------------------------------------------------------
        if show_bar_labels:
            for x, h in zip(bar_x_positions, bar_heights):
                ax.text(x, h, f"{h:.1f}", ha='center', va='bottom', fontsize=8)

        # -------------------------------------------------------
        # 8. Legend for objective responses
        # -------------------------------------------------------
        if show_legend:
            handles = [
                plt.Line2D([], [], color=self.objective_response_colors[key], lw=8)
                for key in ["CR", "PR", "SD", "PD"]
            ]
            labels = [self.objective_response_names[k] for k in ["CR", "PR", "SD", "PD"]]

            ax.legend(handles, labels, title="Objective Response", loc="best")



        # set y limit
        # Set range if given
        if y_range is not None:
            ax.set_ylim(y_range[0], y_range[1])
        else:
            y_range = ax.get_ylim()

        # 9. Draw arm labels centered above each arm block
        # -------------------------------------------------------
        for arm, (start, end) in arm_ranges.items():
            mid = (start + end) / 2
            ax.text(
                mid,
                y_range[1] * 1.02,  # slightly above plot
                arm,
                ha='center',
                va='bottom',
                fontsize=10,
                fontweight='normal'
            )



        ax.set_ylim(y_range[0], y_range[1] * 1.10)

        # Set layout and show
        plt.tight_layout()
        plt.show()
    def add_objective_response_legend(self, ax):
        """Add a legend explaining CR/PR/SD/PD colors."""
        import matplotlib.patches as mpatches

        patches = []
        for code, full_name in self.objective_response_names.items():
            color = self.objective_response_colors.get(code, "gray")
            patches.append(mpatches.Patch(color=color, label=f"{code}: {full_name}"))

        ax.legend(handles=patches, title="Objective Response", loc="best")

    # Class functions
    def __str__(self):
        return f'Tumor Volume Study Class, study = {self.study_id}, num of arms = {len(self.unique_arms)}, arms: {", ".join(self.unique_arms)}'
class TumorVolumeExperimentClass():
    # Class supports the organiziation, presentation, and analysis of tumor volume experimental groups
    def __init__(self, experiment:str, experiment_col:list, study_col:list, study_dict:dict[str, TumorVolumeStudyClass]):

        # Sasve experiment name
        self.experiment = experiment

        # Copy column and dictionary information
        self.experiment_col = experiment_col.copy()
        self.study_col = study_col.copy()
        self.experiment_study_dict = {}

        # Create Experimental Group Dictionary
        study_keys = [s for i, s in enumerate(self.study_col) if experiment_col[i] == self.experiment ]
        study_keys = list(set(study_keys))
        self.study_keys = study_keys

        # Create reduced study dict
        for study in study_keys:
            self.experiment_study_dict[study] = study_dict[study]


        # Plots
        self.objective_response_names = {"CR": "Complete Response", "PR": "Partial Response",
                                         "SD": "Stable Disease", "PD": "Progressive Disease"}
        self.objective_response_colors = {
            "CR": "#FECA57", # sunny yellow
            "PR": "#96CEB4", # mint green
            "SD": "#00D2D3", # cyan
            "PD": "#45B7D1"  # sky blue
        }

    # Summary
    def summarize(self):
        # Write summary to log file
        # Header
        logger.info("")
        logger.info(f"-------------------")

        # Experntal Group Header
        logger.info(f"Experiment: {self.experiment}")

        # Write summary for each study
        study_keys = list(self.experiment_study_dict.keys())
        study_keys.sort()
        for study in study_keys:
            self.experiment_study_dict[study].summarize()

    # Visualization
    def plot_average_tumor_volume_change_bar(self, control_arms=("control", "vehicle", "placebo"),
            error_metric="std", show_legend=True, show_axis_labels=False, compute_day:int|None=None,
            title="Average % Tumor Volume Change by Study", figsize=(10, 6)):
        """
        Plot the average percent tumor volume change for each study.
        """

        import numpy as np
        import matplotlib.pyplot as plt

        # Sort studies
        study_keys = sorted(self.study_keys)

        study_means = []
        study_errors = []
        study_labels = []
        study_colors = []

        cmap = plt.get_cmap("tab20")

        # Build bar data
        for idx, study in enumerate(study_keys):

            study_obj = self.experiment_study_dict[study]

            arms = study_obj.unique_arms
            arms_to_plot = [arm for arm in arms if arm.lower() not in control_arms]

            all_changes = []

            for arm in arms_to_plot:
                arm_id_list = study_obj.study_arms_dict[arm]

                for ts_id in arm_id_list:
                    tv_data_obj = study_obj.study_tv_time_dict[ts_id]
                    tv_pct_change = tv_data_obj.compute_percent_change_tumor_volume(compute_day)
                    final_change = tv_pct_change
                    all_changes.append(final_change)

            if len(all_changes) == 0:
                continue

            mean_val = np.nanmean(all_changes)
            if error_metric == "sem":
                err_val = np.nanstd(all_changes) / np.sqrt(len(all_changes))
            else:
                err_val = np.nanstd(all_changes)

            study_means.append(mean_val)
            study_errors.append(err_val)
            study_labels.append(study)
            study_colors.append(cmap(idx % 20))

        # ---------------- Plotting ----------------
        fig, ax = plt.subplots(figsize=figsize)
        x = np.arange(len(study_means))

        bars = ax.bar(
            x,
            study_means,
            yerr=study_errors,
            color=study_colors,
            capsize=5,
            width=0.6,
            edgecolor="black",
        )

        ax.axhline(0, color="black", linewidth=1)

        # Axis labels
        if show_axis_labels:
            ax.set_ylabel("% Tumor Volume Change")
            ax.set_xlabel("Study")

        if title:
            ax.set_title(title)

        # Ticks
        ax.set_xticks(x)
        ax.set_xticklabels(study_labels, rotation=45, ha="right")

        # -------- Legend that describes the colors --------
        if show_legend:
            legend_elements = [
                plt.Line2D(
                    [0], [0],
                    marker="s",
                    markersize=10,
                    color=color,
                    linestyle="none",
                    label=label
                )
                for label, color in zip(study_labels, study_colors)
            ]

            ax.legend(
                handles=legend_elements,
                loc="upper right",
                frameon=True,
                facecolor="white",
                framealpha=0.8,
                title="Studies"
            )

        plt.tight_layout()
        plt.show()
    def proportion_in_objective_response_classification_bar(self, control_arms=("control", "vehicle", "placebo"),
            show_legend=True, show_axis_labels=False, compute_day: int | None = None,
            title="Objective Response Distribution by Study", figsize=(10, 6)):
        """
        Create a stacked 100% bar plot showing objective response proportions
        for each study, with count and percentage inside each bar segment.
        """

        import numpy as np
        import matplotlib.pyplot as plt

        OR_ORDER = ["CR", "PR", "SD", "PD"]
        OR_COLORS = [self.objective_response_colors[o] for o in OR_ORDER]

        study_keys = sorted(self.study_keys)

        # Holds raw counts per OR code per study
        study_or_counts = []

        # ---------------- Collect Objective Responses ----------------
        for study in study_keys:
            study_obj = self.experiment_study_dict[study]

            arms_to_plot = [
                arm for arm in study_obj.unique_arms
                if arm.lower() not in control_arms
            ]

            resp_counts = {or_code: 0 for or_code in OR_ORDER}

            for arm in arms_to_plot:
                for ts_id in study_obj.study_arms_dict[arm]:
                    tv_obj = study_obj.study_tv_time_dict[ts_id]
                    resp = tv_obj.compute_objective_response(compute_day)

                    if resp in resp_counts:
                        resp_counts[resp] += 1

            study_or_counts.append(resp_counts)

        # Convert counts → proportions
        study_or_props = []
        for count_dict in study_or_counts:
            total = sum(count_dict.values())
            if total == 0:
                study_or_props.append([0, 0, 0, 0])
            else:
                study_or_props.append([count_dict[o] / total for o in OR_ORDER])

        study_or_props = np.array(study_or_props)
        x = np.arange(len(study_keys))

        # ---------------- Plotting ----------------
        fig, ax = plt.subplots(figsize=figsize)

        bottoms = np.zeros(len(study_keys))

        # Add stacked layers CR, PR, SD, PD
        for idx, or_code in enumerate(OR_ORDER):

            heights = study_or_props[:, idx]
            counts = np.array([d[or_code] for d in study_or_counts])

            bars = ax.bar(
                x,
                heights,
                bottom=bottoms,
                color=OR_COLORS[idx],
                edgecolor="black",
                label=self.objective_response_names[or_code],
            )

            # -------- Add Count + Percentage in Each Segment --------
            for i, bar in enumerate(bars):
                count = counts[i]
                height = bar.get_height()
                total = sum(study_or_counts[i].values())

                if count > 0 and height > 0 and total > 0:
                    pct = height * 100
                    label_text = f"{count} ({pct:.0f}%)"

                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bottoms[i] + height / 2,
                        label_text,
                        ha="center",
                        va="center",
                        fontsize=10,
                        color="white" if idx in (0, 1, 3) else "black",
                        fontweight="bold"
                    )

            bottoms += heights

        # Labels
        if show_axis_labels:
            ax.set_ylabel("Proportion of Responses")
            ax.set_xlabel("Study")

        ax.set_xticks(x)
        ax.set_xticklabels(study_keys, rotation=45, ha="right")

        if title:
            ax.set_title(title)

        # ---------------- Legend Outside Plot ----------------
        if show_legend:
            ax.legend(
                title="Objective Responses",
                loc="center left",
                bbox_to_anchor=(1.02, 0.5),
                frameon=True
            )

        plt.tight_layout()
        plt.show()

        # Class functions
    def plot_auc_with_controls_bar(self, control_arms=("control", "vehicle", "placebo"),
            error_metric="std", show_legend=True, show_axis_labels=False, compute_day:int|None=None,
            title="Mean AUC", figsize=(10, 6)):
        """
        plot AUC with control bars for each study with control arms
        """

        import numpy as np
        import matplotlib.pyplot as plt

        # Sort studies
        study_keys = sorted(self.study_keys)

        study_means = []
        study_errors = []
        study_labels = []
        study_colors = []

        cmap = plt.get_cmap("tab20")

        # Build bar data
        for idx, study in enumerate(study_keys):

            study_obj = self.experiment_study_dict[study]

            arms = study_obj.unique_arms
            arms_to_plot = [arm for arm in arms if arm.lower() not in control_arms]

            all_changes = []

            for arm in arms_to_plot:
                arm_id_list = study_obj.study_arms_dict[arm]

                for ts_id in arm_id_list:
                    tv_data_obj = study_obj.study_tv_time_dict[ts_id]
                    tv_auc = tv_data_obj.compute_auc(compute_day)
                    all_changes.append(tv_auc)

                print(f'arm = {arm}, arm_auc = {all_changes}')

            if len(all_changes) == 0:
                continue

            mean_val = np.nanmean(all_changes)
            if error_metric == "sem":
                err_val = np.nanstd(all_changes) / np.sqrt(len(all_changes))
            else:
                err_val = np.nanstd(all_changes)

            study_means.append(mean_val)
            study_errors.append(err_val)
            study_labels.append(study)
            study_colors.append(cmap(idx % 20))

        # ---------------- Plotting ----------------
        fig, ax = plt.subplots(figsize=figsize)
        x = np.arange(len(study_means))

        bars = ax.bar(
            x,
            study_means,
            yerr=study_errors,
            color=study_colors,
            capsize=5,
            width=0.6,
            edgecolor="black",
        )

        ax.axhline(0, color="black", linewidth=1)

        # Axis labels
        if show_axis_labels:
            ax.set_ylabel("% Tumor Volume Change")
            ax.set_xlabel("Study")

        if title:
            ax.set_title(title)

        # Ticks
        ax.set_xticks(x)
        ax.set_xticklabels(study_labels, rotation=45, ha="right")

        # -------- Legend that describes the colors --------
        if show_legend:
            legend_elements = [
                plt.Line2D(
                    [0], [0],
                    marker="s",
                    markersize=10,
                    color=color,
                    linestyle="none",
                    label=label
                )
                for label, color in zip(study_labels, study_colors)
            ]

            ax.legend(
                handles=legend_elements,
                loc="upper right",
                frameon=True,
                facecolor="white",
                framealpha=0.8,
                title="Studies"
            )

        plt.tight_layout()
        plt.show()

    # Python
    def __str__(self):
        return f'Tumor Volume Experiment Class, experiment: {self.experiment}, num of studies = {len(self.study_keys)}, studies = {", ".join(self.study_keys)}'
class TumorVolumeDataClass():
    # Load, analyze, sumarrize, and plot tumor volume data
    def __init__(self):
        # Set up logger
        self.logger = logging.getLogger(__name__)

        # tumor volume
        self.tumor_volume_data_fn:str|None = None
        self.volume_units:str|None = None
        self.weight_units:str|None = None

        # data formats
        self.tmz_col_names:list|None  = ['contributor', 'arms', 'times', 'volume', 'experiment',
                                         'study', 'id', 'tumor', 'disease_type',
                                         'body_weight', 'matched_controls']
        self.unmatched_control_entry = 'unmatched'

        # data information
        self.tmz_data_fn:str|None = None
        self.tmz_data_df:pd|None = None

        # Data Summary
        self.num_of_data_points:int|None
        self.num_of_time_series:int|None

        # Study Summary
        self.unique_contributors:list|None
        self.num_of_contributors:int|None
        self.unique_arms:list|None
        self.num_of_arms:int|None
        self.unique_studies:list|None
        self.num_of_studies:int|None
        self.unique_pdx_ids:list|None
        self.num_unique_pdx_ids:int|None
        self.unique_pdxs:list|None
        self.num_unique_pdxs:int|None
        self.unique_disease_types:list|None
        self.num_disease_types:int|None

        # Add on columns
        self.unique_experimental_groups:list[str]|None
        self.num_experimental_groups:int|none
        self.unique_matched_controls:list|None
        self.num_matched_controls:int|None
        self.num_unmatched:int|None

        # Create time series dictionary
        self.tumor_vol_time_series_dict:dict[str:TumorVolumeTimeSeriesClass]|None = None
        self.tumor_vol_study_dict:dict[str:TumorVolumeStudyClass|None] = None
        self.tumor_vol_experiment_dict:dict[str,TumorVolumeExperimentClass|None] = None

    # File loading
    def load_tmz_csv(self, fn, volume_units='mm^3', weight_units='mg'):
        try:
            df = pd.read_csv(fn)
            self.tmz_data_df = df
            self.tmz_data_fn = fn
        except FileNotFoundError:
            logger.info(f'Could not load the cnv file: {fn}')
            return

        # Store units
        self.volume_units = volume_units
        self.weight_units = weight_units

        # create column rename dictionary
        column_rename_dict = {col_nm: sanitize_column_names(col_nm) for col_nm in df.columns}
        df.rename(columns=column_rename_dict, inplace=True)
        loaded_column_names = list(df.columns)

        # Check column names
        column_names_checked_out, _, _ = self.check_column_names(self.tmz_col_names, loaded_column_names)

        # Create internal summary and time series objects
        self.summarize_data_frame()

        # Create class dictionaries
        self.create_time_series_dict()
        self.create_study_dict()
        self.create_experiment_dict()
    @staticmethod
    def check_column_names(standard_column_names:str, file_column_names:str)->tuple[bool, list, list]:
        # Define return value
        column_names_check_out = True

        # Check column names
        missing_column_names = [cn for cn in file_column_names if cn not in standard_column_names]
        columns_not_included = [cn for cn in standard_column_names if cn not in file_column_names]

        # Check for missing or unspecified columns
        if missing_column_names:
            column_names_check_out = False
            logger.info(f'Extra columns are included')
        if columns_not_included:
            column_names_check_out = False
            logger.info(f'Columns are missing: {columns_not_included}')


        return column_names_check_out, missing_column_names, columns_not_included

    # Generate internal structures: summarize, create time sereies
    def summarize_data_frame(self):
        # Helper function
        unique = lambda x: list(set(x))

        # Data Summary
        self.num_of_data_points = self.tmz_data_df.shape[0]
        self.num_of_time_series = len(unique(self.tmz_data_df['id']))

        # Study summary
        self.unique_contributors = unique(self.tmz_data_df['contributor'])
        self.unique_contributors.sort()
        self.num_of_contributors = len(unique(self.tmz_data_df['contributor']))
        self.unique_arms = unique(self.tmz_data_df['arms'])
        self.num_of_arms = len(unique(self.tmz_data_df['arms']))
        self.unique_studies = unique(self.tmz_data_df['study'])
        self.num_of_studies = len(unique(self.tmz_data_df['study']))
        self.unique_pdx_ids = unique(self.tmz_data_df['id'])
        self.num_unique_pdx_ids = len(unique(self.tmz_data_df['id']))
        self.unique_pdxs = unique(self.tmz_data_df['tumor'])
        self.num_unique_pdxs = len(unique(self.tmz_data_df['tumor']))
        self.unique_disease_types = unique(self.tmz_data_df['disease_type'])
        self.num_disease_types = len(unique(self.tmz_data_df['disease_type']))

        # Supplemental variables
        self.unique_experiments = unique(self.tmz_data_df['experiment'])
        self.num_experiments = unique(self.tmz_data_df['experiment'])

        unmatched_str = self.unmatched_control_entry
        unique_matched_controls = unique(self.tmz_data_df['matched_controls'])
        self.unique_matched_controls = [entry for entry in unique_matched_controls if entry.lower() != unmatched_str]
        self.num_matched_controls = len(self.unique_matched_controls)
        self.num_unmatched = len(unique_matched_controls) - self.num_matched_controls

        # sort lists
        summary_lists = [self.unique_contributors, self.unique_arms, self.unique_studies,
                         self.unique_pdx_ids, self.unique_pdxs, self.unique_disease_types,
                         self.unique_matched_controls]
        for slist in summary_lists:
            slist.sort(key=lambda x: pad_all_numbers(x, min_width=4))
    def create_time_series_dict(self):
        # Prepare data structure to analyze and plot individual time series

        # Check if data is avaialble
        if self.unique_pdx_ids is None:
            logger.info('Load data before creating time_series dictionary')
            return

        # Loop through pdx ids
        df = self.tmz_data_df
        tumor_vol_time_series_dict = {}
        for pdx in self.unique_pdx_ids:
            # Time series
            time_day = np.array(df.loc[df['id'] == pdx, 'times'].values)
            tumor_volume = np.array(df.loc[df['id'] == pdx, 'volume'].values)
            tumor_weight = np.array(df.loc[df['id'] == pdx, 'body_weight'].values)

            # Time Series Unit
            volume_units = self.volume_units
            weight_units = self.weight_units

            # Study variables
            contributor = df[df['id'] == pdx]['contributor'].iloc[0]
            arm = df[df['id'] == pdx]['arms'].iloc[0]
            study_group = df[df['id'] == pdx]['experiment'].iloc[0]
            study = df[df['id'] == pdx]['study'].iloc[0]
            pdx_id = df[df['id'] == pdx]['id'].iloc[0]
            tumor = df[df['id'] == pdx]['tumor'].iloc[0]
            disease_type = df[df['id'] == pdx]['disease_type'].iloc[0]
            matched_controls = df[df['id'] == pdx]['matched_controls'].iloc[0]

            # Build and save time series object
            tv_time_series_obj = TumorVolumeTimeSeriesClass(time_day, tumor_volume, tumor_weight,
                contributor, arm, study_group, study, pdx_id, tumor, disease_type, matched_controls,
                volume_units=volume_units, weight_units=weight_units)
            tumor_vol_time_series_dict[pdx] = tv_time_series_obj
        self.tumor_vol_time_series_dict = tumor_vol_time_series_dict
    def create_study_dict(self):
        # Prepare study data structure for analysis and visualization

        # Check if data is available
        if self.unique_studies is None:
            logger.info('Can not generate study dictionary. Load data file first.')
            return

        # Create dictionary
        tumor_vol_study_dict = {}
        df = self.tmz_data_df
        for study in self.unique_studies:
            # Get information to create study class
            arms_col = list(df.loc[df['study'] == study, 'arms'].values)
            id_col = list(df.loc[df['study'] == study, 'id'].values)
            tumor_col = list(df.loc[df['study'] == study, 'tumor'].values)

            # Create a study specific time series dictionary
            unique_study_ids = list(set(id_col))
            study_tv_time_dict = { id:self.tumor_vol_time_series_dict[id] for id in unique_study_ids}

            # Create study object
            tv_study_obj = TumorVolumeStudyClass(study, arms_col, id_col, tumor_col, study_tv_time_dict)
            tumor_vol_study_dict[study] = tv_study_obj

        # Store study dictionary
        self.tumor_vol_study_dict = tumor_vol_study_dict
    def create_experiment_dict(self):
        # Prepare experimental group data structure for analysis and visualization

        # Check if data is available
        if self.unique_experiments is None:
            logger.info('Can not generate experimental group dictionary. Load data file first.')
            return

        # Create dictionary
        tumor_vol_experiment_dict = {}
        df = self.tmz_data_df
        for experiment in self.unique_experiments:
            # Get information to create study class
            experiment_col = list(df.loc[df['experiment'] == experiment, 'experiment'].values)
            study_col = list(df.loc[df['experiment'] == experiment, 'study'].values)
            arms_col = list(df.loc[df['experiment'] == experiment, 'arms'].values)

            # Create experimental group class
            data_file_name = self.tmz_data_fn
            study_dict = self.tumor_vol_study_dict
            tv_experiment_obj = TumorVolumeExperimentClass(experiment, experiment_col, study_col, study_dict)

            # Store tumor volume experimental group object
            tumor_vol_experiment_dict[experiment] = tv_experiment_obj

        # Store study dictionary
        self.tumor_vol_experiment_dict = tumor_vol_experiment_dict

    # Command line summary
    def write_file_summary_text(self):
        # Data Summary
        logger.info(f'num_of_data_points = {self.num_of_data_points}')
        logger.info(f'num_of_time_series = {self.num_of_time_series}\n')

        # Study Summary
        logger.info(f'num_of_contributors = {self.num_of_contributors}')
        write_title_list('unique_contributors', self.unique_contributors)

        logger.info(f'num_of_arms = {self.num_of_arms}')
        write_title_list('unique_arms', self.unique_arms)

        logger.info(f'num_of_studies = {self.num_of_studies}')
        write_title_list('unique_studies', self.unique_studies)

        logger.info(f'num_unique_pdx_ids = {self.num_unique_pdx_ids}')
        logger.info(f'unique_pdx_ids')
        column_print(self.unique_pdx_ids, number_of_columns=5)

        logger.info(f'num_unique_pdxs = {self.num_unique_pdxs}')
        write_title_list('unique_pdxs', self.unique_pdxs)

        logger.info(f'num_disease_types = {self.num_disease_types}\n')
        write_title_list('unique_disease_types', self.unique_disease_types)

        # Add on columns
        logger.info(f'unique_matched_controls')
        column_print(self.unique_matched_controls, number_of_columns=5)
        logger.info(f'num_matched_controls = {self.num_matched_controls}')
        logger.info(f'num_unmatched = {self.num_unmatched}')
    def list_time_series(self):
        # check if file is loaded
        if self.unique_pdx_ids is None:
            logger.info('')
        # Write one line time series description to command line
        logger.info('')
        for pdx in self.unique_pdx_ids:
            tv_time_series_obj = self.tumor_vol_time_series_dict[pdx]
            logger.info(tv_time_series_obj.summary())
    def write_study_summary(self):

        # Write study summary header
        logger.info('')
        logger.info('')
        logger.info(f'Data file: {self.tmz_data_fn}')
        logger.info(f'Study ids: ' + ', '.join(self.unique_studies))

        # Write study summary to log file
        for study in self.unique_studies:
            study_obj = self.tumor_vol_study_dict[study]
            study_obj.summarize()

    # Class functions
    def __str__(self):
        number_of_points = 0
        file_str = 'Not Set'
        if self.tmz_data_fn is not None:
            file_str = self.tmz_data_fn
            number_of_points = self.num_of_data_points
        return f'Tumor Volume Data Class, num of data points = {number_of_points}, file: {file_str} '

# Test tumor volume classes
def main():
    # Test Flag
    testing_in_process = False
    established_test = False

    # test data
    test_data_tmz = Path("public_data") / "consensus" / "PVA_with_study_group.csv"

    # Example 1: Create data structures
    tvd_obj = TumorVolumeDataClass()
    tvd_obj.load_tmz_csv(test_data_tmz)
    tvd_obj.write_file_summary_text()
    tvd_obj.list_time_series()

    # Example 2
    if established_test:
        pdx_id = tvd_obj.unique_pdx_ids[0]
        pdx_time_obj = tvd_obj.tumor_vol_time_series_dict[pdx_id]
        pdx_time_obj.plot()
        pdx_time_obj.plot(plot_weight=False)

    # Example 3
    if established_test:
        pdx_time_obj.plot(plot_weight=False, tv_transform_str="No Transform", volume_label = "Tumor Volume", volume_units = "mm^3")
        pdx_time_obj.plot(plot_weight=False, tv_transform_str="Percent Change", volume_label = "Tumor Volume Change", volume_units = "%")
        pdx_time_obj.plot(plot_weight=False, tv_transform_str="Prop. Vol. Change", volume_label = "Log2(Proportion Volume Change)", volume_units = "")
        pdx_time_obj.plot(plot_weight=False, tv_transform_str="Percent Prgress/Regress", volume_label = "% Progression/Regression Endpoint", volume_units = "")

    # Example 4
    if established_test:
        tvd_obj.write_study_summary()

    # Example 5
    if established_test:
        aggregate_marker = 'o'
        for study in tvd_obj.unique_studies:
            first_study_obj = tvd_obj.tumor_vol_study_dict[study]
            first_study_obj.plot_spider(plot_weight = False, show_individual=True, show_aggregate=False, aggregate_sem=False)
            first_study_obj.plot_spider(show_individual=True,show_aggregate=False, aggregate_sem=False)
            first_study_obj.plot_spider(show_individual=False,show_aggregate=True, aggregate_sem=False, aggregate_marker=aggregate_marker)
            first_study_obj.plot_spider(show_individual=False,show_aggregate=True, aggregate_sem=True, aggregate_marker=aggregate_marker)
            first_study_obj.plot_spider(show_individual=False, show_aggregate=True, aggregate_sem=True,
                                        aggregate_marker=aggregate_marker, error_bars=True)

    # Example 6
    if established_test:
        study = tvd_obj.unique_studies[2]
        first_study_obj = tvd_obj.tumor_vol_study_dict[study]
        first_study_obj.plot_spider(show_individual=True,show_aggregate=False, aggregate_sem=False,
                                    tv_transform_str="No Transform", volume_label="Tumor Volume", volume_units="mm^3",
                                    plot_weight=False)
        first_study_obj.plot_spider(show_individual=True, show_aggregate=False, aggregate_sem=False,
                                    tv_transform_str="Percent Change", volume_label="Tumor Volume Change", volume_units="%",
                                    plot_weight=False)
        first_study_obj.plot_spider(show_individual=True, show_aggregate=False, aggregate_sem=False,
                                    tv_transform_str="Prop. Vol. Change", volume_label="Log2(Proportion Volume Change)", volume_units="",
                                    plot_weight=False)
        first_study_obj.plot_spider(show_individual=True, show_aggregate=False, aggregate_sem=False,
                                    tv_transform_str="Percent Prgress/Regress", volume_label="% Progression/Regression Endpoint",
                                    volume_units="", plot_weight=False)

    # Example 7: Survival Free Curve
    if established_test:
        study = tvd_obj.unique_studies[2]
        first_study_obj = tvd_obj.tumor_vol_study_dict[study]
        title = f"{study} - Event-Free Survival (Tumor Volume Doubling)"
        first_study_obj.plot_event_free_survival(delta=1.0, cutoff=None, figsize=(10, 8),title=title)
        first_study_obj.plot_event_free_survival(delta=1.0, cutoff=None, figsize=(10, 8),title=title,
                                                 show_number_at_risk_plot=False, show_at_risk_table=False)

    #Example 8: Experimental Group
    if established_test:
        unique_experiments = tvd_obj.unique_experiments
        for experiment in unique_experiments:
            exp_obj = tvd_obj.tumor_vol_experiment_dict[experiment]
            exp_obj.summarize()

    # Example 9: CLass AUC
    if established_test:
        study_keys = tvd_obj.unique_studies
        day = 21
        for study in study_keys:
            title = f"{study} - Normalized AUC by Arm - Day {day}"
            study_obj = tvd_obj.tumor_vol_study_dict[study]
            study_obj.plot_auc_bar(title=title, compute_day=day, plot_normalized_auc = True, show_legend = True,
                                   show_axis_labels=True)

    # Example  10: change in tumor volume
    if established_test:
        study_keys = tvd_obj.unique_studies
        day = None
        for study in study_keys:
            title = f"{study} - Change in Tumor Volume"
            study_obj = tvd_obj.tumor_vol_study_dict[study]
            plot_normalized_tv_change = False
            study_obj.plot_percent_tumor_vol_change_bar(title=title, compute_day=day,
                plot_normalized_tv_change=plot_normalized_tv_change, show_legend=True, show_axis_labels=False)

    # Example  11: Tumor volume as objective response
    if established_test:
        study_keys = tvd_obj.unique_studies
        day = None
        for study in study_keys:
            title = f"{study} - Tumor Volume Change as Objective Response"
            study_obj = tvd_obj.tumor_vol_study_dict[study]
            plot_normalized_tv_change = False
            study_obj.plot_vol_change_as_objective_response_bar(title=title, compute_day=day,
                show_legend=True, show_axis_labels=False)

    # Example  12: Average Tumor Volume Change Experiment
    if established_test:
        experiments = tvd_obj.unique_experiments
        experiments.sort()
        for experiment in experiments:
            tvd_experiment_obj = tvd_obj.tumor_vol_experiment_dict[experiment]
            tvd_experiment_obj.plot_average_tumor_volume_change_bar()
            print(tvd_experiment_obj)

    # Example  13: Objective Response by Study
    if established_test:
        experiments = tvd_obj.unique_experiments
        experiments.sort()
        for experiment in experiments:
            tvd_experiment_obj = tvd_obj.tumor_vol_experiment_dict[experiment]
            tvd_experiment_obj.proportion_in_objective_response_classification_bar()
            print(tvd_experiment_obj)

    # Example  14: Plot AUC average with controls
    if True:
        experiments = tvd_obj.unique_experiments
        experiments.sort()
        for experiment in experiments:
            tvd_experiment_obj = tvd_obj.tumor_vol_experiment_dict[experiment]
            tvd_experiment_obj.plot_auc_with_controls_bar()
            print(tvd_experiment_obj)
if __name__ == '__main__':
    main()