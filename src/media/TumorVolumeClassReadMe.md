# TumorVolumeClass Read Me

A Python module for loading, analyzing, and visualizing tumor volume time-series data from patient-derived xenograft (PDX) studies.

## Overview

This tool provides a comprehensive framework for working with tumor volume data, enabling researchers to:

* Load and organize multi-arm preclinical study data
* Analyze individual tumor growth curves and study-level metrics
* Generate publication-ready visualizations with customizable styles
* Compute objective response classifications (CR/PR/SD/PD)
* Perform survival analysis and statistical comparisons
* Support both standalone plotting and Qt widget integration

## Features

### Data Management

* CSV and XML data loading with automatic validation
* Hierarchical organization: Individual time series → Studies → Experimental groups
* Metadata tracking: Arms, contributors, PDX IDs, disease types
* XML Schema Definition (XSD) support for structured data exchange

### Analysis Capabilities

* Area Under the Curve (AUC) calculations (raw and normalized)
* Percent change and proportional volume change metrics
* Objective response classification (Complete/Partial Response, Stable/Progressive Disease)
* Event-free survival analysis with Kaplan-Meier curves
* Log-rank statistical testing
* T/C (Treatment/Control) ratio calculations with standard error
* Log2 fold-change analysis with confidence intervals

### Visualizations

**Time Series Plots:**
* Individual plots: Time series with tumor volume and weight
* Spider plots: Multi-arm studies with individual and aggregate curves
* Customizable data transformations (percent change, log2, etc.)

**Study-Level Plots:**
* Bar charts: AUC and tumor volume change comparisons
* Survival curves: Event-free survival with at-risk tables
* Waterfall plots: Objective response by treatment arm

**Experiment-Level Plots:**
* Average AUC across studies (with control/treatment separation)
* Average tumor volume change across studies
* Log2 fold-change point plots
* T/C ratio comparisons
* Objective response proportion (stacked bar charts)

### New Features (Latest Update)

#### Enhanced Plotting System
* **Matplotlib Style Support**: All plotting functions now support custom matplotlib styles (e.g., 'dark_background', 'seaborn-v0_8', 'ggplot')
* **Qt Widget Integration**: Seamless embedding of plots into PySide6 applications
* **Dual-Mode Operation**: Functions work both as standalone matplotlib figures and embedded Qt widgets
* **Consistent Style Application**: Theme colors automatically applied to all plot elements

#### Advanced Plot Customization
* Configurable x-axis label rotation
* Optional label shortening (remove alpha characters)
* Show/hide axis labels independently
* Customizable legends and annotations
* Error bar styles (standard error or error bars with caps)

#### Study Analysis Enhancements
* Configurable objective response color schemes
* Flexible compute-day specification for all metrics
* Enhanced survival analysis with customizable risk tables
* Improved data aggregation at exact time points

#### Standardized Plot Interface
* Unified parameter structure across all plotting functions
* `plotting_function_dict_2` for programmatic plot generation
* Plot-by-name functionality for dynamic visualization

## Quick Start

```python
from tumor_volume import TumorVolumeDataClass

# Load data
tvd = TumorVolumeDataClass()
tvd.load_tmz_csv("your_data.csv")

# Summarize dataset
tvd.write_file_summary_text()

# Plot individual time series
pdx_id = tvd.unique_pdx_ids[0]
tvd.tumor_vol_time_series_dict[pdx_id].plot()

# Visualize study with spider plot
study = tvd.unique_studies[0]
tvd.tumor_vol_study_dict[study].plot_spider(
    show_individual=True,
    show_aggregate=True,
    aggregate_sem=True
)

# Generate survival curves
tvd.tumor_vol_study_dict[study].plot_event_free_survival(delta=1.0)

# Plot experiment-level analysis
experiment = tvd.unique_experiments[0]
tvd.tumor_vol_experiment_dict[experiment].plot_auc_with_controls_bar()
```

## Advanced Usage

### Custom Matplotlib Styles

