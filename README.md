# WeatherAnalyzer
A simple weather data viewing tool

![Preview](https://github.com/ibotforwin/WeatherAnalyzer/blob/master/media/demo.png)

# Versions
* Django 3.x
* Python 3.x

# Key Python libraries
* django_tables2
* plotly

# Front-End Functionality
## Upload CSV file
* Files from [weather website](https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=51459) accepted
  
## Date Picker
* On upload
  * Load to date range of data available in the CSV
* On change
  * Update table and graph data to represent selected date range
  
## Table
* Select/Deselect Checkboxes
  * "Update Columns" updates the table data to represent selected checkboxes only

## Graph
* Select/Deselect Lines
  * Graph adds/removes appropriate lines
  
## Export CSV/JSON
* Downloads CSV/JSON file with current table values

# Back-End Functionality
* File Validation
  * Check file extension
  * Check number of columns
  * Check column titles
