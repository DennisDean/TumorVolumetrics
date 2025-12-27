# Code for displaying a tumor experiment pllots

#TODO: Semantic color coding of objective response with gray and blue tones
#TODO: Check with a dataset that contains multuple experiments

# Set up a module-level logger
import logging
logger = logging.getLogger(__name__)

# Extend Existing Class
from FigureGraphicsViewClass import FigureGraphicsView

# Import

# Plotting
import matplotlib as mpl
import matplotlib.pyplot as plt

# Interface
from PySide6.QtWidgets import QMainWindow, QGraphicsView, QSizePolicy, QGroupBox
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

        # Setup and Draw Window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tumor Volume Study")

        # Show plotting configuration layout
        initial_configuration_show_status = False
        self.ui.actionPlot_Configuration.triggered.connect(self.toggle_graph_configuration_group)
        set_layout_visible(self.ui.verticalLayout_visual_graph_settings, initial_configuration_show_status)

        # Save data object
        self.tv_data_obj = tv_data_obj

        # Get Studies
        self.studies = tv_data_obj.unique_studies
        self.ui.comboBox_configuration_study.addItems(self.studies)

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

        # Check if Latex is avaialble
        self.use_latex = latex_available()

        # Set up group boxes
        self._gb_animation:QPropertyAnimation|None = None
        self.initialize_collapsable_group_boxes()

        # Initialize objection response plot
        self.available_style_colors = None
        self.initialize_objective_response_plot_groupbox()

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
        self.ui.comboBox_configuration_study.currentTextChanged.connect(self.update_study_view)
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

        # Set checked
        self.ui.groupBox_plot_configurations.setChecked(True)
        self.ui.groupBox_plot_style_sheet.setChecked(False)
        self.ui.groupBox_objective_response.setChecked(False)

        # Set initial group box settings
        group_boxes = [self.ui.groupBox_plot_configurations, self.ui.groupBox_plot_style_sheet, self.ui.groupBox_objective_response]
        init_group_box_state = [True, False, False]
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
    def initialize_objective_response_plot_groupbox(self):
        # Get current style color selection
        available_style_colors = self.get_style_colors()
        orc_cboxes = [self.ui.comboBox_objective_plot_pd, self.ui.comboBox_objective_plot_sd,
                      self.ui.comboBox_objective_plot_pr, self.ui.comboBox_objective_plot_cr]
        self._populate_color_comboboxes(orc_cboxes, available_style_colors)
        self.available_style_colors = available_style_colors

        # Connect pushbutton to update objective response plot
        self.ui.pushButton_objective_response_update.clicked.connect(self.update_objective_response_bar_plot)

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
    def update_study_view(self):
        # Respond to figure comboBox change
        plot_style = self.get_plot_style()
        self.draw_figure_group(plot_style = plot_style)
    def update_plot_style(self):
        # Update figures
        plot_style = self.get_plot_style()
        self.update_study_view()
        self._recompute_groupbox_height(self.ui.groupBox_plot_style_sheet)

        # Update Objective Response Plot Options
        combo_boxes = [self.ui.comboBox_objective_plot_pd, self.ui.comboBox_objective_plot_sd,
                       self.ui.comboBox_objective_plot_pr, self.ui.comboBox_objective_plot_cr]
        available_style_colors = self.get_style_colors()
        self._populate_color_comboboxes(combo_boxes, available_style_colors)
    def _populate_color_comboboxes(self, combo_boxes, available_style_colors):
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

    # Custom Figure
    def update_objective_response_bar_plot(self):
        # Create new dictionary
        current_colors = self.get_style_colors_2()
        pd_color = current_colors[self.ui.comboBox_objective_plot_pd.currentIndex()]
        sd_color = current_colors[self.ui.comboBox_objective_plot_sd.currentIndex()]
        pr_color = current_colors[self.ui.comboBox_objective_plot_pr.currentIndex()]
        cr_color = current_colors[self.ui.comboBox_objective_plot_cr.currentIndex()]

        # Create new color dictionary
        objective_response_color_dict = {'PD':pd_color, 'SD':sd_color, 'PR':pr_color, 'CR':cr_color}
        self.tv_data_obj.objective_response_colors = objective_response_color_dict.copy()

        # Check if Objective Response Curve is present
        updated_style = self.get_plot_style()
        selected_plot_cbox  = [self.ui.comboBox_configuration_plot_upper_left, self.ui.comboBox_configuration_plot_upper_right,
                               self.ui.comboBox_configuration_plot_lower_left, self.ui.comboBox_configuration_plot_lower_right]
        selected_gviews = [self.graphicsView_visual_top_left,    self.graphicsView_visual_top_right,
                           self.graphicsView_visual_bottom_left, self.graphicsView_visual_bottom_right]
        for splot_cbox, s_gview in zip(selected_plot_cbox, selected_gviews):
            plot_name = splot_cbox.currentText()
            if plot_name == 'Objective_Response_Bar':
                experiment_name = self.ui.comboBox_configuration_experiments.currentText()
                plot_function_name = self.plotting_function_dict[plot_name]
                experiment_obj = self.tv_data_obj.tumor_vol_experiment_dict[experiment_name]
                experiment_obj.plot_to_widget_by_name(plot_function_name, s_gview, plot_style=updated_style,
                    objective_response_color_dict = objective_response_color_dict)

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
        study_id = self.ui.comboBox_configuration_study.currentText()
        num_figures = int(self.ui.comboBox_configuration_num_of_plots.currentText())
        study_obj = self.tv_data_obj.tumor_vol_study_dict[study_id]

        # Update each plot
        for idx in range(num_figures):
            selected_plot = self.plot_select_comboBox[idx].currentText()
            plot_name = self.plotting_function_dict[selected_plot]
            graphic_view = self.graphic_views[idx]
            study_obj.plot_to_widget_by_name(plot_name, graphic_view, plot_style=updated_style)