```python
# Apply dark theme
study_obj.plot_spider(
    plot_style='dark_background',
    show_individual=True,
    show_aggregate=True
)

# Apply multiple styles
study_obj.plot_spider(
    plot_style=['seaborn-v0_8-darkgrid', 'seaborn-v0_8-poster'],
    show_individual=True
)
```

### Qt Widget Integration

```python
# Embed plot in Qt widget
study_obj.plot_spider(
    parent_widget=my_qt_widget,
    plot_style='dark_background',
    show_individual=True,
    show_aggregate=True
)

# Access the canvas for further manipulation
canvas = study_obj.current_tumor_volume_canvas
```

### Dynamic Plot Generation

```python
# Generate plot by name
experiment_obj.plot_to_widget_by_name(
    "plot_average_tumor_volume_change_bar",
    parent_widget=graphic_view,
    plot_style='seaborn-v0_8',
    error_metric="sem",
    show_axis_labels=True
)
```

## Data Format

### CSV Format
CSV files should include these columns:
* `contributor`, `arms`, `times`, `volume`, `experiment`
* `study`, `id`, `tumor`, `disease_type`
* `body_weight`, `matched_controls`

### XML Format
The module supports XML data following a hierarchical structure:
* Contributors → Disease Types → Experiments
* Experiments → Studies → Arms → Tumor Volume Curves
* Measurements with time/volume/weight data

## Requirements

* Python 3.7+
* pandas, numpy, scipy
* matplotlib
* lifelines (for survival analysis)
* PySide6 (for Qt widget integration, optional)
* lxml (for XML validation, optional)

## Figure Examples
**Figure section under construction**

### Time Series Class Figures

* Figure 1. Example tumor volume plot
* Figure 2. Example tumor volume plot with weights subplot
<!-- Figure 1 -->
<p style="text-align: center;">
  <img src="src/media/tumor_volume_time_series.png"
       alt="Example tumor volume plot"><br>
  <strong>Figure 1.</strong>
  Example tumor volume plot.
</p>
<!-- Figure 2 -->
<p style="text-align: center;">
  <img src="src/media/tumor_volume_time_series_with_weight.png"
       alt="Example tumor volume plot with weights subplot"><br>
  <strong>Figure 2.</strong>
  Example tumor volume plot with weights subplot.
</p>

### Study Class Figures
* Figure 3. Tumor volume spider plot
* Figure 4. Tumor volume spider plots with weights shown as subplot
* Figure 5. Tumor volume spider plot with just time series data
* Figure 6. Event Free Kaplan Meier curve
* Figure 7. Event Free Kaplan Meier curve with at-risk table
* Figure 8. Common tumor volume transformations
* Figure 9. Area under the Tumor Volume Curve
* Figure 10. Change in tumor volume as percentage
* Figure 11. Change in tumor volume plotted as objective response

<!-- Figure 3 -->
<p style="text-align: center;">
  <img src="src/media/spider.png"
       alt="Tumor volume spider plot"><br>
  <strong>Figure 3.</strong>
  Example tumor volume plot.
</p>
<!-- Figure 4 -->
<p style="text-align: center;">
  <img src="src/media/spider_with_weights.png"
       alt="Tumor volume spider plots with weights shown as subplot"><br>
  <strong>Figure 4.</strong>
  Tumor volume spider plots with weights shown as subplot.
</p>
<!-- Figure 5 -->
<p style="text-align: center;">
  <img src="src/media/spider_time_series_only.png"
       alt="Tumor volume spider plot with just time series data"><br>
  <strong>Figure 5.</strong>
  Tumor volume spider plot with just time series data.
</p>
<!-- Figure 6 -->
<p style="text-align: center;">
  <img src="src/media/kaplan_meier.png"
       alt=""><br>
  <strong>Figure 6.</strong>
  Event Free Kaplan Meier curve.
</p>
<!-- Figure 7 -->
<p style="text-align: center;">
  <img src="src/media/kaplan_meier_with_at_risk_plot_table.png"
       alt=""><br>
  <strong>Figure 7.</strong>
  Event Free Kaplan Meier curve with at-risk table.
