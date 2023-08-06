Changelog
=========

1.1.0rc3 (2019-09-13)
---------------------
- | Requirements upgrade:
  | PySide2 to at least 5.13.1
- Adding of (for now fake/empty) test case.

1.1.0rc2 (2019-08-02)
---------------------
- StreamEmitter class added.

1.1.0rc1 (2019-07-23)
---------------------
- | Requirements upgrade:
  | QtPy    to at least 1.9.0
  | PySide2 to at least 5.13.0
  | PyQt5   to at least 5.13.0
  | This allows to have applications that import PySide2 and PyQt5 at the same time
  | (which is possible if both bindings are compiled for the same Qt version).

1.0.0b5 (2019-06-10)
--------------------
- Adding setup extras PySide and PyQt for installing PySide2 or PyQt5 backends.

1.0.0b4 (2019-06-06)
--------------------
- Fix a bug for PySide2 as backend.

1.0.0b3 (2019-06-04)
--------------------
- Adding a monkey-patch for vtk.qt (vtk==8.1.x).

1.0.0b2 (2019-05-22)
--------------------
- Fixes and cleanup of setup.

1.0.0b1 (2019-05-22)
--------------------
- First public release.

0.0.1a1 (2012-03-9)
-------------------
- Initial version.
