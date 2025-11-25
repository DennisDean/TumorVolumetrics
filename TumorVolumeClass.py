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

        # Transforms
        self.tv_transform_options = ["No Transform", "Percent Change", "Prop. Vol. Change", "Percent Prgress/Regress"]
        self.tv_transform_dict = {"No Transform":self.tv_to_tv,
                                  "Percent Change":self.tv_percent_change,
                                  "Prop. Vol. Change":self.tv_proportion_volume_change,
                                  "Percent Prgress/Regress":self.tv_percent_prog_regres_endpoint}
        self.tv_transform_str = "No Transform"
        self.tv_transform_f = self.tv_to_tv

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

    # Summary
    def summary(self)->str:
        # Set values after check
        contributor = 'Not Set' if self.contributor is None else self.contributor
        arm = 'Not Set' if self.arm is None else self.arm
        study = 'Not Set' if self.study is None else self.study
        pdx_id = 'Not Set' if self.pdx_id is None else self.pdx_id

        class_str = f'TV Data: pdx_id: {pdx_id}, contributor: {contributor}, arm: {arm}, study: {study}, num points: {self.num_points}'
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
                                 show_number_at_risk_plot=True, show_at_risk_table=True):
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
            km.plot(ax=ax_km, ci_show=False, color=arm_colors[arm], linewidth=2)

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
        self.tmz_col_names:list|None  = ['contributor', 'arms', 'times', 'volume', 'study_group',
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
        self.unique_matched_controls:list|None
        self.num_matched_controls:int|None
        self.num_unmatched:int|None

        # Create time series dictionary
        self.tumor_vol_time_series_dict:dict[str:TumorVolumeTimeSeriesClass]|None = None
        self.tumor_vol_study_dict:dict[str:TumorVolumeStudyClass|None] = None

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
        self.create_time_series_dict()
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
            study_group = df[df['id'] == pdx]['study_group'].iloc[0]
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
        # Prepare if study data structure for analysis and visualization

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
    # test data
    test_data_tmz = Path("public_data") / "consensus" / "PVA_with_study_group.csv"

    # Example 1: Create data structures
    tvd_obj = TumorVolumeDataClass()
    tvd_obj.load_tmz_csv(test_data_tmz)
    tvd_obj.write_file_summary_text()
    tvd_obj.list_time_series()

    # Example 2
    if True:
        pdx_id = tvd_obj.unique_pdx_ids[0]
        pdx_time_obj = tvd_obj.tumor_vol_time_series_dict[pdx_id]
        pdx_time_obj.plot()
        pdx_time_obj.plot(plot_weight=False)

    # Example 3
    if True:
        pdx_time_obj.plot(plot_weight=False, tv_transform_str="No Transform", volume_label = "Tumor Volume", volume_units = "mm^3")
        pdx_time_obj.plot(plot_weight=False, tv_transform_str="Percent Change", volume_label = "Tumor Volume Change", volume_units = "%")
        pdx_time_obj.plot(plot_weight=False, tv_transform_str="Prop. Vol. Change", volume_label = "Log2(Proportion Volume Change)", volume_units = "")
        pdx_time_obj.plot(plot_weight=False, tv_transform_str="Percent Prgress/Regress", volume_label = "% Progression/Regression Endpoint", volume_units = "")

    # Example 4
    tvd_obj.create_study_dict()
    tvd_obj.write_study_summary()

    # Example 5
    if True:
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
    if True:
        study = tvd_obj.unique_studies[2]
        first_study_obj = tvd_obj.tumor_vol_study_dict[study]
        first_study_obj.plot_spider(show_individual=True,show_aggregate=False, aggregate_sem=False,
                                    tv_transform_str="No Transform", volume_label="Tumor Volume", volume_units="mm^3")
        first_study_obj.plot_spider(show_individual=True, show_aggregate=False, aggregate_sem=False,
                                    tv_transform_str="Percent Change", volume_label="Tumor Volume Change", volume_units="%")
        first_study_obj.plot_spider(show_individual=True, show_aggregate=False, aggregate_sem=False,
                                    tv_transform_str="Prop. Vol. Change", volume_label="Log2(Proportion Volume Change)", volume_units="")
        first_study_obj.plot_spider(show_individual=True, show_aggregate=False, aggregate_sem=False,
                                    tv_transform_str="Percent Prgress/Regress", volume_label="% Progression/Regression Endpoint", volume_units="")

    # Example 7: Survival Free Curve
    if True:
        study = tvd_obj.unique_studies[2]
        first_study_obj = tvd_obj.tumor_vol_study_dict[study]
        title = f"{study} - Event-Free Survival (Tumor Volume Doubling)"
        first_study_obj.plot_event_free_survival(delta=1.0, cutoff=None, figsize=(10, 8),title=title)
        first_study_obj.plot_event_free_survival(delta=1.0, cutoff=None, figsize=(10, 8),title=title,
                                                 show_number_at_risk_plot=False, show_at_risk_table=False)


if __name__ == '__main__':
    main()