</p>
<!-- Figure 8 -->
<table align="center">
  <tr>
    <td style="text-align: center;">
      <img src="src/media/transform_spider_1.png" width=500 alt=""><br>
      <strong>Figure 8a.</strong> Tumor Volume.
    </td>
    <td style="text-align: center;">
      <img src="src/media/transform_spider_2.png"  width=500 alt=""><br>
      <strong>Figure 8b.</strong> Percent Change.
    </td>
  </tr>
  <tr>
    <td style="text-align: center;">
      <img src="src/media/transform_spider_3.png"  width=500 alt=""><br>
      <strong>Figure 8c.</strong> Log 2 change.
    </td>
    <td style="text-align: center;">
      <img src="src/media/transform_spider_4.png"  width=500 alt="src/media/transform_spider_4.png"><br>
      <strong>Figure 8d.</strong> Progression/Regression.
    </td>
  </tr>
</table>
<!-- Figure 9 -->
<p style="text-align: center;">
  <img src="src/media/tumor_volume_auc.png"
       alt=""><br>
  <strong>Figure 9.</strong>
  Area Under the Curve by ARM (control and treatment).
</p>
<!-- Figure 10 -->
<p style="text-align: center;">
  <img src="src/media/tumor_volume_change_with legend.png"
       alt="Change in tumor volume as percentage"><br>
  <strong>Figure 9.</strong>
  Change in tumor volume as percentage.
</p>
<!-- Figure 11 -->
<p style="text-align: center;">
  <img src="src/media/tumor_volume_change_as_objective_response.png"
       alt="Change in tumor volume plotted as objective response"><br>
  <strong>Figure 11.</strong>
  Change in tumor volume plotted as objective response.
</p>


### Experiment Class Figures
* Figure 12. Percent tumor volume change across studies
* Figure 13. Log2 fold-change across studies
* Figure 14. Average AUC across studies (control vs treatment)
* Figure 15. T/C Ratio across studies
* Figure 16. Objective response proportion across studies

<!-- Figure 12 -->
<p style="text-align: center;">
  <img src="src/media/percent_tumor_volume_change_across_studies.png"
       alt="Percent tumor volume change across studies"><br>
  <strong>Figure 12.</strong>
  Percent tumor volume change across studies.
</p>
<!-- Figure 13 -->
<p style="text-align: center;">
  <img src="src/media/log2_change_across_studies.png"
       alt="Log2 fold-change across studies"><br>
  <strong>Figure 13.</strong>
  Log2 fold-change across studies.
</p>
<!-- Figure 14 -->
<p style="text-align: center;">
  <img src="src/media/average_auc_across_studies.png"
       alt="Average AUC across studies (control vs treatment)"><br>
  <strong>Figure 14.</strong>
  Average AUC across studies (control vs treatment).
</p>
<!-- Figure 15 -->
<p style="text-align: center;">
  <img src="src/media/TC_ratio_across_studies.png"
       alt="T/C Ratio across studies"><br>
  <strong>Figure 15.</strong>
  T/C Ratio across studies.
</p>
<!-- Figure 16 -->
<p style="text-align: center;">
  <img src="src/media/objective_response_distribution_across_studies.png"
       alt="Objective response proportion across studies"><br>
  <strong>Figure 16.</strong>
  Objective response proportion across studies.
</p>

## Acknowledgements

The structure of the Python code benefited from the experience and contributions of the PDXNet community. Discussions during the process of writing the following publications were highly influential in shaping the code written for this application:

- **Systematic Establishment of Robustness and Standards in Patient-Derived Xenograft Experiments and Analysis**, *Cancer Res* (2020) 80 (11): 2286–2297  
- **PDXNet portal: patient-derived Xenograft model, data, workflow and tool discovery**, *NAR Cancer*, Volume 4, Issue 2, June 2022  
- **Assessment of Patient-Derived Xenograft Growth and Antitumor Activity: The NCI PDXNet Consensus**, *Mol Cancer Ther* (2024) 23 (7): 924–938  

We gratefully acknowledge all members of the PDXNet community for their valuable feedback, discussions, and insights that informed both the design and implementation of this application.

## License

This project is licensed under the GNU Affero General Public License v3.0. See the LICENSE.md file for details.