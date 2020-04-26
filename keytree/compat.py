import warnings
import sys

if sys.version_info < (3, 6):
    warnings.warn(
        "Keytree will soon be Python 3 only. "
        "See this issue to know more: "
        "https://github.com/Toblerity/keytree/issues/7.",
        UserWarning,
    )
