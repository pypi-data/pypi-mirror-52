import os
end = os.path.realpath(__file__).rfind(os.sep)
path_to_templates = os.path.realpath(__file__)[:end]

__all__ = ['path_to_templates']
