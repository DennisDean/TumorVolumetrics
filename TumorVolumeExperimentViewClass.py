# Code for displaying a tumor experiment pllots

# Set up a module-level logger
import logging
logger = logging.getLogger(__name__)

# Extend Existing Class
from FigureGraphicsViewClass import FigureGraphicsView

# Import
from PySide6.QtWidgets import QMainWindow, QGraphicsView, QSizePolicy

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

# GUI Class
class TumorVolumeExperimentWindow(QMainWindow):
    # Intitialize
    def __init__(self, tv_data_obj:TumorVolumeDataClass , parent=None):
        super().__init__(parent)

        # Setup and Draw Window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tumor Volume File")

        # Show plotting configuration layout
        self.ui.actionPlot_Configuration.triggered.connect(self.toggle_graph_configuration_group)
        set_layout_visible(self.ui.verticalLayout_visual_graph_settings, True)

        # Save data object
        self.tv_data_obj = tv_data_obj

        # Get Experiments
        self.experiments = tv_data_obj.unique_experiments
        self.ui.comboBox_configuration_experiments.addItems(self.experiments)

        # Set plot configurations
        self.initial_configuration = '4'
        self.plot_config_to_index = lambda x: int(x)-1
        self.num_of_plot_option_list = ['1','2','3','4']
        self.graphic_view_plot_dict = {'1':[True, False, False, False], '2':[True, True, False, False],
                                       '3':[True, True, True, False],   '4':[True, True, True, True]}
        self.ui.comboBox_configuration_num_of_plots.addItems(self.num_of_plot_option_list)
        self.ui.comboBox_configuration_num_of_plots.setCurrentIndex(self.plot_config_to_index(self.initial_configuration))
        self.ui.comboBox_configuration_num_of_plots.currentTextChanged.connect(self.toggle_plot_graphics_view)

        # Overide Graphic View to Support Context Menus (Right Click)
        self.graphicsView_visual_top_left: QGraphicsView | None = None
        self.graphicsView_visual_top_right: QGraphicsView | None = None
        self.graphicsView_visual_bottom_left: QGraphicsView | None = None
        self.graphicsView_visual_bottom_right: QGraphicsView | None = None
        self.original_graphics_views: QGraphicsView | None = None
        self.add_context_menu_support_to_graphic_view()

        # Setup plotting
        self.plot_types:                list|None = None
        self.plot_select_comboBox:      list|None = None
        self.plotting_functions:        list|None = None
        self.experiment_graphics_views: list|None = None
        self.initialize_plotting()

        # Initialize style sheet
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
        self.plot_style_module:str|None = None
        self.plot_matplotlib_style:str|None = None
        self.plot_scienceplot_journal:str|None = None
        self.plot_scienceplot_color:str|None = None
        self.plot_scienceplot_grid:str|None = None
        self.initialize_style_sheets_functions()

    # Inititialize Utilities
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
        self.ui.groupBox_plot_style_sheet.toggled.connect(self.toggle_plot_style_group)
        self.ui.groupBox_plot_configurations.toggled.connect(self.toggle_plot_configureation_group)

        # Connect plot style selection
        self.ui.pushButton_plot_uodate_style.clicked.connect(self.update_plot_style)

    # Update Figure
    def update_experiment_view(self, plot_style = None):
        # Respond to figure comboBox change
        self.draw_figure_group(plot_style = plot_style)
    def update_plot_style(self):
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
        else:
            logger.info(f'Plot style module not supported: {self.plot_style_module }')
            return

        # Update figures
        self.update_experiment_view(plot_style = plot_style)

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
    def toggle_plot_style_group(self, checked):
        set_layout_visible(self.ui.verticalLayout_plot_style_group, checked)
        if checked == True:
            plot_style_selection = self.ui.comboBox_plot_style_module.currentIndex()
            self.toggle_style_widgets(bool(plot_style_selection))
    def toggle_plot_configureation_group(self, checked):
        set_layout_visible(self.ui.verticalLayout_plot_configuration, checked)

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
            selected_plot = self.plot_select_comboBox[idx].currentText()
            plot_name = self.plotting_function_dict[selected_plot]
            graphic_view = self.graphic_views[idx]
            experiment_obj.plot_to_widget_by_name(plot_name, graphic_view, plot_style = updated_style)



