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
import logging
import os
import re
from pathlib import Path

# Data
import pandas as pd
import numpy as np
from typing import Optional

from pkg_resources import non_empty_lines

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
class tumorVolumeTimeSeriesClass():
    def __init__(self, time_day:Optional[np.ndarray], tumor_volume:Optional[np.ndarray],
                 tumor_weigth:Optional[np.ndarray]=None, contributor:str|None = None, arm:str|None = None,
                 study_group:str|None = None, study:str|None = None, pdx_id:str|None = None,
                 tumor:str|None=None, disease_type:str|None=None, matched_controls:str|None=None):

        # Class variables
        # Tumor volume time series variables
        self.time_day:Optional[np.ndarray] = time_day.copy()
        self.tumor_volume:Optional[np.ndarray] = tumor_volume.copy()
        if tumor_weigth is not None:
            self.tumor_weight:Optional[np.ndarray] = tumor_weigth.copy()

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
    def write_time_series(self):
        pass

    # Class functions
    def __str__(self):
        pdx_id = 'Not Set'
        if self.pdx_id is not None:
            pdx_id = self.pdx_id
        class_str = f'Tumor Volume time Series: num points = {self.num_points}, pdx_id = {pdx_id}'
        return class_str
class tumorVolumeDataClass():
    # Load, analyze, sumarrize, and plot tumor volume data
    def __init__(self):
        # Set up logger
        self.logger = logging.getLogger(__name__)

        # tumor volume
        self.tumor_volume_data_fn:str|None = None

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
        self.tumor_vol_time_series_dict:dict[str:]

    # File loading
    def load_tmz_csv(self, fn):
        try:
            df = pd.read_csv(fn)
            self.tmz_data_df = df
            self.tmz_data_fn = fn
        except FileNotFoundError:
            logger.info(f'Could not load the cnv file: {fn}')
            return

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

    # Create time series dictionary
    def create_time_series_dict(self):
        # Preare data structure to analyze and plot individual time series
        if self.unique_pdx_ids is None:
            logger.info('Load data before creating time_series dictionary')
            return

        # Loop through pdx ids
        df = self.tmz_data_df
        for pdx in self.unique_pdx_ids:
            # Time series
            time_day = np.arry(df.loc[df['id'] == pdx, 'times'].values)
            tumor_volume = np.arry(df.loc[df['id'] == pdx, 'volume'].values)
            tumor_weight = np.arry(df.loc[df['id'] == pdx, 'body_weight'].values)

            # Study variables
            contributor = df[df['ID'] == pdx]['contributor'].iloc[0]
            arm = df[df['ID'] == pdx]['contributor'].iloc[0]
            study_group = df[df['ID'] == pdx]['stud_group'].iloc[0]
            study = df[df['ID'] == pdx]['study'].iloc[0]
            pdx_id = df[df['ID'] == pdx]['id'].iloc[0]
            tumor = df[df['ID'] == pdx]['tumor'].iloc[0]
            disease_type = df[df['ID'] == pdx]['disease_type'].iloc[0]
            matched_controls = df[df['ID'] == pdx]['matched_controls'].iloc[0]

            # Build and save time series object
            tv_time_series_obj = tumorVolumeTimeSeriesClass(time_day, tumor_volume, tumor_weight,
                contributor, arm, study_group, study, pdx_id, tumor, disease_type, matched_controls)
            self.tumor_vol_time_series_dict[pdx] = tv_time_series_obj

    # Summarizing data
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

        #Supplemental variables
        unmatched_str = self.unmatched_control_entry
        unique_matched_controls =  unique(self.tmz_data_df['matched_controls'])
        self.unique_matched_controls = [entry for entry in unique_matched_controls if entry.lower() != unmatched_str]
        self.num_matched_controls = len(self.unique_matched_controls)
        self.num_unmatched = len(unique_matched_controls) - self.num_matched_controls

        # sort lists
        summary_lists = [ self.unique_contributors, self.unique_arms, self.unique_studies,
                          self.unique_pdx_ids, self.unique_pdxs, self.unique_disease_types,
                          self.unique_matched_controls]
        for slist in summary_lists:
            slist.sort(key = lambda x: pad_all_numbers(x, min_width=4))

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

    # Class functions
    def __str__(self):
        number_of_points = 0
        file_str = 'Not Set'
        if self.tmz_data_fn is not None:
            file_str = self.tmz_data_fn
            number_of_points = self.num_of_data_points
        return f'Tumor Volume Data Class, num of data points = {number_of_points}, file: {file_str} '
# Test application
def main():
    # test data
    test_data_tmz = Path("public_data") / "consensus" / "PVA_with_study_group.csv"

    # Example 1
    tvd_obj = tumorVolumeDataClass()
    tvd_obj.load_tmz_csv(test_data_tmz)
    tvd_obj.write_file_summary_text()

if __name__ == '__main__':
    main()