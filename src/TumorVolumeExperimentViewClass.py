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

# Interface
from PySide6.QtWidgets import QMainWindow, QGraphicsView, QSizePolicy, QGroupBox
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPixmap, QIcon

# Tumor volume classes
from TumorVolumeClass import TumorVolumeDataClass

# GUI Interface
from TumorVolumeExperimentView import Ui_MainWindow

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
class TumorVolumeExperimentWindow(QMainWindow):
    # Intitialize
    def __init__(self, tv_data_obj: TumorVolumeDataClass, parent=None):
        super().__init__(parent)

        # 1. CORE SETUP - UI and data
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tumor Volume Experiment")
        self.tv_data_obj = tv_data_obj
        self.experiments = tv_data_obj.unique_experiments

        # 2. SYSTEM-LEVEL CONFIGURATION
        self.use_latex = latex_available()

        # 3. DATA STRUCTURES & OPTIONS (before UI population)
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
            "default", "classic", "fast",
            "dark_background", "grayscale", "bmh",
            "fivethirtyeight", "ggplot", "tableau-colorblind10",
            "seaborn-v0_8-bright", "seaborn-v0_8-colorblind", "seaborn-v0_8-dark",
            "seaborn-v0_8-dark-palette", "seaborn-v0_8-darkgrid", "seaborn-v0_8-deep",
            "seaborn-v0_8-muted", "seaborn-v0_8-notebook", "seaborn-v0_8-paper",
            "seaborn-v0_8-pastel", "seaborn-v0_8-poster", "seaborn-v0_8-talk",
            "seaborn-v0_8-ticks", "seaborn-v0_8-white", "seaborn-v0_8-whitegrid"]
        self.scienceplots_style_sheets = ["No Journal", "Nature", "IEEE", "Science"]
        self.scienceplots_color_palletes = ["No Palette", "bright", "vibrant", "muted", "retro", "high-vis",
                                            "high-contrast"]
        self.scienceplots_grid_options = ["No Grid", "Grid"]
        self.plot_style_module = None
        self.plot_matplotlib_style = None
        self.plot_scienceplot_journal = None
        self.plot_scienceplot_color = None
        self.plot_scienceplot_grid = None

        # Tumor control ratio plot data structures
        self.rotation_option_dict = {"horizontal": 0, "slight": 30, "diagonal": 45, "steep": 60, "vertical": 90}

        # Graphics view references
        self.graphicsView_visual_top_left = None
        self.graphicsView_visual_top_right = None
        self.graphicsView_visual_bottom_left = None
        self.graphicsView_visual_bottom_right = None
        self.original_graphics_views = None

        # Animation references
        self._gb_animation = None

        # Plotting infrastructure (initialize to None before setup)
        self.plot_types = None
        self.plot_select_comboBox = None
        self.plotting_functions = None
        self.experiment_graphics_views = None
        self.available_style_colors = None

        # 4. WIDGET POPULATION (populate combo boxes)
        self.ui.comboBox_configuration_experiments.addItems(self.experiments)
        self.ui.comboBox_configuration_num_of_plots.addItems(self.num_of_plot_option_list)
        self.ui.comboBox_configuration_num_of_plots.setCurrentIndex(
            self.plot_config_to_index(self.initial_configuration))

        # 5. INITIALIZE COMPONENT GROUP BOXES (order matters!)
        self.initialize_style_sheets_functions()  # First - sets up style system
        self.initialize_objective_response_plot_groupbox()
        self.initialize_tumor_control_ratio_groupbox()

        # 6. UI CUSTOMIZATION
        self.add_context_menu_support_to_graphic_view()
        self.initialize_collapsable_group_boxes()

        # 7. SIGNAL CONNECTIONS (after all widgets are initialized)
        initial_plot_configuration_visability = False
        self.ui.actionPlot_Configuration.triggered.connect(self.toggle_graph_configuration_group)
        set_layout_visible(self.ui.verticalLayout_visual_graph_settings,
                           initial_plot_configuration_visability)

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
        # Setup plotting
        self.plot_types = ["Avg_TV_Change_Bar", "TV_Control_Bar", "Objective_Response_Bar",
                           "AUC_with_Control_Bar", "Log2_Fold_Change_w_Error"]
        self.plot_select_comboBox = [self.ui.comboBox_configuration_plot_upper_left, self.ui.comboBox_configuration_plot_upper_right,
                            self.ui.comboBox_configuration_plot_lower_left, self.ui.comboBox_configuration_plot_lower_right]
        self.plotting_function_dict = {"Avg_TV_Change_Bar":"plot_average_tumor_volume_change_bar", "TV_Control_Bar":"plot_tumor_control_ratio_bar",
                            "Objective_Response_Bar":"proportion_in_objective_response_classification_bar", "AUC_with_Control_Bar":"plot_auc_with_controls_bar",
                            "Log2_Fold_Change_w_Error":"plot_log2fc_points"}

        # Initialize selection comboBoxes
        for idx, cbox in enumerate(self.plot_select_comboBox):
            cbox.addItems(self.plot_types)
            cbox.setCurrentIndex(idx)

        # Draw plots
        self.draw_figure_group()

        # Connect combobox change to figure update
        for cbox in self.plot_select_comboBox:
            cbox.currentTextChanged.connect(self.update_experiment_view)
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

        # Define box animation
        self._gb_style_anim = QPropertyAnimation(self.ui.groupBox_plot_style_sheet, b"maximumHeight")
        self._gb_style_anim.setDuration(180)
        self._gb_style_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self._gb_confg_anim = QPropertyAnimation(self.ui.groupBox_plot_configurations, b"maximumHeight")
        self._gb_confg_anim.setDuration(180)
        self._gb_confg_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self._gb_objrp_anim = QPropertyAnimation(self.ui.groupBox_objective_response, b"maximumHeight")
        self._gb_objrp_anim.setDuration(180)
        self._gb_objrp_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self._gb_tcrat_anim = QPropertyAnimation(self.ui.groupBox_tumor_control_ratio, b"maximumHeight")
        self._gb_tcrat_anim.setDuration(180)
        self._gb_tcrat_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Set checked
        self.ui.groupBox_plot_configurations.setChecked(True)
        self.ui.groupBox_plot_style_sheet.setChecked(False)
        self.ui.groupBox_objective_response.setChecked(False)
        self.ui.groupBox_tumor_control_ratio.setChecked(False)

        # Set initial group box settings
        group_boxes = [self.ui.groupBox_plot_configurations, self.ui.groupBox_plot_style_sheet, self.ui.groupBox_objective_response,
                       self.ui.groupBox_tumor_control_ratio]
        init_group_box_state = [True, False, False, False]
        for gbox, gstate in zip(group_boxes, init_group_box_state):
            gbox.setChecked(gstate)
            gbox.layout().activate()
            header_height = gbox.fontMetrics().height()+16
            if gstate == False:
                gbox.setMaximumHeight(header_height)

        # Conenct to toggle function
        self.ui.groupBox_plot_style_sheet.toggled.connect(lambda checked: self._animate_style_groupbox(self.ui.groupBox_plot_style_sheet, checked))
        self.ui.groupBox_plot_configurations.toggled.connect(lambda checked: self._animate_confg_groupbox(self.ui.groupBox_plot_configurations, checked))
        self.ui.groupBox_objective_response.toggled.connect(lambda checked: self._animate_objrp_groupbox(self.ui.groupBox_objective_response, checked))
        self.ui.groupBox_tumor_control_ratio.toggled.connect(lambda checked: self._animate_tcrat_groupbox(self.ui.groupBox_tumor_control_ratio, checked))

    # Groupbox Utilities
    def _populate_color_comboboxes(self, combo_boxes, available_style_colors: list[str] | None, color_shift = 0):
        """Populate ALL combo boxes with ALL available colors from the current style.

        Args:
            combo_boxes: List of combo box objects to populate. If None, attempts to
                         find combo boxes using default naming convention.
        """

        # Convert to hex
        if not self._is_hex_color(available_style_colors[0]):
            available_style_colors = [self._mpl_code_to_hex(c) for c in available_style_colors]

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
                color_name = f"Color {i + 1} ({color})"
                combo_box.addItem(icon, color_name, userData=color)
            combo_box.setCurrentIndex((count + color_shift) % num_color)
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

    # Initialize GroupBoxes
    def initialize_objective_response_plot_groupbox(self):
        # Update log file
        logger.info('Initializing Experiment View Objective Respoonse Plot Groupbox')
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
        self._populate_color_comboboxes(orc_cboxes, available_style_colors)  # Will need to add color shift
        # self._populate_color_comboboxes(orc_cboxes, available_style_colors, color_shift=2)

        # Set Index
        color_shift = 2  # don't use the first two colors, assuming two arms
        for idx, cbox in enumerate(orc_cboxes):
            cbox.setCurrentIndex(idx + color_shift)

        # Connect pushbutton to update objective response plot
        self.ui.pushButton_objective_response_update.clicked.connect(self.update_study_view)
    def initialize_tumor_control_ratio_groupbox(self):
        # Update log file
        logger.info('Initializing Tumor Control Ratio Plot Groupbox')

        # Define cutoff options
        cutoff_day = 15 # setting to a reasonable value to start
        min_day = 5 # Minimum day set arbitrarily
        max_day_across_studies = 14 # set to a reasonable number
        cutoff_options = [f"Common Across Studies - Day {cutoff_day}", "Full Follow Up", "Fixed"]
        fixed_options = [str(day) for day in range(min_day,max_day_across_studies+1)]
        self.ui.comboBox_tc_cutoff_type.addItems(cutoff_options)
        self.ui.comboBox_tc_cutoff_type.setCurrentIndex(0)
        self.ui.comboBox_tc_cutoff_day.addItems(fixed_options)
        self.ui.comboBox_tc_cutoff_day.setCurrentIndex(len(fixed_options)-1)

        # Error metric
        error_metric_options = ["std", "sem"]
        self.ui.comboBox_tc_ratio_error_metric.addItems(error_metric_options)
        self.ui.comboBox_tc_ratio_error_metric.setCurrentIndex(0)

        # Label Options
        cbox_values = ["True", "False"]
        rotation_options = ["horizontal", "slight", "diagonal", "steep", "vertical" ]
        self.rotation_option_dict = {"horizontal": 0, "slight": 30, "diagonal": 45, "steep": 60, "vertical": 90}
        self.ui.comboBox_tc_ratio_labels_show.addItems(cbox_values)
        self.ui.comboBox_tc_ratio_labels_show.setCurrentIndex(0)
        self.ui.comboBox_tc_ratio_shorten_label.addItems(cbox_values)
        self.ui.comboBox_tc_ratio_shorten_label.setCurrentIndex(1)
        self.ui.comboBox_tc_ratio_labels_rotation.addItems(rotation_options)
        self.ui.comboBox_tc_ratio_labels_rotation.setCurrentIndex(0)

        # Connect response
        self.ui.comboBox_tc_cutoff_type.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_tc_cutoff_day.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_tc_ratio_error_metric.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_tc_ratio_labels_show.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_tc_ratio_labels_rotation.currentTextChanged.connect(self.update_study_view_text)
        self.ui.comboBox_tc_ratio_shorten_label.currentTextChanged.connect(self.update_study_view_text)

    # Update Group Box Parameters
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
    def get_style_colors_2(self):
        # rewrite of generated code to return style colors
        # module = ("Matplotlib", "Science Plots")
        plot_style_module = self.ui.comboBox_plot_style_module.currentText()
        plot_style = self.get_plot_style()

        # Apply the style temporarily to extract colors
        with plt.style.context(plot_style):
            # Get the color cycle from the current style
            prop_cycle = plt.rcParams['axes.prop_cycle']
            colors = prop_cycle.by_key()['color']

        return colors
    def get_style_colors(self):
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
    def update_experiment_view(self):
        # Respond to figure comboBox change
        plot_style = self.get_plot_style()
        self.draw_figure_group(plot_style = plot_style)
    def _populate_color_comboboxes2(self, combo_boxes, available_style_colors, color_shift=2):
        """Populate ALL combo boxes with ALL available colors from the current style.

        Args:
            combo_boxes: List of combo box objects to populate. If None, attempts to
                         find combo boxes using default naming convention.
        """

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
            for i, color in enumerate(self.available_style_colors):
                # Create a colored icon for visual reference
                pixmap = QPixmap(20, 20)
                pixmap.fill(QColor(color))
                icon = QIcon(pixmap)

                # Add to combo box with color name/hex
                color_name = f"Color {i+1} ({color})"
                combo_box.addItem(icon, color_name, userData=color)
            combo_box.setCurrentIndex(count)
            count += 1
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

    # Custom Figure
    def update_study_view(self):
        # Write to log
        logger.info('Updating experiment view')

        # Respond to figure comboBox change
        plot_style = self.get_plot_style()
        self.draw_figure_group(plot_style=plot_style)
    def update_study_view_text(self, *_):
        # Respond to figure comboBox change
        plot_style = self.get_plot_style()
        self.draw_figure_group(plot_style=plot_style)

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

    # Group box animation code (could be consolidated with a dictionary)
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
    def _animate_tcrat_groupbox(self, groupbox: QGroupBox, expanded: bool):
        header_height = groupbox.fontMetrics().height() + 16

        layout = groupbox.layout()
        content_height = layout.sizeHint().height() if layout else 0

        expanded_height = header_height + content_height

        self._gb_tcrat_anim.stop()

        if expanded:
            self._gb_tcrat_anim.setStartValue(groupbox.maximumHeight())
            self._gb_tcrat_anim.setEndValue(expanded_height)
        else:
            self._gb_tcrat_anim.setStartValue(groupbox.maximumHeight())
            self._gb_tcrat_anim.setEndValue(header_height)

        self._gb_tcrat_anim.start()
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
        # Get style information
        updated_style = plot_style

        # Get plot settings
        experiment_id = self.ui.comboBox_configuration_experiments.currentText()
        num_figures = int(self.ui.comboBox_configuration_num_of_plots.currentText())
        experiment_obj = self.tv_data_obj.tumor_vol_experiment_dict[experiment_id]

        # Update each plot
        for idx in range(num_figures):
            # Get Plot Information
            selected_plot = self.plot_select_comboBox[idx].currentText()
            plot_name = self.plotting_function_dict[selected_plot]
            graphic_view = self.graphic_views[idx]

            # Get custom parameters
            custom_params = self.get_custom_parameters(plot_name)

            # Plot Figure
            experiment_obj.plot_to_widget_by_name(plot_name, graphic_view, plot_style = updated_style, **custom_params)

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
        elif plot_name == "proportion_in_objective_response_classification_bar":
            custom_params = self.get_objective_response_group_box_parameters()

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

        # Construct custom parameter dictionary
        custom_params = {"objective_response_colors":
                             {"PD": pd_color, "SD": sd_color, "PR": pr_color,"CR": cr_color},
                         "show_axis_labels": show_axis_labels, "shorten_x_labels": shorten_x_labels}
        return custom_params
    def get_tumor_control_ratio_group_box_parameters(self):
        # Get label parameters
        cutoff_type_str = self.ui.comboBox_tc_cutoff_type.currentText()
        compute_day = int(self.ui.comboBox_tc_cutoff_day.currentText())

        # Set error metric
        error_metric = self.ui.comboBox_tc_ratio_error_metric.addItem(error_metric_options)


        # Get Color parameters
        show_axis_labels =  True if self.ui.comboBox_tc_ratio_labels_show.currentText()=='True' else False
        x_label_rotation_type = self.ui.comboBox_tc_ratio_labels_rotation.currentText()
        x_label_rotation = self.rotation_option_dict[x_label_rotation_type]
        shorten_x_labels = self.ui.comboBox_tc_ratio_shorten_label.currentText()

        # Construct custom parameter dictionary
        custom_params = {"compute_day": compute_day, "error_metric": error_metric, "show_axis_labels": show_axis_labels,
                         "x_label_rotation": x_label_rotation, "shorten_x_labels": shorten_x_labels}
        return custom_params


