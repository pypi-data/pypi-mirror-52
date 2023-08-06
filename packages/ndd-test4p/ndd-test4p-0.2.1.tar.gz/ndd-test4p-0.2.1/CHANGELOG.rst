#########
Changelog
#########


Version 0.2.0
=============

**Breaking changes:** None

**Features:**

- Add `ndd_test4p.differences_viewvers.YamlDifferencesViewer`
- Add `ndd_test4p.expects.content_matchers.have_same_content_recursively_as`
- Add `ndd_test4p.comparators.DirectoryContentComparator`
- Add `ndd_test4p.comparators.TextFileContentComparator#unified_diff`
- Add diff output in `ndd_test4p.expects.content_matchers.have_same_content_as`

**Improvements:**

- Change implementation of `ndd_test4p.differences_viewvers.DiffViewerDelegate` to difflib
- Rename GitLab CI stages

**Issues:** None

**Quality:**

- Improve code quality using pylint and flake8
- Fix distribution documentation

Version 0.1.1
=============

- Add 'deploy to PyPI' stage to GitLab CI
- Fix project URLs in ``setup.cfg``
- Fix regular expression in ``.gitlab-ci``


Version 0.1.0
=============

- Add ``ndd_test4p.AbstractTest``
- Add Flake8 linter
- Add Pylint linter
- Add Sphinx documentation
- Add Tox testing
- Add ``doctest`` tests
- Add ``ndd_test4p.expects.numeric_matchers.approximate``
- Add ``ndd_test4p.expects.content_matchers.have_same_content_as``
- Add ``ndd_test4p.comparators.TextFileContentComparator``
- Add ``ndd_test4p.differences_viewers``
- Add ``ndd_test.differences_viewers.TextFileDifferencesViewer``
- Add testing and code coverage to GitLab CI

