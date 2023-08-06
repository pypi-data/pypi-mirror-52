=======
History
=======

Unreleased
----------

* BUGFIX: Provides a helpful error message when `geckoview_datapoint` is used on an metric type that doesn't support GeckoView exfiltration.

* Generate a lookup table for Gecko categorical histograms in `GleanGeckoMetricsMapping`.

1.4.1 (2019-08-28)
------------------

* Documentation only.

1.4.0 (2019-08-27)
------------------

* Added support for generating markdown documentation from `metrics.yaml` files.

1.3.0 (2019-08-22)
------------------

* `quantity` metric type has been added.

1.2.1 (2019-08-13)
------------------

* BUGFIX: `includeClientId` was not being output for PingType.

1.2.0 (2019-08-13)
------------------

* `memory_distribution` metric type has been added.

* `custom_distribution` metric type has been added.

* `labeled_timespan` is no longer an allowed metric type.

1.1.0 (2019-08-05)
------------------

* Add a special `all_pings` value to `send_in_pings`.

1.0.0 (2019-07-29)
------------------

* First release to start following strict semver.

0.1.0 (2018-10-15)
------------------

* First release on PyPI.
