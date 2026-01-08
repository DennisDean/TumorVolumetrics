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
#TODO: Enable matplotlib figure garbage collection

# Import modules

# Setup Log file
from logging_config import logger

# Utilities
import copy
import logging
import os
import re
from pathlib import Path
from typing import Optional

# Data
import pandas as pd
import numpy as np
import uuid
import xml.etree.ElementTree as ET

# Computation
import bisect
import math
from lifelines import KaplanMeierFitter
from scipy.stats import sem, t, ttest_ind

# Visualization
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from contextlib import nullcontext
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
import scienceplots

# GUI
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy


# Set up logger
# Create logs directory if it does not exist
os.makedirs("logs", exist_ok=True)
log_file = os.path.join("logs", "app.log")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[
        logging.FileHandler(log_file),   # Log to file
        logging.StreamHandler()          # Log to console
    ])
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
def remove_alpha(text):
    """
    Remove all alphabetic characters (a-z, A-Z) from a string.
    Keeps numbers, spaces, punctuation, and special characters.

    Args:
        text: Input string

    Returns:
        String with alphabetic characters removed
    """
    return ''.join(char for char in text if not char.isalpha())
def set_xaxis_visible(ax, visible: bool, label: str | None = None):
    ax.tick_params(axis="x", which="both",
                   bottom=visible, labelbottom=visible)
    ax.xaxis.label.set_visible(visible)
    if visible and label is not None:
        ax.set_xlabel(label)

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

    # Return
    def return_log2_change(self, compute_day:int|None = None):
        t_day = self.time_day
        compute_day = t_day[-1] if compute_day is None else compute_day
        compute_day_index = self.get_compute_day_index(t_day, compute_day)
        log2_change = np.log2(self.tumor_volume[compute_day_index]/self.tumor_volume[0])
        return log2_change
    def get_compute_day_index(self, time_day, compute_day):
        idx = bisect.bisect_right(time_day, compute_day)

        # If compute_day is greater than all days, return last index
        if idx >= len(time_day):
            return len(time_day) - 1

        # If exact match exists, return that index
        if idx > 0 and time_day[idx - 1] == compute_day:
            return idx - 1

        # Otherwise idx is already the "larger neighbor"
        return idx

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
        self.tv_transform_label_dict = {
                                  "No Transform": "Tumor Volume",
                                  "Percent Change": "Percent Change",
                                  "Prop. Vol. Change": f"Proportional TV Change",
                                  "Percent Prgress/Regress": "Percent Prgress/Regress"}
        self.tv_transform_units_dict = {
                                  "No Transform": "Tmm*3",
                                  "Percent Change": "%",
                                  "Prop. Vol. Change": f"",
                                  "Percent Prgress/Regress": "%"}
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

        # Create plotting dictionary
        self.plotting_function_dict_2 = {
            "Spider Plot":
                {"function": "plot_spider",
                 "params": {
                    "plot_weight": {"type": "bool","default": True,"label": "Show Weight"},
                    "show_individual": {"type": "bool","default": True,"label": "Show Individual Lines"},
                    "show_aggregate": {"type": "bool","default": True,"label": "Show Aggregate Line"},
                    "aggregate_sem": {"type": "bool","default": True,"label": "Show SEM on Aggregate"},
                    "error_bars": {"type": "bool","default": False,"label": "Show Error Bars"},
                    "tv_transform_str": {"type": "combo","default": "No Transform",
                        "options": ["No Transform", "Log", "Normalize", "Percent Change"],"label": "Volume Transform"},
                    "volume_label": {"type": "text","default": "Tumor Volume","label": "Volume Label"},
                    "volume_units": {"type": "text","default": "mm^3","label": "Volume Units"},
                    "weight_label": {"type": "text","default": "Weight","label": "Weight Label"},
                    "weight_units": {"type": "text","default": "mg","label": "Weight Units"},
                    "title": {"type": "text","default": None,"label": "Custom Title"}
                    }
                },
            "Event-Free Survival":
               {"function": "plot_event_free_survival",
                "params": {
                    "delta": {"type": "float","default": 1.0,"label": "Delta (Doubling Threshold)","min": 0.1,"max": 10.0,"step": 0.1},
                    "cutoff": {"type": "float","default": None,"label": "Cutoff Day (None = auto)","min": 0,"max": 365,"step": 1,"nullable": True},
                    "show_number_at_risk_plot": {"type": "bool","default": True,"label": "Show Number at Risk Plot"},
                    "show_at_risk_table": {"type": "bool","default": True,"label": "Show At-Risk Table"},
                    "title": {"type": "text","default": "Event-Free Survival (Tumor Volume Doubling)","label": "Title"}
                    }
                },
            "AUC Bar Chart":
               {"function": "plot_auc_bar",
                "params": {
                    "compute_day": {"type": "int","default": None,"label": "Compute Through Day","min": 1,"max": 365,"step": 1,"nullable": True},
                    "sort_descending": {"type": "bool","default": True,"label": "Sort Descending"},
                    "plot_normalized_auc": {"type": "bool","default": False,"label": "Plot Normalized AUC"},
                    "show_bar_labels": {"type": "bool","default": False,"label": "Show Value Labels on Bars"},
                    "show_axis_labels": {"type": "bool","default": True,"label": "Show Axis Labels"},
                    "show_legend": {"type": "bool","default": True,"label": "Show Legend"},
                    "remove_text_x_labels": {"type": "bool","default": True,"label": "Remove Text X-Labels"},
                    "bar_alpha": {"type": "float","default": 0.85,"label": "Bar Transparency","min": 0.0,"max": 1.0,"step": 0.05},
                    "title": {"type": "text","default": "AUC by Arm","label": "Title"}
                }
            },
            "Tumor Volume Change (%)": {
                "function": "plot_percent_tumor_vol_change_bar",
                "params": {
                    "compute_day": {"type": "int","default": None,"label": "Compute At Day","min": 1,"max": 365,"step": 1,"nullable": True},
                    "sort_descending": {"type": "bool","default": True,"label": "Sort Descending"},
                    "plot_normalized_tv_change": {"type": "bool","default": False,"label": "Plot Normalized TV Change"},
                    "show_bar_labels": {"type": "bool","default": False,"label": "Show Value Labels on Bars"},
                    "show_axis_labels": {"type": "bool","default": True,"label": "Show Axis Labels"},
                    "show_legend": {"type": "bool","default": True,"label": "Show Legend"},
                    "bar_alpha": {"type": "float","default": 0.85,"label": "Bar Transparency","min": 0.0,"max": 1.0,"step": 0.05},
                    "title": {"type": "text","default": "Tumor Volume Change (%)","label": "Title"}
                }
            },
            "Objective Response": {
                "function": "plot_vol_change_as_objective_response_bar",
                "params": {
                    "compute_day": {"type": "int","default": None,"label": "Compute At Day","min": 1,"max": 365,"step": 1,"nullable": True},
                    "sort_descending": {"type": "bool","default": True,"label": "Sort Descending"},
                    "show_bar_labels": {"type": "bool","default": False,"label": "Show Value Labels on Bars"},
                    "show_axis_labels": {"type": "bool","default": True,"label": "Show Axis Labels"},
                    "show_legend": {"type": "bool","default": True,"label": "Show Legend"},
                    "bar_alpha": {"type": "float","default": 0.85,"label": "Bar Transparency","min": 0.0,"max": 1.0,"step": 0.06},
                    "title": {"type": "text","default": "Objective Response","label": "Title"}
                }
            }
        }

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
        """
        Compute the event time for one mouse.

        Event defined as tumor volume increasing by factor (1+delta).

        Parameters
        ----------
        time_day : array-like
            Time points in days
        volume : array-like
            Tumor volumes
        delta : float
            Threshold for event (volume increase factor)
        cutoff : float or None
            Time cutoff for censoring (in days)

        Returns
        -------
        tuple : (event_time, event_flag)
            event_time: time of event or censoring
            event_flag: 1 if event occurred, 0 if censored
        """
        if len(volume) == 0:
            return None, 0

        baseline = volume[0]
        doubling_threshold = baseline * (1 + delta)

        for t, v in zip(time_day, volume):
            # If we've passed the time cutoff, censor here
            if cutoff is not None and t > cutoff:
                return cutoff, 0  # Censored at cutoff time

            # Check if event occurred
            if v >= doubling_threshold:
                # If event is before cutoff, it's a real event
                if cutoff is None or t <= cutoff:
                    return t, 1
                else:
                    # Event happened after cutoff, so censor at cutoff
                    return cutoff, 0

        # No event occurred during observation period
        # Censor at the cutoff time or last observation time
        if cutoff is not None:
            last_time = time_day[-1]
            return min(last_time, cutoff), 0
        else:
            return time_day[-1], 0
    def compute_event_time_2(self, time_day, volume, delta=1.0, cutoff=None):
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

                t, e = self.compute_event_time(ts.time_day,ts.tumor_volume,delta=delta,cutoff=cutoff)

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

    # Visualization Utilities
    def plot_to_widget_by_name(self, plot_name, parent_widget, plot_style=None, **plot_kwargs):
        """
        Call a plotting function by name and render to a widget.

        Args:
            plot_name: String name of the plotting method
            parent_widget: Qt widget to embed the plot
            **plot_kwargs: Any keyword arguments to pass to the plotting function

        Returns:
            Result from the plotting function (typically (fig, ax) tuple)

        Example:
            # Call by string name
            experiment_obj.plot_to_widget_by_name(
                "plot_average_tumor_volume_change_bar",
                graphic_view,
                error_metric="sem"
            )
        """
        # Get the method by name
        plot_function = getattr(self, plot_name, None)
        if plot_function is None:
            raise ValueError(f"Plot function '{plot_name}' not found")

        if not callable(plot_function):
            raise ValueError(f"'{plot_name}' is not a callable method")

        return plot_function(parent_widget=parent_widget, plot_style=plot_style, **plot_kwargs)
    def _create_styled_figure(self, plot_style=None, parent_widget=None):
        """
        Create a matplotlib figure with optional style applied, supporting both standalone and Qt widget modes.

        Args:
            plot_style: Style(s) to apply. Can be:
                       - None: Use default matplotlib style
                       - str: Single style name (e.g., 'seaborn-v0_8', 'ggplot')
                       - list: Multiple styles (e.g., ['science', 'ieee'] for SciencePlots)
            parent_widget: Optional Qt widget to embed the plot. If None, creates standalone figure.

        Returns:
            tuple: (fig, ax, style_context) where:
                - fig: matplotlib Figure object
                - ax: matplotlib Axes object
                - style_context: Context manager for style (use with 'with' statement)

        Usage:
            fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)
            with style_ctx:
                # All plotting code here
                ax.plot(x, y)
                ax.set_title("My Plot")
        """
        # Create appropriate style context
        if plot_style is not None:
            style_context = plt.style.context(plot_style)
        else:
            style_context = nullcontext()

        # Create figure WITHOUT manually entering the context
        if parent_widget:
            # Create Figure object for Qt widget embedding (size controlled by layout)
            fig = Figure()
            ax = fig.add_subplot(111)
        else:
            # Create standalone pyplot figure (will use matplotlib defaults or rcParams)
            fig, ax = plt.subplots()

        if plot_style:
            with plt.style.context(plot_style):
                # Get the colors from the style
                fig_color = plt.rcParams['figure.facecolor']
                axes_color = plt.rcParams['axes.facecolor']
                text_color = plt.rcParams['text.color']

                # Apply them to your figure
                fig.patch.set_facecolor(fig_color)
                ax.set_facecolor(axes_color)
                ax.tick_params(colors=text_color)
                ax.xaxis.label.set_color(text_color)
                ax.yaxis.label.set_color(text_color)
                ax.title.set_color(text_color)
                ax.spines['bottom'].set_color(text_color)
                ax.spines['top'].set_color(text_color)
                ax.spines['left'].set_color(text_color)
                ax.spines['right'].set_color(text_color)

        return fig, ax, style_context

    # Visualization
    def plot_spider(self, plot_style=None, figsize=(10, 6), volume_label="Tumor Volume", volume_units="mm^3",
            weight_label="Weight", weight_units="mg", title=None, plot_weight=True, show_individual=True,
            show_aggregate=True, aggregate_sem=True, error_bars=False, aggregate_marker='s',
            tv_transform_str="No Transform", parent_widget=None):
        """
        Spider plot for tumor volume study data with optional aggregation curves.

        Creates a spider plot showing individual and/or aggregate tumor volume trajectories.
        Can be embedded in a Qt widget or displayed as a standalone matplotlib figure.

        Parameters
        ----------
        plot_style : str, list, or None
            Matplotlib style sheet(s) to apply. Can be a single style name or list of styles.
            Examples: 'dark_background', 'seaborn-v0_8-darkgrid', ['dark_background', 'seaborn-v0_8-poster']
        figsize : tuple
            Figure size as (width, height) in inches. Defaults to (10, 6).
            Only applies to standalone mode.
        volume_label : str
            Label for tumor volume y-axis.
        volume_units : str
            Units for tumor volume (e.g., "mm^3").
        weight_label : str
            Label for weight y-axis.
        weight_units : str
            Units for weight (e.g., "mg").
        title : str or None
            Plot title. If None, auto-generates title from study_id.
        plot_weight : bool
            Whether to include weight subplot.
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
        tv_transform_str : str
            Transform to apply to tumor volume data. Options: "No Transform",
            "Percent Change", "Prop. Vol. Change", "Percent Prgress/Regress"
        parent_widget : QWidget or None
            Optional Qt widget to embed the plot. If provided, renders as
            a FigureCanvas within this widget. If None, creates standalone
            matplotlib figure. Defaults to None.

        Returns
        -------
        tuple or None
            (fig, ax_vol) or (fig, (ax_vol, ax_w)) - matplotlib Figure and Axes objects.
            Returns None if no valid data to plot.

        Side Effects (when parent_widget is provided)
        ---------------------------------------------
        - Sets self.current_tumor_volume_canvas to FigureCanvas
        - Replaces parent_widget's layout contents

        Raises
        ------
        ValueError
            If no time-series data available or invalid transform specified.
        """
        import numpy as np

        # Validate data
        if not self.study_tv_time_dict:
            raise ValueError("No time-series data available.")

        # Get transform function
        if tv_transform_str not in self.tv_transform_dict:
            raise ValueError(f"Invalid transform: {tv_transform_str}. Options: {self.tv_transform_options}")

        tv_transform_f = self.tv_transform_dict[tv_transform_str]
        tv_transform_label = self.tv_transform_label_dict [tv_transform_str]

        tv_transform_units = self.tv_transform_units_dict [tv_transform_str]
        tv_transform_units = volume_units if  tv_transform_str=="No Transform" else tv_transform_units

        # Determine if any time-series contains weight
        has_weight_data = any(
            hasattr(ts, "tumor_weight") and ts.tumor_weight is not None
            for ts in self.study_tv_time_dict.values()
        )
        has_weight = plot_weight and has_weight_data

        # Create styled figure
        if has_weight:
            # Create multi-axis figure manually since _create_styled_figure returns single axis
            if plot_style is not None:
                style_context = plt.style.context(plot_style)
            else:
                from contextlib import nullcontext
                style_context = nullcontext()

            if parent_widget:
                fig = Figure()

                gs = fig.add_gridspec(
                    nrows=2,
                    ncols=1,
                    height_ratios=[4, 1],  # same as pyplot version
                    hspace=0.1
                )

                ax_vol = fig.add_subplot(gs[0])
                ax_w = fig.add_subplot(gs[1], sharex=ax_vol)

                #ax_vol = fig.add_subplot(2, 1, 1)
                #ax_w = fig.add_subplot(2, 1, 2, sharex=ax_vol)

                fig.subplots_adjust(hspace=0.1)
            else:
                fig, (ax_vol, ax_w) = plt.subplots(
                    2, 1, figsize=figsize, sharex=True,
                    gridspec_kw={'height_ratios': [4, 1]}
                )

            if plot_style:
                with plt.style.context(plot_style):
                    # Get the colors from the style
                    fig_color = plt.rcParams['figure.facecolor']
                    axes_color = plt.rcParams['axes.facecolor']
                    text_color = plt.rcParams['text.color']

                    # Apply to figure
                    fig.patch.set_facecolor(fig_color)

                    # Apply to both axes
                    for ax in [ax_vol, ax_w]:
                        ax.set_facecolor(axes_color)
                        ax.tick_params(colors=text_color)
                        ax.xaxis.label.set_color(text_color)
                        ax.yaxis.label.set_color(text_color)
                        ax.title.set_color(text_color)
                        for spine in ax.spines.values():
                            spine.set_color(text_color)

            style_ctx = style_context
        else:
            fig, ax_vol, style_ctx = self._create_styled_figure(plot_style, parent_widget)
            ax_w = None

        # Apply figsize only for standalone mode
        if not parent_widget and figsize:
            fig.set_size_inches(figsize)

        with style_ctx:
            # Color per arm - get from current style
            color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
            arm_colors = {arm: color_cycle[i % len(color_cycle)]
                          for i, arm in enumerate(self.unique_arms)}
            line_color = plt.rcParams['text.color']  # Will adapt to theme

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
                                        linewidth=1.5,
                                        capsize=4,
                                        capthick=2,
                                        color=color,
                                        ecolor=line_color)
                    else:
                        # Line style (with optional markers)
                        ax_vol.plot(time_points, mean_vol,
                                    marker= 'o' if aggregate_marker is None else aggregate_marker,
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
                                          color=color,
                                          ecolor=line_color)
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
            volume_label_str = f"{tv_transform_label} ({tv_transform_units})"
            if tv_transform_units == "":
                volume_label_str = f"{tv_transform_label}"

            ax_vol.set_ylabel(volume_label_str)

            if plot_weight:
                # Hide x-axis values on top plot
                ax_vol.tick_params(axis="x", which="both", labelbottom=False)
            else:
                # Show x-axis values on volume plot
                ax_vol.set_xlabel("Time (days)")
                ax_vol.tick_params(axis="x", which="both", labelbottom=True)

            ax_vol.minorticks_on()

            # Enable grid with style's properties
            if plot_style:
                # Handle both string and list inputs
                if isinstance(plot_style, str):
                    styles = [plot_style]
                elif isinstance(plot_style, list):
                    styles = plot_style
                else:
                    styles = []

                # Check if any style contains 'grid'
                grid_styles = ['grid', 'seaborn-v0_8-whitegrid', 'seaborn-v0_8-darkgrid']
                if any(grid_style in styles for grid_style in grid_styles):
                    ax_vol.grid(True, alpha=0.3)
                    ax_vol.grid(True, which='minor', linestyle=':', alpha=0.15)
                    ax_vol.set_axisbelow(True)
            else:
                # Default grid behavior
                ax_vol.grid(True, alpha=0.3)
                ax_vol.grid(True, which='minor', linestyle=':', alpha=0.15)

            # Add horizontal line at 0 for transformed data
            if tv_transform_str != "No Transform":
                ax_vol.axhline(y=0, color=line_color, linestyle='--', alpha=0.3, linewidth=1)

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
                ax_w.set_xlabel("Time (days)")
                ax_w.minorticks_on()

                # Ensure x-axis values are visible here
                ax_w.tick_params(axis="x", which="both", labelbottom=True)

                if plot_style:
                    if any(grid_style in styles for grid_style in grid_styles):
                        ax_w.grid(True, alpha=0.3)
                        ax_w.grid(True, which='minor', linestyle=':', alpha=0.15)
                        ax_w.set_axisbelow(True)
                else:
                    ax_w.grid(True, alpha=0.3)
                    ax_w.grid(True, which='minor', linestyle=':', alpha=0.15)

            # ================================
            # 4. TITLE
            # ================================
            if title is None:
                title = f"Tumor Volume Study - {self.study_id}"
                if tv_transform_str != "No Transform":
                    title += f" ({tv_transform_str})"

            fig.suptitle(title)

        # Handle widget integration
        if parent_widget:
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Get matplotlib's figure background color
            fig_facecolor = fig.get_facecolor()

            # Convert RGBA to hex for Qt
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            if plot_style in ['dark_background', 'seaborn-v0_8-dark']:
                fig.patch.set_facecolor(fig.get_facecolor())
                ax_vol.set_facecolor(ax_vol.get_facecolor())
                if has_weight:
                    ax_w.set_facecolor(ax_w.get_facecolor())

            # Enable right-click menu
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas

            # Store canvas reference
            self.current_tumor_volume_canvas = canvas

            # Clear existing layout
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            # Ensure proper sizing
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Draw the canvas
            canvas.draw()
        else:
            # Show plot in standalone mode
            plt.tight_layout()
            plt.show()

        if has_weight:
            return fig, (ax_vol, ax_w)
        else:
            return fig, ax_vol
    def plot_event_free_survival(self, plot_style=None, delta=1.0, cutoff=None, figsize=(10, 8),
            title="Event-Free Survival (Tumor Volume Doubling)", show_risk_plot = True, show_risk_table=True,
            parent_widget=None):
        """
        Event-free survival analysis with Kaplan-Meier curves and risk tables.

        Creates a multi-panel figure showing survival curves, numbers at risk plot, and optional table.
        Can be embedded in a Qt widget or displayed as a standalone matplotlib figure.

        Parameters
        ----------
        plot_style : str, list, or None
            Matplotlib style sheet(s) to apply. Can be a single style name or list of styles.
            Examples: 'dark_background', 'seaborn-v0_8-darkgrid', ['dark_background', 'seaborn-v0_8-poster']
        delta : float
            Threshold for defining an event (tumor volume increase factor). Defaults to 1.0 (doubling).
        cutoff : float or None
            Optional time cutoff for censoring. Defaults to None.
        figsize : tuple
            Figure size as (width, height) in inches. Defaults to (10, 8).
            Only applies to standalone mode.
        title : str
            Plot title. Defaults to "Event-Free Survival (Tumor Volume Doubling)".
        show_risk_plot : bool
            Whether to show the middle panel with line plot of numbers at risk. Defaults to True.
        show_risk_table : bool
            Whether to show the bottom panel with table of numbers at risk. Defaults to False.
        parent_widget : QWidget or None
            Optional Qt widget to embed the plot. If provided, renders as
            a FigureCanvas within this widget. If None, creates standalone
            matplotlib figure. Defaults to None.

        Returns
        -------
        tuple
            (fig, axes_dict) where axes_dict contains:
            - 'km': Kaplan-Meier curve axis (always present)
            - 'labels': Numbers at risk plot axis (if show_number_at_risk_plot=True)
            - 'risk': At-risk table axis (if show_at_risk_table=True)
            Returns None if no valid data to plot.

        Side Effects (when parent_widget is provided)
        ---------------------------------------------
        - Sets self.current_tumor_volume_canvas to FigureCanvas
        - Replaces parent_widget's layout contents
        """
        import numpy as np
        from contextlib import nullcontext

        print(cutoff, show_risk_plot, show_risk_table)

        # Variable name transition
        cutoff = cutoff
        show_number_at_risk_plot = show_risk_plot
        show_at_risk_table = show_risk_table

        # -----------------------------------------------------
        # Compute survival data
        # -----------------------------------------------------
        survival = self.build_survival_data(delta=delta, cutoff=cutoff)
        t_grid, risk_table = self.compute_numbers_at_risk(survival)
        p_val = self.compute_logrank_pvalue(survival)

        # -----------------------------------------------------
        # Create styled figure with multiple subplots
        # -----------------------------------------------------
        # Create appropriate style context
        if plot_style is not None:
            style_context = plt.style.context(plot_style)
        else:
            style_context = nullcontext()

        # Setup subplot proportions
        show_kaplan_meier_curve = True  # axis linked to km has to be true
        km_subplot_proportion = 4.0 if show_kaplan_meier_curve else 0
        num_at_risk_plot_proportion = 1.0 if show_number_at_risk_plot else 0
        spacer_proportion = .3 if show_number_at_risk_plot else 0
        at_risk_table_proportion = 1.0 if show_at_risk_table else 0

        # Determine number of subplots
        show_spacer = show_number_at_risk_plot or show_at_risk_table
        num_of_subplots = (int(show_kaplan_meier_curve) + int(show_number_at_risk_plot)
                         + int(show_spacer) + int(show_at_risk_table) )

        print(f'num_of_subplots={num_of_subplots}')

        # Set up height proportions
        height_ratios = []
        if show_kaplan_meier_curve:
            height_ratios.append(km_subplot_proportion)
        if show_number_at_risk_plot:
            height_ratios.append(num_at_risk_plot_proportion)
        if show_spacer:
            height_ratios.append(spacer_proportion)
        if show_at_risk_table:
            height_ratios.append(at_risk_table_proportion)

        # Check ratio calculation since there was a previous bug
        assert len(height_ratios) == num_of_subplots, (
            f"Layout mismatch: num_of_subplots={num_of_subplots}, height_ratios={height_ratios}")

        # Create figure
        if parent_widget:
            fig = Figure()
        else:
            fig = plt.figure(figsize=figsize)

        gs = fig.add_gridspec(num_of_subplots, 1,
                              height_ratios=height_ratios, hspace=0.3)

        # Create subplots
        current_sub_plot = 0
        axes_dict = {}
        ax_list = []

        # --- KM plot ---
        if show_kaplan_meier_curve:
            ax_km = fig.add_subplot(gs[current_sub_plot])
            axes_dict['km'] = ax_km
            ax_list.append(ax_km)
            current_sub_plot += 1
        else:
            ax_km = None  # safety

        # --- Number at risk plot ---
        if show_number_at_risk_plot:
            ax_labels = fig.add_subplot(gs[current_sub_plot], sharex=ax_km)
            axes_dict['labels'] = ax_labels
            ax_list.append(ax_labels)
            current_sub_plot += 1
        else:
            ax_labels = None

        # --- Spacer ---
        if show_spacer:
            ax_spacer = fig.add_subplot(gs[current_sub_plot])
            ax_spacer.axis("off")
            axes_dict['spacer'] = ax_spacer
            current_sub_plot += 1

        # --- At risk table ---
        if show_at_risk_table:
            ax_risk = fig.add_subplot(gs[current_sub_plot], sharex=ax_km)
            axes_dict['risk'] = ax_risk
            ax_list.append(ax_risk)
            current_sub_plot += 1
        else:
            ax_risk = None

        # Apply style colors to all axes
        if plot_style:
            with plt.style.context(plot_style):
                # Get the colors from the style
                fig_color = plt.rcParams['figure.facecolor']
                axes_color = plt.rcParams['axes.facecolor']
                text_color = plt.rcParams['text.color']

                # Apply to figure
                fig.patch.set_facecolor(fig_color)

                # Apply to all axes
                for ax in axes_dict.values():
                    ax.set_facecolor(axes_color)
                    ax.tick_params(colors=text_color)
                    ax.xaxis.label.set_color(text_color)
                    ax.yaxis.label.set_color(text_color)
                    ax.title.set_color(text_color)
                    for spine in ax.spines.values():
                        spine.set_color(text_color)

        style_ctx = style_context

        # Apply figsize only for standalone mode
        if not parent_widget and figsize:
            fig.set_size_inches(figsize)

        with style_ctx:
            # -----------------------------------------------------
            # KM curves
            # -----------------------------------------------------
            from lifelines import KaplanMeierFitter

            km = KaplanMeierFitter()
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
            arm_colors = {arm: colors[i % len(colors)] for i, arm in enumerate(self.unique_arms)}
            line_color = plt.rcParams['text.color']  # Will adapt to theme

            for arm in self.unique_arms:
                km.fit(survival[arm]["time"], survival[arm]["event"], label=arm)
                km.plot_survival_function(ax=ax_km, ci_show=False, color=arm_colors[arm], linewidth=2)

            ax_km.set_ylabel(f"Event-Free Probability")
            ax_km.set_title(f"{title} - {self.study_id}\nP-value = {p_val:.4g}")

            # Enable grid with style's properties
            if plot_style:
                # Handle both string and list inputs
                if isinstance(plot_style, str):
                    styles = [plot_style]
                elif isinstance(plot_style, list):
                    styles = plot_style
                else:
                    styles = []

                # Check if any style contains 'grid'
                grid_styles = ['grid', 'seaborn-v0_8-whitegrid', 'seaborn-v0_8-darkgrid']
                if any(grid_style in styles for grid_style in grid_styles):
                    ax_km.grid(True, alpha=0.3)
                    ax_km.set_axisbelow(True)
            else:
                ax_km.grid(True, alpha=0.3)

            # Hide top and right spines
            for spine in ["right", "left"]:
                ax_km.spines[spine].set_visible(False)

            # Set x-axis limits
            max_t = int(t_grid[-1])
            ax_km.set_xlim(-0.5, max_t + 0.5)

            # -----------------------------------------------------
            # Middle panel: AT-RISK LINE PLOTS
            # -----------------------------------------------------
            if show_number_at_risk_plot:
                ax_labels.set_ylabel("# at Risk")
                ax_labels.set_ylim(0 - 0.76, max(max(risk_table[arm]) for arm in self.unique_arms) * 1.1 + 0.5)

                # Plot line for each arm showing numbers at risk over time
                for arm in self.unique_arms:
                    ax_labels.plot(t_grid, risk_table[arm],
                                   color=arm_colors[arm],
                                   linewidth=2,
                                   marker='none',
                                   markersize=4,
                                   label=arm)

                ax_labels.tick_params(axis='x', which='both', bottom=False, labelbottom=False)

                # Grid handling
                if plot_style and any(grid_style in styles for grid_style in grid_styles):
                    ax_labels.grid(True, alpha=0.3, axis='y')
                    ax_labels.set_axisbelow(True)
                else:
                    ax_labels.grid(True, alpha=0.3, axis='y')

                # ax_labels.legend(loc='best', framealpha=0.9)

                # Hide top and right spines
                for spine in ["right", "left"]:
                    ax_labels.spines[spine].set_visible(False)

                # Match x-axis limits with KM plot
                ax_labels.set_xlim(-0.5, max_t + 0.5)

            # -----------------------------------------------------
            # Bottom panel: NUMBERS AT RISK
            # -----------------------------------------------------
            if show_at_risk_table:
                ax_risk.set_yticks(range(len(self.unique_arms)))
                ax_risk.set_yticklabels(self.unique_arms)
                # ax_risk.set_xlabel("Time (days)")
                ax_risk.set_xlim(-0.5, max_t + 0.5)
                ax_risk.set_ylim(-1, len(self.unique_arms) + 0.3)

                # Clear spines except left
                for spine in ["right", "left"]:
                    ax_risk.spines[spine].set_visible(False)

                # Plot the numbers at risk
                for i, arm in enumerate(self.unique_arms):
                    # invisible line to preserve alignment
                    ax_risk.plot(t_grid, [i] * len(t_grid), alpha=0)

                    for x, y_val in zip(t_grid, risk_table[arm]):
                        ax_risk.text(x, i, f"{y_val}", ha="center", va="center",
                                     fontsize=10, color=line_color)

                ax_risk.grid(False)

            # ----------------------------------------------------
            # Conditional x-axis ownership logic
            # ----------------------------------------------------
            if show_number_at_risk_plot:
                xaxis_owner = ax_labels
            else:
                xaxis_owner = ax_km

            for ax in (ax_list):
                set_xaxis_visible(ax, ax is xaxis_owner, label="Time (days)")


        # Handle widget integration
        if parent_widget:
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Get matplotlib's figure background color
            fig_facecolor = fig.get_facecolor()

            # Convert RGBA to hex for Qt
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            if plot_style in ['dark_background', 'seaborn-v0_8-dark']:
                fig.patch.set_facecolor(fig.get_facecolor())
                for ax in axes_dict.values():
                    ax.set_facecolor(ax.get_facecolor())

            # Enable right-click menu
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas

            # Store canvas reference
            self.current_tumor_volume_canvas = canvas

            # Clear existing layout
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            # Ensure proper sizing
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Draw the canvas
            canvas.draw()
        else:
            # Show plot in standalone mode
            plt.show()

        return fig, axes_dict
    def plot_auc_bar(self, compute_day: int | None = None,
            figsize=(12, 6), sort_descending=True, control_arms=("control", "vehicle", "placebo"),bar_alpha=0.85,
            bar_edgecolor="black", show_bar_labels=False, title="AUC by Arm", color_cycle=None,
            show_axis_labels: bool = True, plot_normalized_auc=False, show_legend: bool = True, plot_style=None,
            parent_widget=None, remove_text_x_labels = True):
        """
        Vertical bar plot of AUC values for each time-series.
        Controls are plotted first, followed by experimental arms.

        Supports matplotlib styles and embedding into a PySide6 Graphics/View widget.
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

                value = normalized_auc if plot_normalized_auc else auc_val
                arm_auc.append((ts_id, value))

            arm_auc.sort(key=lambda x: x[1], reverse=sort_descending)
            auc_dict[arm] = arm_auc

        # -------------------------------------------
        # 2. ARM ORDERING
        # -------------------------------------------
        controls = [a for a in unique_arms if a.lower() in control_arms]
        experimental = [a for a in unique_arms if a not in controls]
        ordered_arms = controls + experimental

        # # -------------------------------------------
        # # 3. COLOR MAP FOR ARMS
        # # -------------------------------------------
        # if color_cycle is None:
        #     color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        #
        # arm_colors = {
        #     arm: color_cycle[i % len(color_cycle)]
        #     for i, arm in enumerate(ordered_arms)
        # }

        # # -------------------------------------------
        # # 4. FLATTEN BAR DATA
        # # -------------------------------------------
        # bar_x_positions = []
        # bar_heights = []
        # bar_colors = []
        # bar_labels = []
        #
        # idx = 0
        # for arm in ordered_arms:
        #     for ts_id, auc_val in auc_dict[arm]:
        #         bar_x_positions.append(idx)
        #         bar_heights.append(auc_val)
        #         bar_colors.append(arm_colors[arm])
        #         bar_labels.append(remove_alpha(str(ts_id)))
        #         idx += 1
        #     idx += 1
        #
        # if not bar_heights:
        #     logger.info("No AUC values to plot")
        #     return None

        # -------------------------------------------
        # 5. PLOTTING (STYLE + QT SUPPORT)
        # -------------------------------------------
        fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)

        if not parent_widget and figsize:
            fig.set_size_inches(figsize)

        with style_ctx:

            # -------------------------------------------
            # COLOR MAP FOR ARMS
            # -------------------------------------------
            if color_cycle is None:
                color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

            arm_colors = {
                arm: color_cycle[i % len(color_cycle)]
                for i, arm in enumerate(ordered_arms)
            }

            # -------------------------------------------
            # FLATTEN BAR DATA
            # -------------------------------------------
            bar_x_positions = []
            bar_heights = []
            bar_colors = []
            bar_labels = []

            idx = 0
            for arm in ordered_arms:
                for ts_id, auc_val in auc_dict[arm]:
                    bar_x_positions.append(idx)
                    bar_heights.append(auc_val)
                    bar_colors.append(arm_colors[arm])
                    bar_labels.append(remove_alpha(str(ts_id)))
                    idx += 1
                idx += 1

            if not bar_heights:
                logger.info("No AUC values to plot")
                return None




            # Create bar graph
            bars = ax.bar(
                bar_x_positions,
                bar_heights,
                color=bar_colors,
                alpha=bar_alpha,
                edgecolor=bar_edgecolor,
            )

            # X ticks
            if show_axis_labels:
                ax.set_xticks(bar_x_positions)
                ax.set_xticklabels(bar_labels, rotation=75, ha="right", fontsize=8)
            else:
                ax.set_xticks([])
                ax.set_xticklabels([])

            # Labels and title
            y_label = "Normalized AUC" if plot_normalized_auc else "AUC"
            if show_axis_labels:
                ax.set_ylabel(y_label)

            if title:
                ax.set_title(f'{title} - {self.study_id}')

            # Grid handling (respect style)
            if plot_style:
                styles = [plot_style] if isinstance(plot_style, str) else plot_style
                grid_styles = ["grid", "whitegrid", "darkgrid"]
                if any(gs in s for s in styles for gs in grid_styles):
                    ax.grid(True, axis="y")
                    ax.set_axisbelow(True)
            else:
                ax.grid(True, axis="y", alpha=0.3)

            # ---------------------------------------
            # 6. OPTIONAL: Annotate Bars
            # ---------------------------------------
            if show_bar_labels:
                for rect in bars:
                    height = rect.get_height()
                    ax.text(
                        rect.get_x() + rect.get_width() / 2,
                        height,
                        f"{height:.1f}",
                        ha="center",
                        va="bottom",
                        fontsize=8,
                    )

            # ---------------------------------------
            # 7. LEGEND
            # ---------------------------------------
            if show_legend:
                handles = [
                    plt.Line2D([], [], color=arm_colors[a], lw=6)
                    for a in ordered_arms
                ]
                ax.legend(handles, ordered_arms, title="Arms", loc="best")

        # -------------------------------------------
        # 8. QT WIDGET INTEGRATION
        # -------------------------------------------
        if parent_widget:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Match Qt background to matplotlib figure
            fig_facecolor = fig.get_facecolor()
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            # Context menu
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            parent_widget.figure = fig
            parent_widget.canvas_item = canvas
            self.current_auc_canvas = canvas

            layout = parent_widget.layout()
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(layout)

            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(canvas)
            canvas.draw()

        else:
            plt.show()
        return fig, ax
    def plot_percent_tumor_vol_change_bar( self, compute_day: int | None = None, figsize=(12, 6), sort_descending=True,
            control_arms=("control", "vehicle", "placebo"), bar_alpha=0.85, bar_edgecolor="black", show_bar_labels=False,
            title="Tumor Volume Change (%)", color_cycle=None, show_axis_labels: bool = True, plot_normalized_tv_change=False,
            show_legend: bool = True, plot_style=None, parent_widget=None):
        """
        Vertical bar plot of percent tumor volume change per time-series.
        Controls are plotted first, followed by experimental arms.

        Supports matplotlib styles and embedding into a PySide6 widget.
        """

        # -------------------------------------------
        # 1. COLLECT VOLUME CHANGE PER ARM
        # -------------------------------------------
        unique_arms = list(set(self.arm_col))
        vol_change_dict = {}

        for arm in unique_arms:
            ts_ids = self.study_arms_dict[arm]
            vol_change_list = []

            for ts_id in ts_ids:
                ts = self.study_tv_time_dict[ts_id]
                tv_change, normalized_tv_change = ts.compute_percent_change_tumor_volume(
                    compute_day=compute_day
                )

                value = normalized_tv_change if plot_normalized_tv_change else tv_change
                vol_change_list.append((ts_id, value))

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
        # if color_cycle is None:
        #     color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        #
        # arm_colors = {
        #     arm: color_cycle[i % len(color_cycle)]
        #     for i, arm in enumerate(ordered_arms)
        # }

        # # -------------------------------------------
        # # 4. FLATTEN BAR DATA
        # # -------------------------------------------
        # bar_x_positions = []
        # bar_heights = []
        # bar_colors = []
        # bar_labels = []
        #
        # idx = 0
        # for arm in ordered_arms:
        #     for ts_id, tv_change_val in vol_change_dict[arm]:
        #         bar_x_positions.append(idx)
        #         bar_heights.append(tv_change_val)
        #         bar_colors.append(arm_colors[arm])
        #         bar_labels.append(remove_alpha(str(ts_id)))
        #         idx += 1
        #     idx += 1
        #
        # if not bar_heights:
        #     logger.info("No tumor volume change values to plot")
        #     return None

        # -------------------------------------------
        # 5. PLOTTING (STYLE + QT SUPPORT)
        # -------------------------------------------
        fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)

        if not parent_widget and figsize:
            fig.set_size_inches(figsize)

        with style_ctx:

            #------------------
            # Set Arm Colors

            # Get colors from the style (like in plot_auc_with_controls_bar)
            prop_cycle = plt.rcParams['axes.prop_cycle']
            colors = prop_cycle.by_key()['color']
            edge_color = plt.rcParams['axes.edgecolor']
            line_color = plt.rcParams['text.color']

            # Now create color map using style colors
            if color_cycle is None:
                color_cycle = colors

            arm_colors = {
                arm: color_cycle[i % len(color_cycle)]
                for i, arm in enumerate(ordered_arms)
            }

            #---------------------
            # Flatten Bar Data

            bar_x_positions = []
            bar_heights = []
            bar_colors = []
            bar_labels = []

            idx = 0
            for arm in ordered_arms:
                for ts_id, tv_change_val in vol_change_dict[arm]:
                    bar_x_positions.append(idx)
                    bar_heights.append(tv_change_val)
                    bar_colors.append(arm_colors[arm])
                    bar_labels.append(remove_alpha(str(ts_id)))
                    idx += 1
                idx += 1

            if not bar_heights:
                logger.info("No tumor volume change values to plot")
                return None





            bars = ax.bar(
                bar_x_positions,
                bar_heights,
                color=bar_colors,
                alpha=bar_alpha,
                edgecolor=edge_color,
            )

            # X ticks
            if show_axis_labels:
                ax.set_xticks(bar_x_positions)
                ax.set_xticklabels(bar_labels, rotation=75, ha="right", fontsize=8)
            else:
                ax.set_xticks([])
                ax.set_xticklabels([])

            # Labels and title
            y_label = (
                "Normalized Tumor Volume Change (%)"
                if plot_normalized_tv_change
                else "Tumor Volume Change (%)"
            )
            if show_axis_labels:
                ax.set_ylabel(y_label)

            if title:
                ax.set_title(f'{title} - {self.study_id}')

            # Grid handling (respect style)
            if plot_style:
                styles = [plot_style] if isinstance(plot_style, str) else plot_style
                grid_styles = ["grid", "whitegrid", "darkgrid"]
                if any(gs in s for s in styles for gs in grid_styles):
                    ax.grid(True, axis="y")
                    ax.set_axisbelow(True)
            else:
                ax.grid(True, axis="y", alpha=0.3)

            # ---------------------------------------
            # 6. OPTIONAL: Annotate Bars
            # ---------------------------------------
            if show_bar_labels:
                for rect in bars:
                    height = rect.get_height()
                    ax.text(
                        rect.get_x() + rect.get_width() / 2,
                        height,
                        f"{height:.1f}",
                        ha="center",
                        va="bottom",
                        fontsize=8,
                    )

            # ---------------------------------------
            # 7. LEGEND
            # ---------------------------------------
            if show_legend:
                handles = [
                    plt.Line2D([], [], color=arm_colors[a], lw=6)
                    for a in ordered_arms
                ]
                ax.legend(handles, ordered_arms, title="Arms", loc="best")

        # -------------------------------------------
        # 8. QT WIDGET INTEGRATION
        # -------------------------------------------
        if parent_widget:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Match Qt background to matplotlib figure
            fig_facecolor = fig.get_facecolor()
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            parent_widget.figure = fig
            parent_widget.canvas_item = canvas
            self.current_tv_change_canvas = canvas

            layout = parent_widget.layout()
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(layout)

            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(canvas)
            canvas.draw()

        else:
            plt.show()

        return fig, ax
    def plot_vol_change_as_objective_response_bar(self, compute_day: int | None = None, figsize=(12, 6), sort_descending=True,
            control_arms=("control", "vehicle", "placebo"), bar_alpha=0.85, bar_edgecolor="black", show_bar_labels=False,
            title="Objective Response", color_cycle=None, show_axis_labels: bool = True, show_legend: bool = True,
            y_range: list | None = None, plot_style=None, parent_widget=None):
        """
        Bar plot of percent tumor volume change colored by objective response category.
        Supports matplotlib styles and embedding into a PySide6 widget.
        """

        # -------------------------------------------------------
        # 1. Collect volume changes + response codes per arm
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
                tv_change_val, _ = ts.compute_percent_change_tumor_volume(
                    compute_day=compute_day
                )

                response_code = ts.compute_objective_response(compute_day)
                vol_change_list.append((ts_id, tv_change_val))
                resp_code_list.append((ts_id, response_code))

            # Sort by tumor volume change
            vol_change_list.sort(key=lambda x: x[1], reverse=sort_descending)

            # Match response code ordering
            sorted_resp_list = [
                (ts_id, next(r for t, r in resp_code_list if t == ts_id))
                for ts_id, _ in vol_change_list
            ]

            vol_change_dict[arm] = vol_change_list
            response_code_dict[arm] = sorted_resp_list

        # -------------------------------------------------------
        # 2. Arm ordering (controls first)
        # -------------------------------------------------------
        controls = [a for a in unique_arms if a.lower() in control_arms]
        experimental = [a for a in unique_arms if a not in controls]
        ordered_arms = controls + experimental

        # -------------------------------------------------------
        # 3. Flatten bar data + compute arm spans
        # -------------------------------------------------------
        bar_x_positions = []
        bar_heights = []
        bar_colors = []
        bar_labels = []
        arm_ranges = {}

        idx = 0
        for arm in ordered_arms:
            if idx > 0:
                idx += 1  # spacing between arms

            start_idx = idx

            for (ts_id, tv_val), (_, resp_code) in zip(
                    vol_change_dict[arm], response_code_dict[arm]
            ):
                bar_x_positions.append(idx)
                bar_heights.append(tv_val)
                bar_colors.append(self.objective_response_colors[resp_code])
                bar_labels.append(remove_alpha(str(ts_id)))
                idx += 1

            arm_ranges[arm] = (start_idx, idx - 1)

        if not bar_heights:
            logger.info("No tumor volume change values to plot")
            return None

        # -------------------------------------------------------
        # 4. Plotting (STYLE + QT SUPPORT)
        # -------------------------------------------------------
        fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)

        if not parent_widget and figsize:
            fig.set_size_inches(figsize)

        with style_ctx:
            bars = ax.bar(
                bar_x_positions,
                bar_heights,
                color=bar_colors,
                alpha=bar_alpha,
                edgecolor=bar_edgecolor,
            )

            # X ticks
            if show_axis_labels:
                ax.set_xticks(bar_x_positions)
                ax.set_xticklabels(bar_labels, rotation=75, ha="right", fontsize=8)
            else:
                ax.set_xticks([])

            # Labels + title
            if show_axis_labels:
                ax.set_ylabel("Tumor Volume Change (%)")

            if title:
                ax.set_title(f'{title} - {self.study_id}')

            # Grid handling (respect style)
            if plot_style:
                styles = [plot_style] if isinstance(plot_style, str) else plot_style
                grid_styles = ["grid", "whitegrid", "darkgrid"]
                if any(gs in s for s in styles for gs in grid_styles):
                    ax.grid(True, axis="y")
                    ax.set_axisbelow(True)
            else:
                ax.grid(True, axis="y", alpha=0.3)

            # ---------------------------------------------------
            # 5. Optional bar labels
            # ---------------------------------------------------
            if show_bar_labels:
                for rect in bars:
                    h = rect.get_height()
                    ax.text(
                        rect.get_x() + rect.get_width() / 2,
                        h,
                        f"{h:.1f}",
                        ha="center",
                        va="bottom",
                        fontsize=8,
                    )

            # ---------------------------------------------------
            # 6. Legend for objective response
            # ---------------------------------------------------
            if show_legend:
                handles = [
                    plt.Line2D([], [], color=self.objective_response_colors[k], lw=6)
                    for k in ["CR", "PR", "SD", "PD"]
                ]
                labels = [
                    k #self.objective_response_names[k]
                    for k in ["CR", "PR", "SD", "PD"]
                ]
                ax.legend(handles, labels, loc="best")

            # ---------------------------------------------------
            # 7. Y-axis limits
            # ---------------------------------------------------
            if y_range is not None:
                ax.set_ylim(y_range[0], y_range[1])
            else:
                y_range = ax.get_ylim()

            # ---------------------------------------------------
            # 8. Arm labels above bars
            # ---------------------------------------------------
            for arm, (start, end) in arm_ranges.items():
                mid = (start + end) / 2
                ax.text(
                    mid,
                    y_range[1] * 1.02,
                    arm,
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="normal",
                )

            ax.set_ylim(y_range[0], y_range[1] * 1.10)

        # -------------------------------------------------------
        # 9. QT WIDGET INTEGRATION
        # -------------------------------------------------------
        if parent_widget:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            canvas.updateGeometry()

            fig_facecolor = fig.get_facecolor()
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(
                parent_widget.show_context_menu
            )

            parent_widget.figure = fig
            parent_widget.canvas_item = canvas
            self.current_objective_response_canvas = canvas

            layout = parent_widget.layout()
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(layout)

            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(canvas)
            canvas.draw()

        else:
            plt.show()

        return fig, ax
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
            "CR": "#66C2A5",  # teal (best)
            "PR": "#8DA0CB",  # muted blue (partial)
            "SD": "#B8B8B8",  # light gray (stable)
            "PD": "#808080"  # gray (progression)
        }
        self.plot_types = ("Avg_TV_Change_Bar", "TV_Control_Bar", "Objective_Response_Bar",
                           "AUC_with_Control_Bar", "Log2_Fold_Change_w_Error")

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

    # Computation
    def log2fc_ci(meanA, sdA, nA, meanB, sdB, nB, confidence=0.95):
        # Fold change
        fc = meanB / meanA
        log2fc = np.log2(fc)

        # Standard errors using delta method
        SEA = sdA / (meanA * np.sqrt(nA))
        SEB = sdB / (meanB * np.sqrt(nB))

        # Convert to log2 base
        SEA_log2 = SEA / np.log(2)
        SEB_log2 = SEB / np.log(2)

        # Combined SE
        SE_log2fc = np.sqrt(SEA_log2 ** 2 + SEB_log2 ** 2)

        # t-value
        dof = nA + nB - 2
        tval = t.ppf((1 + confidence) / 2, dof)

        # CI
        lower = log2fc - tval * SE_log2fc
        upper = log2fc + tval * SE_log2fc

        return log2fc, lower, upper

    # Visualization Utilities
    def plot_to_widget_by_name(self, plot_name, parent_widget, plot_style = None, **plot_kwargs):
        """
        Call a plotting function by name and render to a widget.

        Args:
            plot_name: String name of the plotting method
            parent_widget: Qt widget to embed the plot
            **plot_kwargs: Any keyword arguments to pass to the plotting function

        Returns:
            Result from the plotting function (typically (fig, ax) tuple)

        Example:
            # Call by string name
            experiment_obj.plot_to_widget_by_name(
                "plot_average_tumor_volume_change_bar",
                graphic_view,
                error_metric="sem"
            )
        """
        # Get the method by name
        plot_function = getattr(self, plot_name, None)

        if plot_function is None:
            raise ValueError(f"Plot function '{plot_name}' not found")

        if not callable(plot_function):
            raise ValueError(f"'{plot_name}' is not a callable method")

        return plot_function(parent_widget=parent_widget, plot_style = plot_style, **plot_kwargs)
    def _create_styled_figure(self, plot_style=None, parent_widget=None):
        """
        Create a matplotlib figure with optional style applied, supporting both standalone and Qt widget modes.

        Args:
            plot_style: Style(s) to apply. Can be:
                       - None: Use default matplotlib style
                       - str: Single style name (e.g., 'seaborn-v0_8', 'ggplot')
                       - list: Multiple styles (e.g., ['science', 'ieee'] for SciencePlots)
            parent_widget: Optional Qt widget to embed the plot. If None, creates standalone figure.

        Returns:
            tuple: (fig, ax, style_context) where:
                - fig: matplotlib Figure object
                - ax: matplotlib Axes object
                - style_context: Context manager for style (use with 'with' statement)

        Usage:
            fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)
            with style_ctx:
                # All plotting code here
                ax.plot(x, y)
                ax.set_title("My Plot")
        """
        # Create appropriate style context
        if plot_style is not None:
            style_context = plt.style.context(plot_style)
        else:
            style_context = nullcontext()

        # Create figure WITHOUT manually entering the context
        if parent_widget:
            # Create Figure object for Qt widget embedding (size controlled by layout)
            fig = Figure()
            ax = fig.add_subplot(111)
        else:
            # Create standalone pyplot figure (will use matplotlib defaults or rcParams)
            fig, ax = plt.subplots()

        if plot_style:
            with plt.style.context(plot_style):
                # Get the colors from the style
                fig_color = plt.rcParams['figure.facecolor']
                axes_color = plt.rcParams['axes.facecolor']
                text_color = plt.rcParams['text.color']

                # Apply them to your figure
                fig.patch.set_facecolor(fig_color)
                ax.set_facecolor(axes_color)
                ax.tick_params(colors=text_color)
                ax.xaxis.label.set_color(text_color)
                ax.yaxis.label.set_color(text_color)
                ax.title.set_color(text_color)
                ax.spines['bottom'].set_color(text_color)
                ax.spines['top'].set_color(text_color)
                ax.spines['left'].set_color(text_color)
                ax.spines['right'].set_color(text_color)

        return fig, ax, style_context

    # Plotting Functions
    def plot_average_tumor_volume_change_bar(self, plot_style = None, control_arms=("control", "vehicle", "placebo"),
            error_metric="std", show_axis_labels=True, compute_day: int | None = None,
            title="Average % Tumor Volume Change by Study", figsize=(10, 6), parent_widget=None):
        """
        Plot the average percent tumor volume change for each study.

        Creates a bar chart showing mean tumor volume changes across studies with error bars.
        Can be embedded in a Qt widget or displayed as a standalone matplotlib figure.

        Args:
            control_arms: Tuple of arm names to exclude (case-insensitive).
            error_metric: Error bar type - "std" for standard deviation or "sem" for standard error.
            show_axis_labels: Whether to display axis labels. Defaults to True.
            compute_day: Optional specific day for computing percent change. Defaults to None (final day).
            title: Plot title. Set to None to hide. Defaults to "Average % Tumor Volume Change by Study".
            figsize: Figure size as (width, height) in inches. Defaults to (10, 6).
            parent_widget: Optional Qt widget to embed the plot. If provided, renders as
                          a FigureCanvas within this widget. If None, creates standalone
                          matplotlib figure. Defaults to None.

        Returns:
            tuple: (fig, ax) - matplotlib Figure and Axes objects for the plot.
                Returns None if no studies have data to plot.

        Side Effects (when parent_widget is provided):
            - Sets self.current_tumor_volume_canvas to FigureCanvas
            - Replaces parent_widget's layout contents
        """
        import numpy as np

        # Sort studies
        study_keys = sorted(self.study_keys)

        study_means = []
        study_errors = []
        study_labels = []

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

        # Check if we have data to plot
        if len(study_means) == 0:
            logger.info("No studies with data to plot")
            return None

        # ---------------- Plotting ----------------
        # Create styled figure
        fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)

        # Apply figsize only for standalone mode
        if not parent_widget and figsize:
            fig.set_size_inches(figsize)

        with style_ctx:
            x = np.arange(len(study_means))

            # Get style colors
            prop_cycle = plt.rcParams['axes.prop_cycle']
            colors = prop_cycle.by_key()['color']
            bar_colors = [colors[i % len(colors)] for i in range(len(study_means))]
            line_color = plt.rcParams['text.color']  # Will be white for dark themes

            # Assign colors to bars (cycling if more bars than colors)
            bar_colors = [colors[i % len(colors)] for i in range(len(study_means))]

            bars = ax.bar(
                x,
                study_means,
                yerr=study_errors,
                color=bar_colors[0],
                ecolor=line_color,  # Error bars match theme
                capsize=5,
            )

            # Add lines between each study
            ax.axhline(0, color=line_color, linewidth=1)

            # Enable grid with style's properties
            # Enable grid with style's properties
            # Enable grid only if 'grid' style is in the plot_style
            if plot_style:
                # Handle both string and list inputs
                if isinstance(plot_style, str):
                    styles = [plot_style]
                elif isinstance(plot_style, list):
                    styles = plot_style
                else:
                    styles = []

                # Check if any style contains 'grid'
                grid_styles = ['grid', 'seaborn-v0_8-whitegrid', 'seaborn-v0_8-darkgrid']
                if any(grid_style in styles for grid_style in grid_styles):
                    ax.grid(True)
                    ax.set_axisbelow(True)

            # Add vertical lines between studies
            for i in range(len(x) - 1):
                line_x = x[i] + 0.5
                ax.axvline(x=line_x, color=line_color, linestyle='-',
                           linewidth=1, alpha=0.5)

            # Axis labels
            if show_axis_labels:
                ax.set_ylabel("% Tumor Volume Change")
                ax.set_xlabel("Study")

            if title:
                ax.set_title(title)

            # Ticks
            ax.set_xticks(x)
            ax.set_xticklabels(study_labels, rotation=45, ha="right")

        # fig.tight_layout()

        # Handle widget integration
        if parent_widget:
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Get matplotlib's figure background color
            fig_facecolor = fig.get_facecolor()

            # Convert RGBA to hex for Qt
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            if plot_style in ['dark_background', 'seaborn-v0_8-dark']:
                fig.patch.set_facecolor(fig.get_facecolor())
                ax.set_facecolor(ax.get_facecolor())

            # Enable right-click menu
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas

            # Store canvas reference
            self.current_tumor_volume_canvas = canvas

            # Clear existing layout
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            # Ensure proper sizing
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Draw the canvas
            canvas.draw()
        else:
            # Show plot in standalone mode
            plt.show()

        return fig, ax
    def plot_tumor_control_ratio_bar(self, plot_style = None, control_arms=("control", "vehicle", "placebo"), error_metric="std", show_axis_labels=True,
            compute_day: int | None = None, title="T/C Ratio (SE) by Study", figsize=(10, 6), parent_widget=None):
        """
        Plot the T/C (Treatment/Control) ratio for each study with standard error.

        Creates a bar chart showing the ratio of mean treatment tumor volume to mean control
        tumor volume, with error bars calculated using the delta method. Can be embedded in
        a Qt widget or displayed as a standalone matplotlib figure.

        Args:
            control_arms: Tuple of arm names to treat as controls (case-insensitive).
            error_metric: Error bar type - currently only "std" supported (uses SE calculation).
            show_axis_labels: Whether to display axis labels. Defaults to True.
            compute_day: Optional specific day for computing ratio. Defaults to None (final day).
            title: Plot title. Set to None to hide. Defaults to "T/C Ratio (SE) by Study".
            figsize: Figure size as (width, height) in inches. Defaults to (10, 6).
            parent_widget: Optional Qt widget to embed the plot. If provided, renders as
                          a FigureCanvas within this widget. If None, creates standalone
                          matplotlib figure. Defaults to None.

        Returns:
            tuple: (fig, ax) - matplotlib Figure and Axes objects for the plot.
                Returns None if no studies have data to plot.

        Side Effects (when parent_widget is provided):
            - Sets self.current_tumor_control_ratio_canvas to FigureCanvas
            - Replaces parent_widget's layout contents
        """

        # Sort studies
        study_keys = sorted(self.study_keys)

        study_means = []
        study_errors = []
        study_labels = []
        study_colors = []

        # Build bar data
        for idx, study in enumerate(study_keys):

            study_obj = self.experiment_study_dict[study]

            arms = study_obj.unique_arms
            arms_to_plot = [arm for arm in arms if arm.lower() not in control_arms]
            trtarms = [arm for arm in arms if arm.lower() not in control_arms]
            ctrl_arms = [arm for arm in arms if arm.lower() in control_arms]

            all_changes = []
            treatment = []
            controls = []

            # Grab relative tumor volume for treatments
            for arm in trtarms:
                trt_arm_id_list = study_obj.study_arms_dict[arm]

                for ts_id in trt_arm_id_list:
                    tv_data_obj = study_obj.study_tv_time_dict[ts_id]
                    compute_day_val = compute_day if compute_day is not None else tv_data_obj.time_day[-1]
                    compute_day_index = tv_data_obj.get_compute_day_index(tv_data_obj.time_day, compute_day_val)
                    relative_tumor_volume = tv_data_obj.tumor_volume[compute_day_index] / tv_data_obj.tumor_volume[0]
                    treatment.append(relative_tumor_volume)

            # Grab relative tumor volume for controls
            for arm in ctrl_arms:
                ctrl_arm_id_list = study_obj.study_arms_dict[arm]

                for ts_id in ctrl_arm_id_list:
                    tv_data_obj = study_obj.study_tv_time_dict[ts_id]
                    compute_day_val = compute_day if compute_day is not None else tv_data_obj.time_day[-1]
                    compute_day_index = tv_data_obj.get_compute_day_index(tv_data_obj.time_day, compute_day_val)
                    relative_tumor_volume = tv_data_obj.tumor_volume[compute_day_index] / tv_data_obj.tumor_volume[0]
                    controls.append(relative_tumor_volume)

            # Calculate means
            t_mean = np.mean(treatment)
            t_size = np.size(treatment, axis=0)
            t_var = np.var(treatment)
            c_mean = np.mean(controls)
            c_size = np.size(controls, axis=0)
            c_var = np.var(controls)

            # Compute ratio and standard error
            tc_ratio = t_mean / c_mean
            s_err = tc_ratio * np.sqrt(
                (t_var / (t_mean ** 2 * t_size)) +
                (c_var / (c_mean ** 2 * c_size)))

            if len(treatment) == 0:
                continue

            study_means.append(tc_ratio)
            study_errors.append(s_err)
            study_labels.append(study)
            study_colors.append('#808080')

        # Check if we have data to plot
        if len(study_means) == 0:
            logger.info("No studies with data to plot")
            return None

        # ---------------- Plotting ----------------
        # Create styled figure
        fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)

        # Apply figsize only for standalone mode
        if not parent_widget and figsize:
            fig.set_size_inches(figsize)

        with style_ctx:
            x = np.arange(len(study_means))

            # Get style colors
            prop_cycle = plt.rcParams['axes.prop_cycle']
            colors = prop_cycle.by_key()['color']
            bar_colors = [colors[i % len(colors)] for i in range(len(study_means))]
            line_color = plt.rcParams['text.color']  # Will be white for dark themes

            # Assign colors to bars (cycling if more bars than colors)
            bar_colors = [colors[i % len(colors)] for i in range(len(study_means))]

            bars = ax.bar(
                x,
                study_means,
                yerr=study_errors,
                color=bar_colors[0],
                ecolor=line_color,  # Error bars match theme
                capsize=5,
            )


            # Add lines between each study
            ax.axhline(0, color=line_color, linewidth=1)


            # Enable grid with style's properties
            # Enable grid only if 'grid' style is in the plot_style
            if plot_style:
                # Handle both string and list inputs
                if isinstance(plot_style, str):
                    styles = [plot_style]
                elif isinstance(plot_style, list):
                    styles = plot_style
                else:
                    styles = []

                # Check if any style contains 'grid'
                grid_styles = ['grid', 'seaborn-v0_8-whitegrid', 'seaborn-v0_8-darkgrid']
                if any(grid_style in styles for grid_style in grid_styles):
                    ax.grid(True)
                    ax.set_axisbelow(True)






            # Add vertical lines between studies
            for i in range(len(x) - 1):
                line_x = x[i] + 0.5
                ax.axvline(x=line_x, color=line_color, linestyle='-',
                           linewidth=1, alpha=0.5)

            # Axis labels
            if show_axis_labels:
                ax.set_ylabel("T/C Ratio (SE)")
                ax.set_xlabel("Study")

            if title:
                ax.set_title(title)

            # Ticks
            ax.set_xticks(x)
            ax.set_xticklabels(study_labels, rotation=45, ha="right")

        # fig.tight_layout()

        # Handle widget integration
        if parent_widget:
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Get matplotlib's figure background color
            fig_facecolor = fig.get_facecolor()

            # Convert RGBA to hex for Qt
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            if plot_style in ['dark_background', 'seaborn-v0_8-dark']:
                fig.patch.set_facecolor(fig.get_facecolor())
                ax.set_facecolor(ax.get_facecolor())

            # Enable right-click menu
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas

            # Store canvas reference
            self.current_tumor_control_ratio_canvas = canvas

            # Clear existing layout
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            # Ensure proper sizing
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Draw the canvas
            canvas.draw()
        else:
            # Show plot in standalone mode
            plt.show()

        return fig, ax
    def proportion_in_objective_response_classification_bar(self, plot_style = None, control_arms=("control", "vehicle", "placebo"),
            show_legend=False, show_axis_labels=False, compute_day: int | None = None,
            title="Objective Response Distribution by Study", figsize=(10, 6), parent_widget=None,
            objective_response_color_dict:dict[str,str]|None = None):
        """
        Create a stacked 100% bar plot showing objective response proportions
        for each study, with count and percentage inside each bar segment.

        Creates a stacked bar chart showing the distribution of objective responses (CR, PR, SD, PD)
        across studies. Each bar segment displays both the count and percentage. Can be embedded in
        a Qt widget or displayed as a standalone matplotlib figure.

        Args:
            control_arms: Tuple of arm names to exclude (case-insensitive).
            show_legend: Whether to display the legend. Defaults to True.
            show_axis_labels: Whether to display axis labels. Defaults to False.
            compute_day: Optional specific day for computing objective response. Defaults to None (final day).
            title: Plot title. Set to None to hide. Defaults to "Objective Response Distribution by Study".
            figsize: Figure size as (width, height) in inches. Defaults to (10, 6).
            parent_widget: Optional Qt widget to embed the plot. If provided, renders as
                          a FigureCanvas within this widget. If None, creates standalone
                          matplotlib figure. Defaults to None.

        Returns:
            tuple: (fig, ax) - matplotlib Figure and Axes objects for the plot.

        Side Effects (when parent_widget is provided):
            - Sets self.current_objective_response_canvas to FigureCanvas
            - Replaces parent_widget's layout contents

        Notes:
            - Response order: CR (Complete Response), PR (Partial Response),
              SD (Stable Disease), PD (Progressive Disease)
            - Each segment shows "count (percentage%)"
            - Colors are pulled from self.objective_response_colors
        """

        OR_ORDER = ["CR", "PR", "SD", "PD"]
        if objective_response_color_dict is None:
            OR_COLORS = [self.objective_response_colors[o] for o in OR_ORDER]
        else:
            OR_COLORS = [objective_response_color_dict[o] for o in OR_ORDER]

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
        # Create styled figure
        fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)

        # Apply figsize only for standalone mode
        if not parent_widget and figsize:
            fig.set_size_inches(figsize)

        with style_ctx:


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
                        label_text = f"{or_code}\n\n{count} ({pct:.0f}{"%"})"

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

        # fig.tight_layout()

        # Handle widget integration
        if parent_widget:
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Get matplotlib's figure background color
            fig_facecolor = fig.get_facecolor()

            # Convert RGBA to hex for Qt
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            if plot_style in ['dark_background', 'seaborn-v0_8-dark']:
                fig.patch.set_facecolor(fig.get_facecolor())
                ax.set_facecolor(ax.get_facecolor())

            # Enable right-click menu
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas

            # Store canvas reference
            self.current_objective_response_canvas = canvas

            # Clear existing layout
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            # Ensure proper sizing
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Draw the canvas
            canvas.draw()
        else:
            # Show plot in standalone mode
            plt.show()

        return fig, ax
    def plot_auc_with_controls_bar(self, plot_style = None, control_arms=("control", "vehicle", "placebo"), error_metric="sem",
            show_legend=True, show_axis_labels=False, compute_day: int | None = None, title="Average AUC by Study",
            figsize=(12, 6), parent_widget=None):
        """
        Plot mean AUC for each study with control vs treatment bars.
        If parent_widget is provided, embeds the plot in a Qt widget
        using a FigureCanvas. Otherwise uses matplotlib standalone mode.
        """

        # ---------------------------------------------------------
        #  Handle Qt vs standalone
        # ---------------------------------------------------------

        study_keys = sorted(self.study_keys)

        study_labels = []
        control_means = []
        control_errors = []
        treatment_means = []
        treatment_errors = []

        ctrl_color = "#6C757D"
        trt_color = "#1F77B4"

        # ---------------------------------------------------------
        #   COLLECT DATA
        # ---------------------------------------------------------
        for study in study_keys:
            study_obj = self.experiment_study_dict[study]
            arms = study_obj.unique_arms

            control_list = [a for a in arms if a.lower() in control_arms]
            treatment_list = [a for a in arms if a.lower() not in control_arms]

            ctrl_vals = []
            trt_vals = []

            # Controls
            for arm in control_list:
                for ts_id in study_obj.study_arms_dict[arm]:
                    tv = study_obj.study_tv_time_dict[ts_id]
                    auc = tv.compute_auc(compute_day)
                    ctrl_vals.append(auc)

            # Treatments
            for arm in treatment_list:
                for ts_id in study_obj.study_arms_dict[arm]:
                    tv = study_obj.study_tv_time_dict[ts_id]
                    auc = tv.compute_auc(compute_day)
                    trt_vals.append(auc)

            if len(ctrl_vals) == 0 and len(trt_vals) == 0:
                continue

            study_labels.append(study)

            # Error helper
            def _err(vals):
                if error_metric == "sem":
                    return np.nanstd(vals) / np.sqrt(len(vals))
                return np.nanstd(vals)

            # Control
            control_means.append(np.nanmean(ctrl_vals) if len(ctrl_vals) > 0 else np.nan)
            control_errors.append(_err(ctrl_vals) if len(ctrl_vals) > 0 else 0)

            # Treatment
            treatment_means.append(np.nanmean(trt_vals) if len(trt_vals) > 0 else np.nan)
            treatment_errors.append(_err(trt_vals) if len(trt_vals) > 0 else 0)

        # ---------------------------------------------------------
        #   NO DATA TO PLOT
        # ---------------------------------------------------------
        if len(study_labels) == 0:
            logger.info("No AUC data available to plot")
            return None

        # ---------------------------------------------------------
        #   CREATE FIGURE
        # ---------------------------------------------------------
        # Create styled figure
        fig, ax, style_ctx = self._create_styled_figure(plot_style, parent_widget)

        # Apply figsize only for standalone mode
        if not parent_widget and figsize:
            fig.set_size_inches(figsize)



        # ---------------------------------------------------------
        #   PLOT
        # ---------------------------------------------------------
        with style_ctx:
            n_studies = len(study_labels)
            x = np.arange(n_studies)
            width = 0.35

            # Get colors from the style
            prop_cycle = plt.rcParams['axes.prop_cycle']
            colors = prop_cycle.by_key()['color']
            edge_color = plt.rcParams['axes.edgecolor']
            line_color = plt.rcParams['text.color']

            # Use first two colors from the cycle for control/treatment
            ctrl_color = colors[0]
            trt_color = colors[1]

            ax.bar(
                x - width / 2,
                control_means,
                width=width,
                yerr=control_errors,
                color=ctrl_color,
                edgecolor=edge_color,
                ecolor=line_color,  # Error bar color
                capsize=5,
                label="Control"
            )

            ax.bar(
                x + width / 2,
                treatment_means,
                width=width,
                yerr=treatment_errors,
                color=trt_color,
                edgecolor=edge_color,
                ecolor=line_color,  # Error bar color
                capsize=5,
                label="Treatment"
            )

            ax.axhline(0, color=line_color, linewidth=1)

            # Enable grid with style's properties
            # Enable grid only if 'grid' style is in the plot_style
            if plot_style:
                # Handle both string and list inputs
                if isinstance(plot_style, str):
                    styles = [plot_style]
                elif isinstance(plot_style, list):
                    styles = plot_style
                else:
                    styles = []

                # Check if any style contains 'grid'
                grid_styles = ['grid', 'seaborn-v0_8-whitegrid', 'seaborn-v0_8-darkgrid']
                if any(grid_style in styles for grid_style in grid_styles):
                    ax.grid(True)
                    ax.set_axisbelow(True)

            # Labels
            y_label_title = f"AUC ({error_metric.upper()})"
            if compute_day is not None:
                y_label_title = f"AUC at Day {compute_day} ({error_metric.upper()})"
            ax.set_ylabel(y_label_title)

            if show_axis_labels:
                ax.set_xlabel("Study")

            if title:
                ax.set_title(title)

            ax.set_xticks(x)
            ax.set_xticklabels(study_labels, rotation=45, ha="right")

            if show_legend:
                ax.legend(loc="upper right", frameon=True, framealpha=0.8)


        # ---------------------------------------------------------
        #   EMBED IN QT (IF REQUESTED)
        # ---------------------------------------------------------
        if parent_widget:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Get matplotlib's figure background color
            fig_facecolor = fig.get_facecolor()

            # Convert RGBA to hex for Qt
            hex_color = mcolors.to_hex(fig_facecolor)
            canvas.setStyleSheet(f"background-color: {hex_color};")

            if plot_style in ['dark_background', 'seaborn-v0_8-dark']:
                fig.patch.set_facecolor(fig.get_facecolor())
                ax.set_facecolor(ax.get_facecolor())


            # Enable right-click menu
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas

            # Store reference so you can save the figure later
            self.current_auc_canvas = canvas

            # Clear the existing layout
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            canvas.draw()
        else:
            plt.show()

        return fig, ax
    def plot_log2fc_points(self, plot_style = None, control_arms=("control", "vehicle", "placebo"), show_legend=True, show_axis_labels=True,
            compute_day=None, title="Log2 Change (Control vs Treatment)", figsize=(12, 6), parent_widget=None):
        """
        Plot log2-fold change at compute_day for control vs treatment arms.
        Supports Qt embedding via parent_widget or standalone matplotlib display.
        """

        # ----- helper: find index for compute_day -----
        def get_index(days, compute_day):
            if compute_day is None:
                return len(days) - 1
            days = list(days)
            if compute_day >= days[-1]:
                return len(days) - 1
            for i, d in enumerate(days):
                if compute_day <= d:
                    return i
            return len(days) - 1

        study_keys = sorted(self.study_keys)

        # Create figure
        if parent_widget:
            fig = Figure(figsize=figsize)
            ax = fig.add_subplot(111)
        else:
            fig, ax = plt.subplots(figsize=figsize)

        x_positions = []
        x_labels = []
        x_counter = 0

        ctrl_color = '#808080'  # gray
        trt_color = '#1f77b4'  # blue

        for study_idx, study in enumerate(study_keys):
            study_obj = self.experiment_study_dict[study]
            arms = study_obj.unique_arms

            control_list = [a for a in arms if a.lower() in control_arms]
            treatment_list = [a for a in arms if a.lower() not in control_arms]

            ctrl_vals = []
            trt_vals = []
            ctrl_vals_raw = []
            trt_vals_raw = []

            # ---- collect controls ----
            for arm in control_list:
                for ts_id in study_obj.study_arms_dict[arm]:
                    tv = study_obj.study_tv_time_dict[ts_id]
                    idx = get_index(tv.time_day, compute_day)
                    v0 = tv.tumor_volume[0]
                    v_end = tv.tumor_volume[idx]
                    if v0 > 0:
                        ctrl_vals.append(np.log2(v_end / v0))
                        ctrl_vals_raw.append(v_end / v0)

            # ---- collect treatment ----
            for arm in treatment_list:
                for ts_id in study_obj.study_arms_dict[arm]:
                    tv = study_obj.study_tv_time_dict[ts_id]
                    idx = get_index(tv.time_day, compute_day)
                    v0 = tv.tumor_volume[0]
                    v_end = tv.tumor_volume[idx]
                    if v0 > 0:
                        trt_vals.append(np.log2(v_end / v0))
                        trt_vals_raw.append(v_end / v0)

            if len(ctrl_vals) == 0 or len(trt_vals) == 0:
                continue

            def sem(x):
                return np.std(x, ddof=1) / np.sqrt(len(x)) if len(x) > 1 else 0.0

            # t-test
            t_stat, p_value = ttest_ind(trt_vals_raw, ctrl_vals_raw, equal_var=False)
            logger.info(f"Study={study}, t-stat={t_stat}, p-value={p_value}")

            ctrl_mean = np.mean(ctrl_vals)
            trt_mean = np.mean(trt_vals)
            ctrl_sem = sem(ctrl_vals)
            trt_sem = sem(trt_vals)

            # Plot positions
            ctrl_x = x_counter
            trt_x = x_counter + 1
            center_x = (ctrl_x + trt_x) / 2

            x_positions.append(center_x)
            x_labels.append(study)

            # Plot control
            ax.errorbar(
                [ctrl_x], [ctrl_mean],
                yerr=[ctrl_sem],
                fmt="o",
                markersize=10,
                capsize=5,
                linewidth=2,
                color=ctrl_color,
                label='Control' if study_idx == 0 else ''
            )

            # Plot treatment
            ax.errorbar(
                [trt_x], [trt_mean],
                yerr=[trt_sem],
                fmt="o",
                markersize=10,
                capsize=5,
                linewidth=2,
                color=trt_color,
                label='Treatment' if study_idx == 0 else ''
            )

            x_counter += 3  # spacing

        # Vertical separators
        for i in range(len(x_positions) - 1):
            line_x = x_positions[i] + 1.5
            ax.axvline(x=line_x, color='black', linestyle='-', linewidth=1, alpha=0.5)

        # Formatting
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=45, ha="right")

        if show_axis_labels:
            ax.set_ylabel("log2(Change)")

        if title:
            ax.set_title(title)

        if show_legend:
            ax.legend(loc='best')

        #fig.tight_layout()

        # ---------------------------------------------------------
        #   EMBED IN QT (IF REQUESTED)
        # ---------------------------------------------------------
        if parent_widget:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()
            canvas.setStyleSheet("background-color: white;")

            # Enable right-click menu
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas

            # Store reference
            self.current_log2fc_canvas = canvas

            layout = parent_widget.layout()
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(layout)

            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(canvas)

            canvas.draw()

        else:
            plt.show()

        return fig, ax

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
        self.unique_experiments:list[str]|None
        self.num_experiments:int|none
        self.unique_matched_controls:list|None
        self.num_matched_controls:int|None
        self.num_unmatched:int|None

        # Create time series dictionary
        self.tumor_vol_time_series_dict:dict[str:TumorVolumeTimeSeriesClass]|None = None
        self.tumor_vol_study_dict:dict[str:TumorVolumeStudyClass|None] = None
        self.tumor_vol_experiment_dict:dict[str,TumorVolumeExperimentClass|None] = None

    # File loading and saving
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

    # XML Support
    # Helper: safe text getter
    def _text_or_none(self, elem):
        return elem.text if elem is not None else None
    def xml_to_dataframe(self, xml_path: str) -> pd.DataFrame:
        """
        Parse an XML file following the XSD structure and return a DataFrame
        with one row per Measurement. Columns include:
          contributor, contributor_id, disease_type, disease_id,
          experiment_id, experiment_description, study_id, study_name,
          arm_id, arm_name, matched_controls,
          curve_id, subject_id, tumor_id, body_weight, age, sex,
          time, time_unit, volume, volume_unit, matched_control_refs (semicolon separated)
        """
        tree = ET.parse(xml_path)
        root = tree.getroot()

        rows = []

        # Build dictionaries for contributor/disease names by id
        contributors = {}
        for contrib in root.findall(".//Contributors/Contributor"):
            cid = contrib.get("id")
            name = _text_or_none(contrib.find("Name"))
            contributors[cid] = {"name": name}
            # collect disease types
            dtypes = {}
            dt_parent = contrib.find("DiseaseTypes")
            if dt_parent is not None:
                for dt in dt_parent.findall("DiseaseType"):
                    dt_id = dt.get("id")
                    dt_name = dt.text
                    dtypes[dt_id] = dt_name
            contributors[cid]["diseases"] = dtypes

        # Iterate experiments
        for exp in root.findall(".//Experiments/Experiment"):
            exp_id = exp.get("id")
            contrib_ref = exp.findtext("ContributorRef")
            disease_ref = exp.findtext("DiseaseTypeRef")
            description = _text_or_none(exp.find("Description"))

            for study in exp.findall(".//Study"):
                study_id = study.get("id")
                study_name = _text_or_none(study.find("Name"))

                for arm in study.findall(".//Arm"):
                    arm_id = arm.get("id")
                    arm_name = _text_or_none(arm.find("Name"))
                    matched_controls_text = _text_or_none(arm.find("MatchedControls"))
                    matched_controls = None
                    if matched_controls_text is not None:
                        matched_controls = matched_controls_text.lower() in ("true", "1", "yes")

                    for curve in arm.findall(".//TumorVolumeCurve"):
                        curve_id = curve.get("id")
                        subject_id = _text_or_none(curve.find("SubjectID"))
                        tumor_id = _text_or_none(curve.find("TumorID"))

                        # Demographics
                        body_weight = None
                        age = None
                        sex = None
                        dem = curve.find("Demographics")
                        if dem is not None:
                            bw = dem.find("BodyWeight")
                            if bw is not None and bw.text:
                                body_weight = bw.text
                            a = dem.find("Age")
                            if a is not None and a.text:
                                age = a.text
                            s = dem.find("Sex")
                            if s is not None:
                                sex = s.text

                        # matched control refs
                        matched_refs = []
                        mcrefs = curve.find("MatchedControlRefs")
                        if mcrefs is not None:
                            for cref in mcrefs.findall("CurveRef"):
                                matched_refs.append(cref.text)

                        # Measurements: one row per measurement
                        for meas in curve.findall(".//Measurement"):
                            time_elem = meas.find("Time")
                            volume_elem = meas.find("Volume")
                            time_val = _text_or_none(time_elem)
                            time_unit = time_elem.get("unit") if time_elem is not None else None
                            vol_val = _text_or_none(volume_elem)
                            vol_unit = volume_elem.get("unit") if volume_elem is not None else None

                            row = {
                                "contributor_id": contrib_ref,
                                "contributor": contributors.get(contrib_ref, {}).get("name"),
                                "disease_id": disease_ref,
                                "disease_type": contributors.get(contrib_ref, {}).get("diseases", {}).get(disease_ref),
                                "experiment_id": exp_id,
                                "experiment_description": description,
                                "study_id": study_id,
                                "study_name": study_name,
                                "arm_id": arm_id,
                                "arm_name": arm_name,
                                "matched_controls": matched_controls,
                                "curve_id": curve_id,
                                "subject_id": subject_id,
                                "tumor_id": tumor_id,
                                "body_weight": body_weight,
                                "age": age,
                                "sex": sex,
                                "time": time_val,
                                "time_unit": time_unit,
                                "volume": vol_val,
                                "volume_unit": vol_unit,
                                "matched_control_refs": ";".join(matched_refs) if matched_refs else None
                            }
                            rows.append(row)

        df = pd.DataFrame(rows)
        return df
    def _ensure_id(self, prefix: str, maybe_id):
        """Return existing id or create a stable id if missing"""
        if maybe_id:
            return str(maybe_id)
        return f"{prefix}_{uuid.uuid4().hex[:8]}"
    def dataframe_to_xml(self, df: pd.DataFrame, file_path: str):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")

        root = ET.Element("TumorVolumeData")

        # ----------------------------
        # Contributors Section
        # ----------------------------
        contributors_el = ET.SubElement(root, "Contributors")

        for (contributor, disease), d1 in df.groupby(["contributor", "disease_type"], dropna=False):
            cont_el = ET.SubElement(contributors_el, "Contributor", name=str(contributor))

            disease_el = ET.SubElement(cont_el, "Disease", type=str(disease))

            # unique experiment refs
            experiments = sorted(d1["experiment"].dropna().unique())
            for exp_name in experiments:
                ET.SubElement(disease_el, "ExperimentRef").text = str(exp_name)

        # ----------------------------
        # Experiments Section
        # ----------------------------
        experiments_el = ET.SubElement(root, "Experiments")

        for exp_name, d_exp in df.groupby("experiment", dropna=False):
            exp_el = ET.SubElement(experiments_el, "Experiment", name=str(exp_name))

            for study_name, d_study in d_exp.groupby("study", dropna=False):
                study_el = ET.SubElement(exp_el, "Study", name=str(study_name))

                for arm_name, d_arm in d_study.groupby("arms", dropna=False):
                    arm_el = ET.SubElement(study_el, "Arm", name=str(arm_name))

                    for tumor_name, d_tumor in d_arm.groupby("tumor", dropna=False):
                        tumor_el = ET.SubElement(arm_el, "Tumor", name=str(tumor_name))

                        for animal_id, d_id in d_tumor.groupby("id", dropna=False):
                            id_el = ET.SubElement(tumor_el, "ID", name=str(animal_id))

                            # timepoints under ID
                            for _, row in d_id.iterrows():
                                t_el = ET.SubElement(id_el, "Timepoint", time=str(row["times"]))

                                ET.SubElement(t_el, "Volume").text = str(row.get("volume", ""))
                                ET.SubElement(t_el, "BodyWeight").text = str(row.get("body_weight", ""))

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
    def validate_xml(self, xml_path: str, xsd_path: str) -> bool:
        """
        Optional: validate using lxml if available. Returns True if valid, False otherwise.
        Prints errors if validation fails or lxml not installed.
        """
        try:
            from lxml import etree
        except Exception:
            logger.info("lxml is not installed. Install it (pip install lxml) to perform XSD validation.")
            return False

        xml_doc = etree.parse(xml_path)
        with open(xsd_path, "rb") as fh:
            schema_doc = etree.parse(fh)
        schema = etree.XMLSchema(schema_doc)
        valid = schema.validate(xml_doc)
        if not valid:
            logger.info("Validation errors:")
            for err in schema.error_log:
                logger.info(err.message)
        return valid
    def dataframe_to_csv(self, df: pd.DataFrame, csv_path: str, index=False):
        """
        Write DataFrame to CSV. Example columns are the ones produced by xml_to_dataframe.
        """
        os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)
        df.to_csv(csv_path, index=index)

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

        # Store Summary
        self.unique_experiments = list(tumor_vol_experiment_dict.keys())
        self.unique_experiments.sort()
        self.num_experiments = len(self.unique_experiments)

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
    established_test = True

    # test data
    test_data_tmz = Path("public_data") / "consensus" / "PVA_with_study_group.tv.csv"

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

    # Example  13: Objective Response by Study
    if established_test:
        experiments = tvd_obj.unique_experiments
        experiments.sort()
        for experiment in experiments:
            tvd_experiment_obj = tvd_obj.tumor_vol_experiment_dict[experiment]
            tvd_experiment_obj.proportion_in_objective_response_classification_bar()

    # Example  14: Plot AUC average with controls
    if established_test:
        experiments = tvd_obj.unique_experiments
        experiments.sort()
        compute_day = None
        title = 'Average AUC by Study'
        if compute_day is not None:
            title = f'Average AUC by Study ({compute_day})'
        for experiment in experiments:
            tvd_experiment_obj = tvd_obj.tumor_vol_experiment_dict[experiment]
            tvd_experiment_obj.plot_auc_with_controls_bar(compute_day=compute_day, title=title)

    # Example  15: plot_log2fc_points
    if established_test:
        experiments = tvd_obj.unique_experiments
        experiments.sort()
        compute_day = None
        title = 'Average AUC by Study'
        if compute_day is not None:
            title = f'Average AUC by Study ({compute_day})'
        for experiment in experiments:
            tvd_experiment_obj = tvd_obj.tumor_vol_experiment_dict[experiment]
            tvd_experiment_obj.plot_log2fc_points(compute_day=compute_day, title=title)

    # Example  16: Tumor volume ratio across experiment
    if established_test:
        experiments = tvd_obj.unique_experiments
        experiments.sort()
        for experiment in experiments:
            tvd_experiment_obj = tvd_obj.tumor_vol_experiment_dict[experiment]
            tvd_experiment_obj.plot_tumor_control_ratio_bar()

if __name__ == '__main__':
    main()