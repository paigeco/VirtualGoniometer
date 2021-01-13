"""[ ensure that the necessary packages are installed ]"""

# QUESTIONABLE PACKAGES
try:
    # Attempt an import
    import scipy # pylint: disable=unused-import
    import sklearn # pylint: disable=unused-import
    
except ImportError:
    pass
