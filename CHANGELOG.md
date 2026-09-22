# Changelog

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
(or tries as best as it can)

## [Unreleased]

### Fixed

  - Fixed a crash (`pandas.errors.ParserError`) parsing `.mapstat` files from newer KMA versions (>=1.6.x), which write an extra `## command` metadata line that CCMetagen's fixed `header=6` offset didn't account for. Mapstat metadata is now parsed by key name (`fParseKMA.parse_mapstat_header`) instead of assuming a fixed number of header lines, so this is robust to future KMA format changes too. Affects `-du rpm`, `-du fr`, `-ef y`, and `-k rc`/`-k rca`.
  - Fixed a crash (`TypeError: Invalid value ... for dtype 'str'`) in `populate_w_tax` under pandas >=3.0, which infers a strict string dtype for the taxa columns (`LCA_TaxId`, `Superkingdom`, ...) from their initial `""` values, then rejects the int NCBI taxids assigned into them afterward. These columns are now explicitly forced to `object` dtype.
  - Fixed a crash (`TypeError: DataFrame.groupby() got an unexpected keyword argument 'axis'`) in `CCMetagen_merge.py` under pandas >=3.0, which removed the `axis` parameter from `groupby()`. Replaced with the transpose/groupby/transpose-back pattern, pandas' own recommended migration for this exact case.

### Changed

  - Pinned `kma >=1.6.15` in `environment.yaml`, the version this fix was tested against.

## [v1.4.2](https://github.com/vrmarcelino/CCMetagen/releases/tag/v1.4.2)

- We've recently resumed CCMetagen development. `v1.4.2` is mostly a documental update,
preparing the software for updates to follow.

# Archive

## [v1.2.2](https://github.com/vrmarcelino/CCMetagen/compare/v1.1.2...v1.2.2) - 16.06.2020

### Fixed

  - broken PyPi setup and install

### Fixed

  - Importing modules

## [v1.1.2](https://github.com/vrmarcelino/CCMetagen/compare/v1.1.1...v1.1.2) - 09.07.2019

### Fixed

  - Importing modules

### Changed

  - ETE3 checks its taxonomy database after help implicitly

## [v1.1.3](https://github.com/vrmarcelino/CCMetagen/compare/v1.1.2...v1.1.3) - 10.07.2019

### Changed

  - Changed default abundance calculations back to the default kma - i.e. taking gene lengths into consideration.

## [v1.1.4](https://github.com/vrmarcelino/CCMetagen/compare/v1.1.3...v1.1.4) - 12.12.2019

### Changed

  - Added option to calculate abundance in Reads Per Million (RPM).

## [v1.1.5](https://github.com/vrmarcelino/CCMetagen/compare/v1.1.4...v1.1.5) - 20.03.2020

### Changed

 - Changed CCMetagen_merge.py code to be compatible with latest version of Pandas, it now allows merging at Closest_match without raising an ambiguity error.


## [v1.2.0](https://github.com/vrmarcelino/CCMetagen/compare/v1.1.5...v1.2.0) - 13.06.2020

### Changed

 - Added CCMetagen_extract_seqs.py and a feature to calculate the proportion of mapped reads.


