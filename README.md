# Tumor Volumetrics

**Tumor Volumetrics** is an early-stage Python application for loading, validating, analyzing, summarizing, and visualizing tumor volume time series data.
The repository currently includes the foundations of a data access layer and specialized classes for working with tumor growth measurements.

The motivation is to have a framwork for quickly integrating new advance methods for use on existing data sets. We expect the python code will enable statsitician and engineers to quickly test and deploy methods under development.

The first component under development is the *[TumorVolumeTimeSeriesClass](media/TumorVolumeClassReadMe.md)*, which enables users to verify their data, inspect metadata, and generate basic plots of tumor volume and optional weight over time. As the project matures, additional modules for data QC, normalization, group-level summaries, and interactive visualization will be added.

This repository is under active development and does not yet represent a stable API. More features, documentation, and examples will follow.

## Features (in progress)

- Load tumor volume datasets from CSV files
- Creation of individual tumor time-series objects
- Creation of tumor volume study objects
- Creattion of tumor volume experiment objects
- Graphic user interface for interactively visualizing and analyuzing tumor volume data

## Figure Examples

<p align="center">    
<img src="media/spider_with_weights.png" /><br>
<b>Figure.</b> Tumor volume spider plots with weights shown as a subplot.
</p>

<p align="center">    
<img src="media/tumor_volume_average_with_std.png" /><br>
<b>Figure.</b> Average tumor volume curves with standard deviation shown.
</p>

<p align="center">    
<img src="media/kaplan_meier_with_at_risk_plot_table.png" /> <br>
<b>Figure.</b> Event Free Kaplan Meier curve with at risk shown.
</p>

<p align="center">    
<img src="media/tumor_volume_change_as_objective_response.png" /><br>
<b>Figure.</b> Change in tumor volume plotted as objectiv response.
</p>

## Roadmap

The plan is to create a PySide6 interface that will allow for interactive review of analysis of tumor volume data. Interactive analysis will support a range of researchers during the data collection, analysis, and publishing stages. The application will include the most common starting analysis. We expect it will be stratight forward for those with appropraite experience to add less commonly used figures and analytsis. 

The starting point will use existing flat file formats. We expect to develop an XML format that will allow for additiona information to be included such as location of the genomics data. 

A major feature of the application will be the ability to export publication quality features and to reapidly configures figure properties. We expect supporting figure foramting will enable a wide range of users to customize figures according to group standards. 

Future updates will include:
- Expanded plotting aesthetics
- Quality control checks for raw data
- Enhanced statistical summaries
- Interactive visualization tools

Optional collaboration once the application is fully developed

## License

This project is [licensed](LICENSE.md) under the GNU Affero General Public License v3.0.
See the LICENSE.md file for details.