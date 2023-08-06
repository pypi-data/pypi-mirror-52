class MobikitUtilsError(Exception):
    """Generic mobikit utils error; can be used as a catch-all for calls to mobikit-utils methods."""

    pass


class MetadataError(MobikitUtilsError):
    """A generic error within the metadata service."""

    pass
