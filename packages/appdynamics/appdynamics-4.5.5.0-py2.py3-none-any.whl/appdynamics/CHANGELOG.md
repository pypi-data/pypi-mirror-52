# Change Log

This is the Python Agent for AppDynamics.

## [4.5.5.0] - 2019-09-11
### Fixed
 - DLNATIVE-2769 redis interceptor works with redis-py versions >= 3.3.0


## [4.5.4.0] - 2019-08-12
### Fixed
 - DLNATIVE-2217 fixes snapshotting for Django's lazily loaded objects


## [4.5.3.0] - 2019-07-31
### Changed
 - DLNATIVE-2712 added automated integration tests for latest django(2.2) and flask(1.0) versions


## [4.5.2.0] - 2019-07-15
### Changed
 - DLNATIVE-2438 updated java proxy to remove dependencies on libraries with known security vulnerabilities.


## [4.5.1.0] - 2019-02-08
### Added
 - DLNATIVE-1421 Add support for CPython3.7

### Changed
 - DLNATIVE-2279 Removed support for CPython3.3 (EOL was 2017-09-29)


## [4.5.0.0] - 2018-07-11
### Changed
 - DLNATIVE-1668 Upgraded the agent versin from 4.3 to 4.5
 - BARE-1389 Migrate code sign agent used in pipeline to aws


## [4.3.18.0] - 2018-05-25
### Added
 - DLNATIVE-1577 python 2.6 deprecated


## [4.3.17.0] - 2018-03-08
### Added
 - DLNATIVE-1329 Added support for Django 2.0


## [4.3.16.0] - 2017-11-07
### Added
 - DLNATIVE-970 Auto-update changelog on release


## [4.3.14.0] - 2017-10-24
### Fixed
 - DLNATIVE-941 Allow custom cursor classes to be passed to `Connection.cursor` method in psycopg2


## [4.3.12.0] - 2017-09-14
### Fixed
 - DLNATIVE-782 Agent now continues to report metrics if Java proxy is restarted
 - DLNATIVE-830 Fix event in 'wait_for_bt_info_response' which always timed out


## [4.3.10.0] - 2017-08-28
### Changed
 - Agent reports its own version number and the proxy version to the controller
 - Exceptions in the transaction service are handled gracefully

### Fixed
 - DLNATIVE-637 Fixed crash when tornado.httpclient.fetch is passed kwargs


## [4.3.8.0] - 2017-08-10
### Added
 - Agent now installs and runs on CPython 3.5 and 3.6

### Fixed
 - Agent now runs on all CPython 2.x ABI versions on OSX
 - Fix agent install dependencies for py3 on linux


## [4.2.15.0] - 2017-03-16
### Added
 - OOTB instrumentation for cx_Oracle

### Changed
 - tornado.httpclient interceptor now works on all tornado versions >= 3.2


## [4.2.14.0] - 2017-02-22
### Added
 - Support for mysqlclient (MySQLdb on py3)

### Changed
 - tornado.web interceptor now works on all tornado versions >= 3.2

### Fixed
 - Fixed rare case of segfaults with mod_wsgi when handling raw Python frame objects
