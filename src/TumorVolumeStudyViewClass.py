# Code for displaying a tumor experiment pllots

#TODO: Semantic color coding of objective response with gray and blue tones
#TODO: Check with a dataset that contains multuple experiments

# Set up a module-level logger
import logging
logger = logging.getLogger(__name__)

# Extend Existing Class
from FigureGraphicsViewClass import FigureGraphicsView

# Import

# Computing
import numpy as np
import re

# Plotting
import matplotlib as mpl
import matplotlib.pyplot as plt

# Science Plot Styles
import scienceplots #Needed

# Interface
from PySide6.QtWidgets import QMainWindow, QGraphicsView, QSizePolicy, QGroupBox, QScrollArea
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QColor, QPixmap, QIcon

# Tumor volume classes
from TumorVolumeClass import TumorVolumeDataClass

# GUI Interface
from TumorVolumeStudyView import Ui_MainWindow

# Utilities
def set_layout_visible(layout, visible: bool):
    """
    Recursively set visibility for all widgets in a layout and its nested layouts.

    Args:
        layout: QLayout object to process
        visible: Boolean indicating whether to show (True) or hide (False) widgets
    """
    for i in range(layout.count()):
        item = layout.itemAt(i)

        # Check if the item is a widget
        widget = item.widget()
        if widget:
            widget.setVisible(visible)

        # Check if the item is a nested layout
        nested_layout = item.layout()
        if nested_layout:
            # Recursively process the nested layout
            set_layout_visible(nested_layout, visible)
def latex_available():
    try:
        mpl.rcParams["text.usetex"] = True
        import matplotlib.pyplot as plt
        plt.figure()
        plt.text(0.5, 0.5, r"$\alpha$")
        plt.close()
        return True
    except Exception:
        return False
    finally:
        mpl.rcParams["text.usetex"] = False

