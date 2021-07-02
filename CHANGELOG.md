
## CHANGELOG

---

### Version 0.3.0 (2021-0/-02)

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