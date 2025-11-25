# Tumor Volumetrics

**Tumor Volumetrics** is an early-stage Python application for loading, validating, analyzing, summarizing, and visualizing tumor volume time series data.
The repository currently includes the foundations of a data access layer and specialized classes for working with tumor growth measurements.

The first component under development is the *TumorVolumeTimeSeriesClass*, which enables users to verify their data, inspect metadata, and generate basic plots of tumor volume and optional weight over time. As the project matures, additional modules for data QC, normalization, group-level summaries, and interactive visualization will be added.

This repository is under active development and does not yet represent a stable API. More features, documentation, and examples will follow.

## Features (in progress)

- Load tumor volume datasets from CSV files
- Automatic column name sanitization
- Creation of individual tumor time-series objects
- Summary utilities for contributors, studies, and model identifiers
- Initial plotting support for tumor volume and weight
- Logging framework for debugging and data validation


<p align="center">    
<img src="media/tumor_volume.png" /><br>
<b>Figure 1.</b> Example tumor volume plot.
</p>

<p align="center">    
<img src="media/tumor_volume_and_weight.png" width="600" /><br>
<b>Figure 2.</b> Example tumor volume plot with weights subplot.
</p>

<p align="center">    
<img src="media/spider.png"  /><br>
<b>Figure 3.</b> Tumor volume spider plot.
</p>

<p align="center">    
<img src="media/spider_with_weights.png" width="600" /><br>
<b>Figure 4.</b> Tumor volume spider plots with weights shown as a subplot.
</p>

<p align="center">    
<img src="media/tumor_volume_average_with_std.png" width="600" /><br>
<b>Figure 5.</b> Average tumor volume curves with standard develation shown.
</p>


<p align="center">    
<img src="media/kaplan_meier.png" /><br>
<b>Figure 6.</b> Event Free Kaplan Meier curve.
</p>

<p align="center">    
<img src="media/kaplan_meier_with_at_risk_plot_table.png" width="600" /><br>
<b>Figure 7.</b> Event Free Kaplan Meier curve with at risk shown.
</p>

## Roadmap

Future updates will include:
- Expanded plotting aesthetics
- Quality control checks for raw data
- Enhanced statistical summaries
- Interactive visualization tools

Optional collaboration once the application is fully developed

## License

This project is [licensed](LICENSE.md) under the GNU Affero General Public License v3.0.
See the LICENSE.md file for details.