# GUI Class
class TumorVolumeStudyWindow(QMainWindow):
    # Intitialize
    def __init__(self, tv_data_obj:TumorVolumeDataClass , parent=None):
        super().__init__(parent)

        # 1. CORE SETUP - UI and data
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tumor Volume Study")
        self.tv_data_obj = tv_data_obj
        self.studies = tv_data_obj.unique_studies

        # 2. SYSTEM-LEVEL CONFIGURATION
        self.use_latex = latex_available()

        # 3. DATA STRUCTURES & OPTIONS (before UI population)
        # Initialize all the options lists and dicts
        self.tv_transform_options = None
        self.tv_transform_dict = None
        self.spider_show_options = ["True", "False"]
        self.spider_show_dict = {"True": True, "False": False}
        self.marker_values = ['Default', '.', 'o', "s", "D"]
        self.marker_dict = {'Default': None, ".": ".", "o": "o", "s": "s", "D": "D"}
        self.event_free_delta_values = ['0.5', '1.0', '1.5', '2.0']
        self.event_free_delta_default_index = 1
        self.show_true_false_options = ["True", "False"]
        self.show_true_false_dict = {"True": True, "False": False}

        # Plot configuration data structures
        self.initial_configuration = '4'
        self.plot_config_to_index = lambda x: int(x) - 1
        self.num_of_plot_option_list = ['1', '2', '3', '4']
        self.graphic_view_plot_dict = {'1': [True, False, False, False],
                                       '2': [True, True, False, False],
                                       '3': [True, True, True, False],
                                       '4': [True, True, True, True]}

        # Style configuration data structures
        self.current_plot_style = 0
        self.style_modules_supported = ['Matplotlib', 'Science Plots']
        self.matplotlib_style_sheets_options = [
            "default",                      "classic",                   "fast",
            "dark_background",              "grayscale",                 "bmh",
            "fivethirtyeight",              "ggplot",                    "tableau-colorblind10",
            "seaborn-v0_8-bright",          "seaborn-v0_8-colorblind",   "seaborn-v0_8-dark",
            "seaborn-v0_8-dark-palette",    "seaborn-v0_8-darkgrid",     "seaborn-v0_8-deep",
            "seaborn-v0_8-muted",           "seaborn-v0_8-notebook",     "seaborn-v0_8-paper",
            "seaborn-v0_8-pastel",          "seaborn-v0_8-poster",       "seaborn-v0_8-talk",
            "seaborn-v0_8-ticks",           "seaborn-v0_8-white",        "seaborn-v0_8-whitegrid"]
        self.scienceplots_style_sheets = ["No Journal", "Nature", "IEEE", "Science"]
        self.scienceplots_color_palletes = ["No Palette", "bright", "vibrant", "muted", "retro", "high-vis", "high-contrast"]
        self.scienceplots_grid_options = ["No Grid", "Grid"]
        self.plot_style_module = None
        self.plot_matplotlib_style = None
        self.plot_scienceplot_journal = None
        self.plot_scienceplot_color = None
        self.plot_scienceplot_grid = None

        # Graphics view references
        self.graphicsView_visual_top_left = None
        self.graphicsView_visual_top_right = None
        self.graphicsView_visual_bottom_left = None
        self.graphicsView_visual_bottom_right = None
        self.original_graphics_views = None

        # Animation references
        self._gb_animation = None
        self._gb_style_anim = None
        self._gb_confg_anim = None
        self._gb_aucam_anim = None
        self._gb_evfre_anim = None
        self._gb_spidr_anim = None
        self._gb_objrp_anim = None

        # Plotting infrastructure (initialize to None before setup)
        self.plot_types = None
        self.plot_select_comboBox = None
        self.plotting_functions = None
        self.experiment_graphics_views = None
        self.available_style_colors = None

        # 4. WIDGET POPULATION (populate combo boxes)
        self.ui.comboBox_configuration_study.addItems(self.studies)
        self.ui.comboBox_configuration_num_of_plots.addItems(self.num_of_plot_option_list)
        self.ui.comboBox_configuration_num_of_plots.setCurrentIndex(
            self.plot_config_to_index(self.initial_configuration))

        # 5. INITIALIZE COMPONENT GROUP BOXES (order matters!)
        self.initialize_style_sheets_functions()  # First - sets up style system
        self.initialize_auc_by_arm_group_box()
        self.initialize_percent_tv_change_groupbox()
        self.initialize_spider_plot_group_box()
        self.initialize_event_free_group_box()
        self.initialize_objective_response_plot_groupbox()  # UNCOMMENT and place before plotting

        # 6. UI CUSTOMIZATION
        self.add_context_menu_support_to_graphic_view()
        self.initialize_collapsable_group_boxes()

        # 7. SIGNAL CONNECTIONS (after all widgets are initialized)
        initial_configuration_show_status = False
        self.ui.actionPlot_Configuration.triggered.connect(self.toggle_graph_configuration_group)
        set_layout_visible(self.ui.verticalLayout_visual_graph_settings,
                           initial_configuration_show_status)

        self.ui.comboBox_event_free_cutoff.currentIndexChanged.connect(
            self.toggle_event_free_cutoff_options)
        self.ui.comboBox_event_free_delta.currentIndexChanged.connect(
            self.update_study_view)
        self.ui.comboBox_event_free_show_risk_plot.currentIndexChanged.connect(
            self.update_study_view)
        self.ui.comboBox_event_free_show_risk_table.currentIndexChanged.connect(
            self.update_study_view)
        self.ui.comboBox_event_free_cutoff_days.currentIndexChanged.connect(
            self.update_study_view)
        self.ui.comboBox_configuration_num_of_plots.currentTextChanged.connect(
            self.toggle_plot_graphics_view)

        # 8. FINAL SETUP - Initialize plotting system (MUST BE LAST)
        self.initialize_plotting()

    # Figure utilities
    def replace_designer_graphic_view_with_custom(self, old_graphic_view: QGraphicsView):
        # Capture the original geometry and size policy
        old_height = old_graphic_view.height()
        old_policy = old_graphic_view.sizePolicy()

        # Create the new graphics view
        gv_name = old_graphic_view.objectName()
        new_graphic_view = FigureGraphicsView(self, graphic_view_name = gv_name)

        # Apply the same size policy and fixed height
        new_graphic_view.setSizePolicy(old_policy)
        if old_policy.verticalPolicy() == QSizePolicy.Policy.Fixed:
            new_graphic_view.setFixedHeight(old_height)
        else:
            # Maintain the same min/max height if not fixed
            new_graphic_view.setMinimumHeight(old_graphic_view.minimumHeight())
            new_graphic_view.setMaximumHeight(old_graphic_view.maximumHeight())

        # Replace in the parent layout
        layout = old_graphic_view.parent().layout()
        layout.replaceWidget(old_graphic_view, new_graphic_view)
        old_graphic_view.deleteLater()

        # Match geometry explicitly to prevent layout recalculation from resizing it
        new_graphic_view.setGeometry(old_graphic_view.geometry())

        return new_graphic_view
    def add_context_menu_support_to_graphic_view(self):
        # Collect Graphic Views to change
        self.graphicsView_visual_top_left = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_visual_top_left)
        self.graphicsView_visual_top_right = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_visual_top_right)
        self.graphicsView_visual_bottom_left = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_visual_bottom_left)
        self.graphicsView_visual_bottom_right = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_visual_bottom_right)

        self.graphic_views = [self.graphicsView_visual_top_left, self.graphicsView_visual_top_right,
            self.graphicsView_visual_bottom_left, self.graphicsView_visual_bottom_right]

    # Inititialize Utilities
    def initialize_plotting(self):
        # Setup study plotting
        self.plot_types = ["Spider_Plot", "Event_Free_Survivial", "Area_Under_the_Curve",
                           "Percent_TV_Change", "Objective_Response"]
        self.plot_select_comboBox = [self.ui.comboBox_configuration_plot_upper_left_2,
                                     self.ui.comboBox_configuration_plot_upper_right_2,
                                     self.ui.comboBox_configuration_plot_lower_left_2,
                                     self.ui.comboBox_configuration_plot_lower_right_2]
        self.plotting_function_dict = {"Spider_Plot": "plot_spider",
                                       "Event_Free_Survivial": "plot_event_free_survival",
                                       "Area_Under_the_Curve": "plot_auc_bar",
                                       "Percent_TV_Change": "plot_percent_tumor_vol_change_bar",
                                       "Objective_Response": "plot_vol_change_as_objective_response_bar"}

        # Get plotting function dict from TumorVolumeClass
        # Start process of replacing plotting function dict with metadata complete
        unique_studies = self.tv_data_obj.unique_studies
        first_study = self.tv_data_obj.tumor_vol_study_dict[unique_studies[0]]
        self.plotting_function_dict_2 = first_study.plotting_function_dict_2

        # Get avaialble plot type
        self.plot_types = list(self.plotting_function_dict_2.keys())
        self.plot_types.sort()

        # Initialize selection comboBoxes
        for idx, cbox in enumerate(self.plot_select_comboBox):
            cbox.addItems(self.plot_types)
            cbox.setCurrentIndex(idx)

        # Draw plots
        self.draw_figure_group()

        # Connect combobox change to figure update
        for cbox in self.plot_select_comboBox:
            cbox.currentTextChanged.connect(self.update_study_view)

        # Initialize study selection
        self.ui.comboBox_configuration_study.currentTextChanged.connect(self.update_study_configuration)
    def initialize_style_sheets_functions(self):
        # Set up highlevel options
        self.current_plot_style = 0
        self.style_modules_supported = ['Matplotlib', 'Science Plots']
        self.ui.comboBox_plot_style_module.addItems(self.style_modules_supported)
        self.ui.comboBox_plot_matplotlib_style.setCurrentIndex(self.current_plot_style )
        self.toggle_style_widgets(self.current_plot_style)

        # Set up matplotlib options
        self.ui.comboBox_plot_matplotlib_style.addItems(self.matplotlib_style_sheets_options)

        # Set up science plots
        self.ui.comboBox_plot_scienceplot_journal.addItems(self.scienceplots_style_sheets)
        self.ui.comboBox_plot_scienceplot_color.addItems(self.scienceplots_color_palletes)
        self.ui.comboBox_plot_scienceplot_grid.addItems(self.scienceplots_grid_options)

        # Toggle module widgets with group
        self.toggle_style_widgets(self.current_plot_style)

        # Connect module change to togle
        self.ui.comboBox_plot_style_module.currentIndexChanged.connect(self.toggle_style_widgets)

        # Connect plot style selection
        self.ui.pushButton_plot_uodate_style.clicked.connect(self.update_plot_style)
    def initialize_collapsable_group_boxes(self):
        # -----------------------------------------------------
        # Set animation parameters
        # -----------------------------------------------------
        animation_duration = 180
        easing = QEasingCurve.Type.InOutCubic

        # -----------------------------------------------------
        # Group box + attribute mapping
        # -----------------------------------------------------
        self._groupbox_anim_map = {
            self.ui.groupBox_plot_configurations: "_gb_confg_anim",
            self.ui.groupBox_plot_style_sheet: "_gb_style_anim",
            self.ui.groupBox_auc_by_arm: "_gb_aucam_anim",
            self.ui.groupBox_event_free_survival: "_gb_evfre_anim",
            self.ui.groupBox_configuration_spider: "_gb_spidr_anim",
            self.ui.groupBox_objective_response: "_gb_objrp_anim",
            self.ui.groupBox_percent_tv_change: "_gb_pertv_anim",
        }

        # -----------------------------------------------------
        # Create animations and store on self
        # -----------------------------------------------------
        for gbox, attr_name in self._groupbox_anim_map.items():
            anim = QPropertyAnimation(gbox, b"maximumHeight")
            anim.setDuration(animation_duration)
            anim.setEasingCurve(easing)
            setattr(self, attr_name, anim)

        # -----------------------------------------------------
        # Set initial group box settings
        # -----------------------------------------------------
        for gbox in self._groupbox_anim_map.keys():
            gbox.setChecked(False)
            gbox.layout().activate()

            header_height = gbox.fontMetrics().height() + 16
            gbox.setMaximumHeight(header_height)

        # -----------------------------------------------------
        # Connect toggles to animation handlers
        # -----------------------------------------------------
        self.ui.groupBox_plot_style_sheet.toggled.connect(
            lambda checked, gb=self.ui.groupBox_plot_style_sheet: self._animate_style_groupbox(gb, checked))
        self.ui.groupBox_plot_configurations.toggled.connect(
            lambda checked, gb=self.ui.groupBox_plot_configurations: self._animate_confg_groupbox(gb, checked))
        self.ui.groupBox_auc_by_arm.toggled.connect(
            lambda checked, gb=self.ui.groupBox_auc_by_arm: self._animate_auc_by_arm_groupbox(gb, checked))
        self.ui.groupBox_event_free_survival.toggled.connect(
            lambda checked, gb=self.ui.groupBox_event_free_survival: self._animate_event_free_groupbox(gb, checked))
        self.ui.groupBox_configuration_spider.toggled.connect(
            lambda checked, gb=self.ui.groupBox_configuration_spider: self._animate_spider_groupbox(gb, checked))
        self.ui.groupBox_objective_response.toggled.connect(
            lambda checked, gb=self.ui.groupBox_objective_response: self._animate_objrp_groupbox(gb, checked))
        self.ui.groupBox_percent_tv_change.toggled.connect(
            lambda checked, gb=self.ui.groupBox_percent_tv_change: self._animate_pertv_groupbox(gb, checked))

    # Initialize Groupboxes
    def initialize_auc_by_arm_group_box(self):
        # Combo box values
        cbox_values = ["True", "False"]

        # Define the boxes
        self.ui.comboBox_auc_normalize.addItems(cbox_values)
        self.ui.comboBox_auc_normalize.setCurrentIndex(1)

        self.ui.comboBox_auc_show_labels.addItems(cbox_values)
        self.ui.comboBox_auc_show_labels.setCurrentIndex(0)

        self.ui.comboBox_auc_shorten_labels.addItems(cbox_values)
        self.ui.comboBox_auc_shorten_labels.setCurrentIndex(1)

        # Set connections
        self.ui.comboBox_auc_normalize.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_auc_show_labels.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_auc_shorten_labels.currentTextChanged.connect(self.update_study_view_text)
    def initialize_event_free_group_box(self):
        # Block signals during initialization to prevent intermediate updates
        self.ui.comboBox_event_free_delta.blockSignals(True)
        self.ui.comboBox_event_free_cutoff.blockSignals(True)
        self.ui.comboBox_event_free_cutoff_days.blockSignals(True)
        self.ui.comboBox_event_free_show_risk_plot.blockSignals(True)
        self.ui.comboBox_event_free_show_risk_table.blockSignals(True)

        try:
            # Set parameters
            self.ui.comboBox_event_free_delta.clear()
            self.ui.comboBox_event_free_delta.addItems(self.event_free_delta_values)
            self.ui.comboBox_event_free_delta.setCurrentIndex(self.event_free_delta_default_index)

            # Set study dependent value
            min_of_max_cutoff = self.get_study_min_of_max_timepoints()
            self.cutoff_options = [f"Common Across Arms - Day {int(min_of_max_cutoff)}",
                                   "Full Follow-up", "Fixed"]
            self.ui.comboBox_event_free_cutoff.clear()
            self.ui.comboBox_event_free_cutoff.addItems(self.cutoff_options)

            minimum_allowable_cutoff_options = 5
            fixed_cutoff_options = [str(cutoff_val)
                                    for cutoff_val in
                                    range(minimum_allowable_cutoff_options, int(min_of_max_cutoff) + 1)]
            self.ui.comboBox_event_free_cutoff_days.clear()
            self.ui.comboBox_event_free_cutoff_days.addItems(fixed_cutoff_options)
            self.ui.comboBox_event_free_cutoff_days.setCurrentIndex(self.ui.comboBox_event_free_cutoff_days.count() - 1)

            # Set fixed day option visibility - FIXED: Check the cutoff TYPE combobox
            current_cutoff_type_index = self.ui.comboBox_event_free_cutoff.currentIndex()
            set_layout_visible(self.ui.horizontalLayout_event_free_cutoff_day,
                               True if current_cutoff_type_index == 2 else False)

            # Set combo box options
            self.ui.comboBox_event_free_show_risk_plot.clear()
            self.ui.comboBox_event_free_show_risk_plot.addItems(self.show_true_false_options)
            self.ui.comboBox_event_free_show_risk_table.clear()
            self.ui.comboBox_event_free_show_risk_table.addItems(self.show_true_false_options)

        finally:
            # Always unblock signals, even if there's an error
            self.ui.comboBox_event_free_delta.blockSignals(False)
            self.ui.comboBox_event_free_cutoff.blockSignals(False)
            self.ui.comboBox_event_free_cutoff_days.blockSignals(False)
            self.ui.comboBox_event_free_show_risk_plot.blockSignals(False)
            self.ui.comboBox_event_free_show_risk_table.blockSignals(False)
    def initialize_objective_response_plot_groupbox(self):
        # Combo box values
        cbox_values = ["True", "False"]

        # Define the boxes
        self.ui.comboBox_obj_res_show_labels.addItems(cbox_values)
        self.ui.comboBox_obj_res_show_labels.setCurrentIndex(0)

        self.ui.comboBox_obj_res_shorten_labels.addItems(cbox_values)
        self.ui.comboBox_obj_res_shorten_labels.setCurrentIndex(1)

        # Get current style color selection
        if self.available_style_colors == None:
            # First initialization add default color
            available_style_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        else:
            available_style_colors = self.get_style_colors()  # Lazy loading
        self.available_style_colors = available_style_colors

        orc_cboxes = [self.ui.comboBox_objective_plot_pd, self.ui.comboBox_objective_plot_sd,
                      self.ui.comboBox_objective_plot_pr, self.ui.comboBox_objective_plot_cr]
        self._populate_color_comboboxes(orc_cboxes, available_style_colors, color_shift=2)

        # Set Index
        color_shift = 2  # don't use the first two colors, assuming two arms
        for idx, cbox in enumerate(orc_cboxes):
            cbox.setCurrentIndex(idx+color_shift)

        # Connect pushbutton to update objective response plot
        self.ui.pushButton_objective_response_update.clicked.connect(self.update_study_view)
    def initialize_percent_tv_change_groupbox(self):
        # Combo box values
        cbox_values = ["True", "False"]

        # Define the boxes
        self.ui.comboBox_tv_change_normalize.addItems(cbox_values)
        self.ui.comboBox_tv_change_normalize.setCurrentIndex(1)

        self.ui.comboBox_tv_change_show_labels.addItems(cbox_values)
        self.ui.comboBox_tv_change_show_labels.setCurrentIndex(0)

        self.ui.comboBox_tv_change_shorten_labels.addItems(cbox_values)
        self.ui.comboBox_tv_change_shorten_labels.setCurrentIndex(1)

        # Set connections
        self.ui.comboBox_tv_change_normalize.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_tv_change_show_labels.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_tv_change_shorten_labels.currentTextChanged.connect(self.update_study_view_text)
    def initialize_spider_plot_group_box(self):
        # Get transform information
        unique_studies = self.tv_data_obj.unique_studies
        first_study = self.tv_data_obj.tumor_vol_study_dict[unique_studies[0]]
        self.tv_transform_options = first_study.tv_transform_options
        self.tv_transform_dict = first_study.tv_transform_dict
        self.ui.comboBox_config_data_transform.addItems(self.tv_transform_options)

        # Set show varaibles
        self.ui.comboBox_spider_time_series.addItems(self.spider_show_options)
        self.ui.comboBox_spider_aggregate.addItems(self.spider_show_options)
        self.ui.comboBox_spider_weight.addItems(self.spider_show_options)

        # Aggregate variables
        self.ui.comboBox_spider_marker.addItems(self.marker_values)
        self.ui.comboBox_spider_sem.addItems(self.spider_show_options)
        self.ui.comboBox_spider_err_bars.addItems(self.spider_show_options)
        self.ui.comboBox_spider_err_bars.setCurrentIndex(1) #set to false

        # Connect update buttong to graph plot
        self.ui.comboBox_config_data_transform.currentTextChanged.connect(self.update_study_view)
        self.ui.comboBox_spider_time_series.currentTextChanged.connect(self.update_study_view)
        self.ui.comboBox_spider_aggregate.currentTextChanged.connect(self.update_study_view)
        self.ui.comboBox_spider_weight.currentTextChanged.connect(self.update_study_view)
        self.ui.comboBox_spider_marker.currentTextChanged.connect(self.update_study_view)
        self.ui.comboBox_spider_sem.currentTextChanged.connect(self.update_study_view)
        self.ui.comboBox_spider_err_bars.currentTextChanged.connect(self.update_study_view)

    # Group Box Utilities
    def get_study_min_of_max_timepoints(self):
        # Get current study
        current_study_label = self.ui.comboBox_configuration_study.currentText()
        study_obj = self.tv_data_obj.tumor_vol_study_dict[current_study_label]
        study_tv_time_dict = study_obj.study_tv_time_dict

        # Scan time series
        tv_labels = study_tv_time_dict.keys()
        max_time_array = []
        for tv_label in tv_labels:
            tv_data = study_tv_time_dict[tv_label]
            max_time_array.append(np.max(tv_data.time_day))
        min_of_max_time_array = np.min(max_time_array)
        return min_of_max_time_array
    def get_study_max_of_max_timepoints(self):
        # Get current study
        current_study_label = self.ui.comboBox_configuration_study.currentText()
        study_obj = self.tv_data_obj.tumor_vol_study_dict[current_study_label]
        study_tv_time_dict = study_obj.study_tv_time_dict

        # Scan time series
        tv_labels = study_tv_time_dict.keys()
        max_time_array = []
        for tv_label in tv_labels:
            tv_data = study_tv_time_dict[tv_label]
            max_time_array.append(np.max(tv_data.time_day))
        max_of_max_time_array = np.max(max_time_array)
        return max_of_max_time_array
    def _populate_color_comboboxes(self, combo_boxes, available_style_colors:list[str]|None, color_shift:int=0):
        """Populate ALL combo boxes with ALL available colors from the current style.

        Args:
            combo_boxes: List of combo box objects to populate. If None, attempts to
                         find combo boxes using default naming convention.
        """

        # Convert to hex
        if not self._is_hex_color(available_style_colors[0]):
            available_style_colors = [ self._mpl_code_to_hex(c) for c in available_style_colors]

        # If no combo boxes provided, try default naming convention
        if combo_boxes is None:
            combo_boxes = []
            response_types = ['PD', 'SD', 'PR', 'CR']

            for response in response_types:
                combo_box_name = f'comboBox_{response}_color'
                if hasattr(self.ui, combo_box_name):
                    combo_boxes.append(getattr(self.ui, combo_box_name))

        # Populate EACH combo box with ALL available colors
        count = 0
        for idx, combo_box in enumerate(combo_boxes):
            combo_box.clear()

            # Add ALL colors from the style to this combo box
            num_color = len(available_style_colors)
            for i, color in enumerate(available_style_colors):
                # Create a colored icon for visual reference
                pixmap = QPixmap(20, 20)
                pixmap.fill(QColor(color))
                icon = QIcon(pixmap)

                # Add to combo box with color name/hex
                color_name = f"Color {i+1} ({color})"
                combo_box.addItem(icon, color_name, userData=color)
            combo_box.setCurrentIndex((count+color_shift)%num_color)
            count += 1
    def _extract_color_from_label(self, color_label):
        """Extract hex color from a label like 'Color 1 (#1f77b4)'"""
        match = re.search(r'#[0-9a-fA-F]{6}', color_label)
        if match:
            return match.group(0)
        # If no hex code found, assume it's already a valid color
        return color_label
    def _is_hex_color(self,s: str) -> bool:
        if not isinstance(s, str):
            return False
        if not s.startswith("#"):
            return False
        if len(s) not in (4, 7, 9):
            return False

        try:
            int(s[1:], 16)
            return True
        except ValueError:
            return False
    def _mpl_code_to_hex(self,code: str) -> str:
        base_map = {
            "b": "#0000FF",
            "g": "#008000",
            "r": "#FF0000",
            "c": "#00FFFF",
            "m": "#FF00FF",
            "y": "#FFFF00",
            "k": "#000000",
            "w": "#FFFFFF",
        }

        tab_map = {
            "tab:blue": "#1f77b4",
            "tab:orange": "#ff7f0e",
            "tab:green": "#2ca02c",
            "tab:red": "#d62728",
            "tab:purple": "#9467bd",
            "tab:brown": "#8c564b",
            "tab:pink": "#e377c2",
            "tab:gray": "#7f7f7f",
            "tab:olive": "#bcbd22",
            "tab:cyan": "#17becf",
        }

        gray_map = {
            "0.00": "#000000",
            "0.40": "#666666",
            "0.60": "#999999",
            "0.70": "#b2b2b2"
        }

        gray_map_numeric = {
            0.00: "#000000",
            0.40: "#666666",
            0.60: "#999999",
            0.70: "#b2b2b2"
        }

        if code in base_map:
            return base_map[code]
        if code in tab_map:
            return tab_map[code]
        if code in gray_map:
            return gray_map[code]
        if code in gray_map_numeric:
            return gray_map[code]

        raise ValueError(f"Unknown matplotlib color code: {code}")

    # Update Figure
    def get_plot_style(self):
        # Get style information from interface
        plot_style = None
        plot_style_module = self.ui.comboBox_plot_style_module.currentText()
        if plot_style_module == "Matplotlib":
            self.plot_style_module = plot_style_module
            self.plot_matplotlib_style = self.ui.comboBox_plot_matplotlib_style.currentText()
            plot_style = self.plot_matplotlib_style
        elif plot_style_module == "Science Plots":
            # Get plot specification
            self.plot_style_module = plot_style_module
            self.plot_scienceplot_journal = self.ui.comboBox_plot_scienceplot_journal.currentText().lower()
            self.plot_scienceplot_color = self.ui.comboBox_plot_scienceplot_color.currentText().lower()
            self.plot_scienceplot_grid = self.ui.comboBox_plot_scienceplot_grid.currentText().lower()

            # Set up matplotloib style variable
            plot_style = ['science']
            if self.plot_scienceplot_journal != "No Journal".lower():
                plot_style.append(self.plot_scienceplot_journal.lower())
            if self.plot_scienceplot_color != "No Palette".lower():
                plot_style.append(self.plot_scienceplot_color)
            if self.plot_scienceplot_grid != 'No Grid'.lower():
                plot_style.append(self.plot_scienceplot_grid)
            if self.use_latex == False:
                plot_style.append(self.plot_scienceplot_grid)
        else:
            logger.info(f'Plot style module not supported: {self.plot_style_module}')

        # Return Plot Style
        return plot_style
    def get_style_colors(self):
        # Default fallback
        if not self.plot_style_module or not self.plot_matplotlib_style:
            # Use matplotlib default if style not configured
            return plt.rcParams['axes.prop_cycle'].by_key()['color']

        # module = ("Matplotlib", "Science Plots")
        plot_style_module = self.ui.comboBox_plot_style_module.currentText()
        plot_style = self.get_plot_style()

        # Apply the style temporarily to extract colors
        with plt.style.context(plot_style):
            # Get the color cycle from the current style
            prop_cycle = plt.rcParams['axes.prop_cycle']
            colors = prop_cycle.by_key()['color']

        return colors
    def get_obj_response_color_from_style_colors(self):
        # Default fallback
        if not self.plot_style_module or not self.plot_matplotlib_style:
            # Use matplotlib default if style not configured
            return plt.rcParams['axes.prop_cycle'].by_key()['color']

        # module = ("Matplotlib", "Science Plots")
        plot_style_module = self.ui.comboBox_plot_style_module.currentText()
        plot_style = self.get_plot_style()

        # Apply the style temporarily to extract colors
        with plt.style.context(plot_style):
            # Get the color cycle from the current style
            prop_cycle = plt.rcParams['axes.prop_cycle']
            colors = prop_cycle.by_key()['color']

            # Create objective response color dictionary
            # Map responses to colors from the style's color cycle
            objective_responses = ['PD', 'SD', 'PR', 'CR']

            self.objective_response_colors = {}

            # Assign colors to each response type
            for i, response in enumerate(objective_responses):
                # Use modulo to cycle through colors if we have more responses than colors
                color_idx = i % len(colors)
                self.objective_response_colors[response] = colors[color_idx]

            # Optionally, store all available colors for the combo box
            self.available_style_colors = list(colors)

        return self.objective_response_colors
    def update_study_view(self):
        # Respond to figure comboBox change
        plot_style = self.get_plot_style()
        self.draw_figure_group(plot_style = plot_style)
    def update_study_view_text(self, *_):
        # Respond to figure comboBox change
        plot_style = self.get_plot_style()
        self.draw_figure_group(plot_style = plot_style)

    # Update Group Box Parameters
    def update_study_configuration(self):
        # Update Study View
        self.update_study_view()

        # Update Event Free Options
        self.initialize_event_free_group_box()
    def update_plot_style(self):
        # Update figures
        plot_style = self.get_plot_style()
        self._recompute_groupbox_height(self.ui.groupBox_plot_style_sheet)

        # Update Objective Response Plot Options
        combo_boxes = [self.ui.comboBox_objective_plot_pd, self.ui.comboBox_objective_plot_sd,
                       self.ui.comboBox_objective_plot_pr, self.ui.comboBox_objective_plot_cr]
        available_style_colors = self.get_style_colors()
        self._populate_color_comboboxes(combo_boxes, available_style_colors, color_shift=2)

        # Update Study View
        self.update_study_view()
    def update_event_free_cutoff_type(self):
        # Set
        current_cutoff_index = self.ui.comboBox_event_free_cutoff_days.currentIndex()
        set_layout_visible(self.ui.horizontalLayout_event_free_cutoff_day,
                           True if current_cutoff_index == 2 else False)

    # Interface Utilities
    def toggle_graph_configuration_group(self):
        # Add/remove plot selection parmaeters
        toggled_boolean =  not self.ui.groupBox_plot_configurations.isVisible()
        configuration_layout = self.ui.verticalLayout_visual_graph_settings
        set_layout_visible(configuration_layout, toggled_boolean)
    def toggle_plot_graphics_view(self, new_text):
        # Reconfigure display to include number of graphic views displayed
        configuration_text = new_text
        graphic_view_boolean_settings = self.graphic_view_plot_dict[configuration_text]
        for (gv, gv_visible) in zip(self.graphic_views, graphic_view_boolean_settings):
            gv.setVisible(gv_visible)
    def toggle_style_widgets(self, new_index):
        # Matplotlib = 0, Science Plots = 1
        set_layout_visible(self.ui.verticalLayout_plot_scienceplot_options, bool(new_index))
        set_layout_visible(self.ui.verticalLayout_matplotlib_options,not bool(new_index))
        self._recompute_groupbox_height(self.ui.groupBox_plot_style_sheet)
    def toggle_event_free_cutoff_options(new_index):
        # Handle fixed cutoff options
        common_across_arms = 0
        full_follow_up = 1
        fixed_option_value = 2
        if fixed_option_value == new_index:
            set_layout_visible(self.ui.horizontalLayout_event_free_cutoff_day, True)
        elif full_follow_up == new_index:
            # Set cutoff to maximum number of days
            option_index = self.ui.comboBox_event_free_cutoff_days.count()-1
            self.ui.comboBox_event_free_cutoff_days.setCurrentIndex(option_index)

            # Hide cutoff day visability
            set_layout_visible(self.ui.horizontalLayout_event_free_cutoff_day, False)
        elif common_across_arms == new_index:
            # Set cutof day to minimmum of maximum number of days per time series
            study_min_of_max_days = self.get_study_min_of_max_timepoints()
            cutoff_options = [int(self.ui.comboBox_event_free_cutoff_days.itemText(i))
                              for i in range(self.ui.comboBox_event_free_cutoff_days.count())]
            option_index = [idx for idx, v in enumerate(cutoff_options) if v == study_min_of_max_days]
            option_index = option_index[0]

            self.ui.comboBox_event_free_cutoff_days.setCurrentIndex(option_index)

            # Hide cuttoff day visability
            set_layout_visible(self.ui.horizontalLayout_event_free_cutoff_day, False)
        else:
            logger.info('Event Free cutoff option changed. Option not supported.')

    # Group box animation code (could be consolidated with a dictionary)
    def _animate_style_groupbox_3(self, groupbox: QGroupBox, expanded: bool):
        layout = groupbox.layout()
        if layout is None:
            return

        header_height = groupbox.fontMetrics().height() + 16

        # EXPAND
        if expanded:
            # 1. Show content FIRST
            set_layout_visible(self.ui.verticalLayout_plot_style_group, True)

            # 2. Force layout recalculation
            layout.invalidate()
            groupbox.updateGeometry()

            # 3. Measure AFTER content is visible
            content_height = layout.sizeHint().height()
            expanded_height = header_height + content_height

            anim = QPropertyAnimation(groupbox, b"minimumHeight", groupbox)
            anim.setDuration(200)
            anim.setStartValue(header_height)
            anim.setEndValue(expanded_height)

            # Update scroll area during animation
            #anim.valueChanged.connect(lambda: self._update_scroll_area(groupbox))

        # COLLAPSE
        else:
            # Keep maximum height unlimited during animation
            groupbox.setMaximumHeight(16777215)

            anim = QPropertyAnimation(groupbox, b"minimumHeight", groupbox)
            anim.setDuration(200)
            anim.setStartValue(groupbox.height())
            anim.setEndValue(header_height)

            # Update scroll area during animation
            anim.valueChanged.connect(lambda: self._update_scroll_area(groupbox))

            # Hide content and constrain size AFTER collapse finishes
            def on_collapse_finished():
                set_layout_visible(self.ui.verticalLayout_plot_style_group, False)
                groupbox.setMaximumHeight(header_height)
                groupbox.setMinimumHeight(header_height)
                self._update_scroll_area(groupbox)

            anim.finished.connect(on_collapse_finished)

        anim.start()
        groupbox._anim = anim  # keep alive+
    def _update_scroll_area(self, groupbox: QGroupBox):
        """Force the scroll area to update when groupbox size changes"""
        scroll_area = groupbox
        # Walk up the parent hierarchy to find the scroll area
        while scroll_area is not None:
            if isinstance(scroll_area, QScrollArea):
                scroll_area.widget().updateGeometry()
                break
            scroll_area = scroll_area.parentWidget()
    def _animate_style_groupbox(self, groupbox: QGroupBox, expanded: bool):
        header_height = groupbox.fontMetrics().height() + 16

        layout = groupbox.layout()
        content_height = layout.sizeHint().height() if layout else 0

        expanded_height = header_height + content_height

        self._gb_style_anim.stop()

        if expanded:
            self._gb_style_anim.setStartValue(groupbox.maximumHeight())
            self._gb_style_anim.setEndValue(expanded_height)
        else:
            self._gb_style_anim.setStartValue(groupbox.maximumHeight())
            self._gb_style_anim.setEndValue(header_height)

        self._gb_style_anim.start()
    def _animate_confg_groupbox(self, groupbox: QGroupBox, expanded: bool):
        header_height = groupbox.fontMetrics().height() + 16

        layout = groupbox.layout()
        content_height = layout.sizeHint().height() if layout else 0

        expanded_height = header_height + content_height

        self._gb_confg_anim.stop()

        if expanded:
            self._gb_confg_anim.setStartValue(groupbox.maximumHeight())
            self._gb_confg_anim.setEndValue(expanded_height)
        else:
            self._gb_confg_anim.setStartValue(groupbox.maximumHeight())
            self._gb_confg_anim.setEndValue(header_height)

        self._gb_confg_anim.start()
    def _animate_auc_by_arm_groupbox(self, groupbox: QGroupBox, expanded: bool):
        header_height = groupbox.fontMetrics().height() + 16

        layout = groupbox.layout()
        content_height = layout.sizeHint().height() if layout else 0

        expanded_height = header_height + content_height

        self._gb_aucam_anim.stop()

        if expanded:
            self._gb_aucam_anim.setStartValue(groupbox.maximumHeight())
            self._gb_aucam_anim.setEndValue(expanded_height)
        else:
            self._gb_aucam_anim.setStartValue(groupbox.maximumHeight())
            self._gb_aucam_anim.setEndValue(header_height)

        self._gb_aucam_anim.start()
    def _animate_event_free_groupbox(self, groupbox: QGroupBox, expanded: bool):
        header_height = groupbox.fontMetrics().height() + 16

        layout = groupbox.layout()
        content_height = layout.sizeHint().height() if layout else 0

        expanded_height = header_height + content_height

        self._gb_evfre_anim.stop()

        if expanded:
            self._gb_evfre_anim.setStartValue(groupbox.maximumHeight())
            self._gb_evfre_anim.setEndValue(expanded_height)
        else:
            self._gb_evfre_anim.setStartValue(groupbox.maximumHeight())
            self._gb_evfre_anim.setEndValue(header_height)

        self._gb_evfre_anim.start()
    def _animate_spider_groupbox(self, groupbox: QGroupBox, expanded: bool):
        header_height = groupbox.fontMetrics().height() + 16

        layout = groupbox.layout()
        content_height = layout.sizeHint().height() if layout else 0

        expanded_height = header_height + content_height

        self._gb_spidr_anim.stop()

        if expanded:
            self._gb_spidr_anim.setStartValue(groupbox.maximumHeight())
            self._gb_spidr_anim.setEndValue(expanded_height)
        else:
            self._gb_spidr_anim.setStartValue(groupbox.maximumHeight())
            self._gb_spidr_anim.setEndValue(header_height)

        self._gb_spidr_anim.start()
    def _animate_objrp_groupbox(self, groupbox: QGroupBox, expanded: bool):
        header_height = groupbox.fontMetrics().height() + 16

        layout = groupbox.layout()
        content_height = layout.sizeHint().height() if layout else 0

        expanded_height = header_height + content_height

        self._gb_objrp_anim.stop()

        if expanded:
            self._gb_objrp_anim.setStartValue(groupbox.maximumHeight())
            self._gb_objrp_anim.setEndValue(expanded_height)
        else:
            self._gb_objrp_anim.setStartValue(groupbox.maximumHeight())
            self._gb_objrp_anim.setEndValue(header_height)

        self._gb_objrp_anim.start()
    def _animate_pertv_groupbox(self, groupbox: QGroupBox, expanded: bool):
        header_height = groupbox.fontMetrics().height() + 16

        layout = groupbox.layout()
        content_height = layout.sizeHint().height() if layout else 0

        expanded_height = header_height + content_height

        self._gb_pertv_anim.stop()

        if expanded:
            self._gb_pertv_anim.setStartValue(groupbox.maximumHeight())
            self._gb_pertv_anim.setEndValue(expanded_height)
        else:
            self._gb_pertv_anim.setStartValue(groupbox.maximumHeight())
            self._gb_pertv_anim.setEndValue(header_height)

        self._gb_pertv_anim.start()
    def _recompute_groupbox_height(self, groupbox):
        layout = groupbox.layout()
        if not layout:
            return

        layout.activate()

        header_height = groupbox.fontMetrics().height() + 16
        content_height = layout.sizeHint().height()

        expanded_height = header_height + content_height

        groupbox.setMaximumHeight(expanded_height)

    # Plot Figure
    def draw_figure_group(self, plot_style = None):
        # Log draw
        logger.info('Drawing figure group')

        # Get style information
        updated_style = plot_style

        # Get plot settings
        study_id = self.ui.comboBox_configuration_study.currentText()
        num_figures = int(self.ui.comboBox_configuration_num_of_plots.currentText())
        study_obj = self.tv_data_obj.tumor_vol_study_dict[study_id]

        # Update each plot
        for idx in range(num_figures):
            # Get plot information
            selected_plot = self.plot_select_comboBox[idx].currentText()
            plot_metadata = self.plotting_function_dict_2[selected_plot]
            plot_name = plot_metadata["function"]
            graphic_view = self.graphic_views[idx]

            # Get custom parameters
            custom_params = self.get_custom_parameters(plot_name)

            # Plot figure
            study_obj.plot_to_widget_by_name(plot_name, graphic_view, plot_style=updated_style, **custom_params)

    # Get custom plot figures
    def get_custom_parameters(self, plot_name):
        # Define custom parameters
        custom_params = {}

        if plot_name == "plot_auc_bar":
            logger.info('Returning auc by arm group box parameters')
            custom_params = self.get_auc_by_arm_group_box_parameters()
        elif plot_name == "plot_event_free_survival":
            custom_params = self. get_event_free_group_box_parameters()
        elif plot_name == "plot_vol_change_as_objective_response_bar":
            custom_params = self. get_objective_response_group_box_parameters()
        elif plot_name == "plot_percent_tumor_vol_change_bar":
            custom_params = self. get_percent_tv_change_group_box_parameters()
        elif plot_name == "plot_spider":
            custom_params = self.get_spider_group_box_parameters()

        return custom_params
    def get_auc_by_arm_group_box_parameters(self):
        # log parameter query
        logger.info('Getting auc by arm group box parameters')

        # Get values
        plot_normalized_auc = True if self.ui.comboBox_auc_normalize.currentText() == "True" else False
        show_axis_labels = True if self.ui.comboBox_auc_show_labels.currentText() == "True" else False
        shorten_x_labels = True if self.ui.comboBox_auc_shorten_labels.currentText() == "True" else False

        # Construct custom parameter dictionary
        custom_params = {"plot_normalized_auc": plot_normalized_auc, "show_axis_labels": show_axis_labels,
                         "shorten_x_labels": shorten_x_labels}
        return custom_params
    def get_event_free_group_box_parameters(self):
        # Get values
        delta = float(self.ui.comboBox_event_free_delta.currentText())
        show_risk_plot = True if self.ui.comboBox_event_free_show_risk_plot.currentText() == "True" else False
        show_risk_table = True if self.ui.comboBox_event_free_show_risk_table.currentText() == "True" else False

        # Set cutoff directly, not using None option to transparency
        # Assumes interface appropraitely sets cutoff value based on selection option
        cutoff_type = self.ui.comboBox_event_free_cutoff.currentText()
        if cutoff_type == "Full Follow-up":
            cutoff = None
        else:
            cutoff_value = int(self.ui.comboBox_event_free_cutoff_days.currentText())
            cutoff = cutoff_value

        # Construct custom parameter dictionary
        custom_params = {"delta": delta, "cutoff": cutoff, "show_risk_plot": show_risk_plot,
                         "show_risk_table": show_risk_table}
        return custom_params
    def get_spider_group_box_parameters(self):
        # Get information from group box
        data_transform = self.ui.comboBox_config_data_transform.currentText()
        time_series = self.spider_show_dict[self.ui.comboBox_spider_time_series.currentText()]
        aggregate = self.spider_show_dict[self.ui.comboBox_spider_aggregate.currentText()]
        weight = self.spider_show_dict[self.ui.comboBox_spider_weight.currentText()]
        marker = self.marker_dict[self.ui.comboBox_spider_marker.currentText()]
        sem = self.spider_show_dict[self.ui.comboBox_spider_sem.currentText()]
        err_bars = self.spider_show_dict[self.ui.comboBox_spider_err_bars.currentText()]

        # Construct custom parameter dictionary
        custom_params = {"plot_weight": weight, "show_individual": time_series, "show_aggregate": aggregate,
                         "aggregate_sem": sem, "error_bars": err_bars, "aggregate_marker":marker,
                         "tv_transform_str":data_transform}
        return custom_params
    def get_objective_response_group_box_parameters(self):
        # Get label parameters
        show_axis_labels = True if self.ui.comboBox_obj_res_show_labels.currentText()=='True' else False
        shorten_x_labels = True if self.ui.comboBox_obj_res_shorten_labels.currentText()=='True' else False

        # Get Color parameters
        pd_color = self._extract_color_from_label(self.ui.comboBox_objective_plot_pd.currentText())
        sd_color = self._extract_color_from_label(self.ui.comboBox_objective_plot_sd.currentText())
        pr_color = self._extract_color_from_label(self.ui.comboBox_objective_plot_pr.currentText())
        cr_color = self._extract_color_from_label(self.ui.comboBox_objective_plot_cr.currentText())

        pd_index = self.ui.comboBox_objective_plot_pd.currentIndex()
        sd_index = self.ui.comboBox_objective_plot_sd.currentIndex()
        pr_index = self.ui.comboBox_objective_plot_pr.currentIndex()
        cr_index = self.ui.comboBox_objective_plot_cr.currentIndex()

        # Construct custom parameter dictionary
        custom_params = {"objective_response_colors":
                             {"PD": pd_color, "SD": sd_color, "PR": pr_color,"CR": cr_color},
                         "show_axis_labels": show_axis_labels, "shorten_x_labels": shorten_x_labels}
        return custom_params
    def get_percent_tv_change_group_box_parameters(self):
        # log parameter query
        logger.info('Getting percent tv change group box parameters')

        # Get values
        plot_normalized_tv_change = True if self.ui.comboBox_tv_change_normalize.currentText() == "True" else False
        show_axis_labels = True if self.ui.comboBox_tv_change_show_labels.currentText() == "True" else False
        shorten_x_labels = True if self.ui.comboBox_tv_change_shorten_labels.currentText() == "True" else False

        # Construct custom parameter dictionary
        custom_params = {"plot_normalized_tv_change": plot_normalized_tv_change, "show_axis_labels": show_axis_labels,
                         "shorten_x_labels": shorten_x_labels}
        return custom_params