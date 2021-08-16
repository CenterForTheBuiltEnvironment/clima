
## CHANGELOG

---

### Version 0.4.3 (2021-08-16)

Fix:

- app was crashing is Koppen data was not available
- displaying elevation correctly

Features:

- displaying info on reference years used to create EPW file
- added labels to some chart
- pop up modal now shows weather station name

### Version 0.4.2 (2021-07-22)

Fix:

- display error if no data are available to plot
- saving charts with their unique names 

Features:

- added more variables to plot in psy and explore tabs
- user can now invert hour and month selection

### Version 0.4.1 (2021-07-08)

Fix:

- issue with natural ventilation heatmap chart
- title heatmap natural ventilation tab

Features:

- added checkbox in apply filter dew point temperature
- changed order outdoor and natural ventilation tab
- natural ventilation tab charts have now a constant y range

### Version 0.4.0 (2021-07-06)

Features:

- created natural ventilation tab

### Version 0.3.2 (2021-07-06)

Fix:

- meta is now a dictionary

Features:

- user can download both the EPW and the Clima df
- improved data explorer tab
- outdoor tab added images
- violin plots in climate summary now updates as function of range selected
- discrete color bar UTCI thermal stress

### Version 0.3.0 (2021-07-02)

Fix:

- issues in psychrometric chart tab
- changed Flask cache type

Features:

- added more links to EPW files ([source](http://climate.onebuilding.org/))
- improved layout wind tab
- changed order tabs
- added month name in yearly chart
- set local range as the default one

### Version 0.2.1 (2021-06-23)

Fix:

- added Koppen-Geiger climate classification
- tooltip is now correctly displaying

Features:

- added heating and cooling degree days chart
- successfully implemented continuous deployment
- improved the layout of the application
- figures have now narrower white margins

### Version 0.2.0 (2021-06-23)

Fix:

- callback error in select tab - the callback was not returning an output
- tabs are disabled until data is uploaded
- changed the name of chart when downloaded
- added LICENSE file

Features:

- improved loading speed of temperature and RH tab
- user can upload a custom EPW file
- user can select and EPW directly from the map
- user can download the underlying data used to create charts
- removed natural ventilation tab
- removed input URL EPW
- psychrometric chart shows frequency of occurrence

### Version 0.1.1 (2021-06-21)

Features:

- Changed look of the footer
- Added CHANGELOG

### Version 0.1.0 (2021-06-14)

Features:

- Reduced loading time
- Fixed errors
- EPW data loaded persist even if the user navigates back to main page
- The URL in `select weather file` persists, user choice is kept in memory