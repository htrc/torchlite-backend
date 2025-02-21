# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- All logging to use logger instead of print statements
- How the word cloud widget tabulates word counts, significantly reducing processing time once the EF API has responded.

### Added
- Comparison between frontend featured workset list and backend to keep backend representation up-to-date to allow featured worksets to be swapped out by the AG user, and those changes will seemlessly propogate to TORCHLITE [#148](https://github.com/htrc/torchlite-backend/issues/148)

### Fixed
- Handling of unauthorized and invalid worksets [#146](https://github.com/htrc/torchlite-backend/issues/146)
- Handling of volumes without text in text-based widgets [#146](https://github.com/htrc/torchlite-backend/issues/146)
- Handling of widgets when trying to load worksets that have not yet been built in the database [#146](https://github.com/htrc/torchlite-backend/issues/146)
- Handling of building redis connection at startup [#150](https://github.com/htrc/torchlite-backend/issues/150)

## [0.2.0] – 2025-01-06

### Added
- Endpoint for downloading workset data and metadata, optionally with filters applied. [#120](https://github.com/htrc/torchlite-backend/issues/120)

### Changed
- Brought changes from stage to main branch, and from main to dev. [#135](https://github.com/htrc/torchlite-backend/issues/135)
- Full and Filtered to pull from aggregate data as a stopgap while full data is not loaded

### Fixed
- Redis close error on shutdown

## [0.1.0] – 2024-12-06

### Added
- This CHANGELOG file.
- HTTPX client for mTLS connections to the registry to retrieve worksets. [#125](https://github.com/htrc/torchlite-backend/issues/125)

[unreleased]: https://github.com/htrc/torchlite-backend/compare/0.2.0...HEAD
[0.2.0]: https://github.com/htrc/torchlite-backend/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/htrc/torchlite-backend/releases/tag/0.1.0