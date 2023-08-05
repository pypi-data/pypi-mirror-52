=======
History
=======

1.2.0 (2019-09-11)
==================

- Added test utility setup_test_raster() to make unit testing easier.

1.1.0 (2019-08-23)
==================

- Added option "version" to PointTimeseries.get_cached() so that it can
  save in different file format versions.

1.0.1 (2019-08-22)
==================

- Fixed a bug in extract_point_from_timeseries() where it was sometimes
  raising the wrong exception type (depending on GDAL version).

1.0.0 (2019-08-16)
==================

- The API for extract_point_timeseries_from_rasters() has changed.
  Instead of a function, there's now a PointTimeseries class.
- When extracting a point timeseries from rasters, start_date and
  end_date can now be specified.

0.2.0 (2019-08-13)
==================

- When extracting point time series from a set of rasters, it is now
  possible to provide a prefix as well as a list of files, and it is
  also possible to save the extracted time series to a file, optionally
  only if the file is outdated.
- extract_point_from_raster (and extract_point_timeseries_from_rasters)
  now supports GeoDjango (GEOS) Point objects besides GDAL Point
  objects.
- Function coordinates2point has been added.

0.1.2 (2019-07-30)
==================

- Fixed a bug where hts files were opened in the wrong mode, with
  inconsistent results.

0.1.1 (2019-07-05)
==================

- Fixed an ugly timezone bug that caused the data to refer to a
  different time than what the timestamp actually said.
- When the timezone was missing from the input files, there was an
  incomprehensible AttributeError. This was fixed and now it provides an
  understandable error message.

0.1.0 (2019-06-21)
==================

- Initial release
