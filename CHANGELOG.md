# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Endpoint for downloading workset data and metadata, optionally with filters applied. [#120](https://github.com/htrc/torchlite-backend/issues/120)

### Changed
- Brought changes from stage to main branch, and from main to dev. [#135](https://github.com/htrc/torchlite-backend/issues/135)

### Fixed
- Redis close error on shutdown

## [0.1.0] – 2024-12-06

### Added
- This CHANGELOG file.
- HTTPX client for mTLS connections to the registry to retrieve worksets. [#125](https://github.com/htrc/torchlite-backend/issues/125)

[unreleased]: https://github.com/htrc/torchlite-backend/compare/0.1.0...HEAD
[0.1.0]: https://github.com/htrc/torchlite-backend/releases/tag/0.1.0