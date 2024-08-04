from json import JSONEncoder
import numpy as np

class NumpyArrayEncoder(JSONEncoder):
    """
    A custom JSONEncoder subclass to convert numpy arrays to lists for JSON serialization.

    Methods
    -------
    default(self, obj)
        Overrides the default method to handle numpy arrays by converting them to lists.
    """
    def default(self, obj):
        """
        Override the default method to convert numpy arrays to lists.

        Parameters
        ----------
        obj : any
            The object to be encoded. If it's a numpy array, it will be converted to a list.

        Returns
        -------
        list or any
            The list representation of the numpy array, or the default encoding for other objects.
        """
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)