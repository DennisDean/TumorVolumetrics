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