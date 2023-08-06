## 2.0.0 (2019-09-19)

### Features
- Support for uploading to OneDrive.
- Efficient drive item enumeration.
- Rudimentary, mostly unuseful support for incremental operations.
- Rudimentary, mostly untested support for groups/shared drives.
- Reduced memory footprint.

### Incompatible changes
- Some CLI changes to avoid ambiguous names and use more consistent nomenclature.
- Restructured metadata files.

### Bugfixes
- Compatible with newer versions of requests_oauthlib
- Improved retry logic.
- gdm's lookup of folders inside the root will no longer return matches nested
  in subfolders.


## 1.0.0 (2018-08-15)

- Initial stable release.
