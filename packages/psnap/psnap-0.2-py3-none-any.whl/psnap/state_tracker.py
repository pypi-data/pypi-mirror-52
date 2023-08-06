import datetime
import json
import os.path
import sys
import time

class StateTracker:
    """
    Intended to capture outputs and metadata for single Python script.

    ...

    Attributes
    ----------
    meta : dict
        dictionary containing metadata
    data : dict
        dictionary containing values that have been set
    code_snap : str
        output name of Python script with keyword substitution

    Methods
    -------
    set(key, value)
        Stores data[key] = value
    save(filename=None)
        Save json output and metadata, defaulting to constructor filename
    """

    # Top-level output dictionary contains ["data"] and ["psnap_meta"].
    _data_key = "data"
    _meta_key = "psnap_meta"

    def __init__(self, filename, dateformat=None, code_src=None, code_snap=None):
        """
        Parameters
        ----------
        filename : str
            default name of output json file, %D will be expanded using dateformat
        dateformat : str, optional
            datetime date format intended for use in output filenames;
            defaults to "%Y%m%d_%H%M%S"
        code_src : str, optional
            defaults to sys.argv[0] but may be overridden if running in
            Jupyter notebook, etc.
        code_snap : str, optional
            can specify output name of code snapshot for psnap keyword
            substitution; defaults to use code_src with "_dateformat"
            inserted before the file extension
        """

        self._hist = {}
        if dateformat is None:
            dateformat = "%Y%m%d_%H%M%S"
        self._dateformat = dateformat

        self._hist[StateTracker._data_key] = {}
        now = time.time()
        time_ts = datetime.datetime.fromtimestamp(now)
        ts_iso = time_ts.isoformat()
        self.ts_str = time_ts.strftime(dateformat)
        filename = self._expand_filename(filename)

        if code_src is None:
            # Note: Should pass value as arg for notebook, etc.
            code_src = sys.argv[0]
        if code_snap is None:
            code_snap = os.path.splitext(code_src)[0] + f"_{self.ts_str}" + os.path.splitext(code_src)[1]
        self._hist[StateTracker._meta_key] = {
            "code_src": code_src,
            "code_snap": code_snap,
            "filename": filename,
            "date": ts_iso,
            "date_string": self.ts_str,
            "data_key": StateTracker._data_key
        }

    def _expand_filename(self, filename):
        """
        Expands any formatting strings present in filename.

        Parameters
        ----------
        filename : str
            Name of file to expand.

        Returns
        -------
        str
            Expanded filename.
        """
        # Only formatting currently allowed is %D for self.dateformat formatting
        if "%D" in filename:
            filename = filename.replace("%D", self.ts_str)
        return filename

    def set(self, key, value):
        """
        Stores data[key] = value.

        Parameters
        ----------
        key : str
            Key.
        value : object
            Json-serializable object.
        """
        self._hist[StateTracker._data_key][key] = value

    @property
    def meta(self):
        """Dictionary containing metadata."""
        return self._hist[StateTracker._meta_key]

    @property
    def data(self):
        """Dictionary containing values that have been set."""
        return self._hist[self._hist[StateTracker._meta_key]["data_key"]]

    @property
    def code_snap(self):
        """Output name of Python script with keyword substitution."""
        return self._hist[StateTracker._meta_key]["code_snap"]

    def save(self, filename=None):
        """
        Save json output and metadata, defaulting to constructor filename.
        A different filename could be specified, such as for intermediate
        snapshots.

        Parameters
        ----------
        filename : str, optional
            Output filename which may contain formatting strings.

        Returns
        -------
        str
            Name of saved file.
        """
        if filename is None:
            filename = self._hist[StateTracker._meta_key]["filename"]
        else:
            # Allow expansion of any special vars
            filename = StateTracker._expand_filename(filename)
        with open(f"{filename}", "w", encoding="utf-8") as f:
            json.dump(self._hist, f)
        return filename
