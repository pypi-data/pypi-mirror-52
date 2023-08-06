# -*- coding: utf-8 -*-
import sys


PY3 = sys.version_info > (3, )

unicode = str if PY3 else unicode  # noqa: F821
