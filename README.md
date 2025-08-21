# CBE Clima Tool

The CBE Clima Tool is a web-based application built to support climate analysis specifically designed to support the need of architects and engineers interested in climate-adapted design. It can be freely accessed at [clima.cbe.berkeley.edu](http://clima.cbe.berkeley.edu).

It allows users to analyze the climate data of more than 27,500 locations worldwide from both [Energy Plus](https://energyplus.net/weather) and [Climate.One.Building.org](http://climate.onebuilding.org/). You can, however, also choose to upload your own EPW weather file.

Our tool can be used to analyze and visualize data contained in EnergyPlus Weather (EPW) files. It furthermore calculates a number of climate-related values (i.e. solar azimuth and altitude, Universal Thermal Climate Index (UTCI), comfort indices, etc.) that are not contained in the EPW files but can be derived from the information therein contained.

## Key Features

*   **Interactive Climate Analysis:** Visualize EPW weather data through a variety of interactive charts.
*   **Extensive Weather Data:** Access weather files for over 27,500 locations from EnergyPlus and Climate.One.Building.org.
*   **Custom Data Upload:** Analyze your own custom `.epw` weather files.
*   **Advanced Calculations:** Computes derived metrics like solar positions, UTCI, and various thermal comfort indices.
*   **Data Export:** Download charts, data, and psychrometric chart overlays.

## Documentation

The official documentation for the tool can be found [here](https://center-for-the-built-environment.gitbook.io/clima/).

## Citation

If you use this tool in your research or work, please cite our paper:

Betti, G., Tartarini, F. & Schiavon, S. CBE Clima Tool: a free and open-source web application for climate analysis for architects and building engineers. *Build. Simul.* (2023). https://doi.org/10.1007/s12273-023-1090-5

## Getting Support

For any questions, feedback, or bug reports, please use the [GitHub Discussions](https://github.com/CenterForTheBuiltEnvironment/clima/discussions) section.

## Authors
* [Giovanni Betti](https://www.linkedin.com/in/gbetti/)
* [Federico Tartarini](https://www.linkedin.com/in/federico-tartarini-3991995b/)
* [Christine Nguyen](https://chrlng.github.io/)

## Built with

* [Dash](https://plotly.com/dash/) - Main web framework
* [Plotly Python](https://plotly.com/python/) - Interactive scientific graphing
* [Pandas](https://pandas.pydata.org/) - Data analysis and manipulation
