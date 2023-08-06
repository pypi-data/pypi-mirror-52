import json
import os.path
import re
import sys

class KeywordExpander:
    """
    Parse input file or stream line by line, performing keyword expansion from saved json state.

    ...

    Methods
    -------
    expand_from_json(data, output_directory):
        Given current json, read code_src and write code_snap
    expand_from_json_file(infile, output_directory):
        Given json input file, read code_src and write code_snap
    """

    _var_expand_str = r'(?P<pre>.*[$])(?P<var>[a-zA-Z_][a-zA-Z_0-9.]*)(?P<col>:?:?)(?P<curval>.*)(?P<post>[$].*)'

    _var_expand_re = re.compile(_var_expand_str, re.S)

    @staticmethod
    def _lookup_var(str, data):
        from psnap import state_tracker
        meta_key = state_tracker.StateTracker._meta_key

        data_key = data[meta_key]["data_key"]

        # Or, see dotty dict
        pieces = str.split(".", 2)

        if len(pieces) >= 1 and len(pieces) <= 2:
            if pieces[0] in data[data_key]:
                if len(pieces) == 1:
                    return data[data_key][pieces[0]]
                elif len(pieces) == 2:
                    return data[data_key][pieces[0]][pieces[1]]

        return None

    @staticmethod
    def _expand_vars(line, data):
        # Try to return quickly if see nothing to expand
        if not "$" in line:
            return line

        # Search is for match anywhere on line
        # but we are matching to full line.
        #match = KeywordExpander._var_expand_re.search(line)
        match = KeywordExpander._var_expand_re.match(line)

        if match is not None:
            d = match.groupdict()
            val = KeywordExpander._lookup_var(d['var'], data)
            if val is not None:
                coltype = d['col']
                if len(coltype) == 0:
                    coltype = ":"
                line = f"{d['pre']}{d['var']}{coltype} {val} {d['post']}"

        return line

    @staticmethod
    def expand_from_json(data, output_directory=None):
        """
        Given current json, read code_src and write code_snap.

        Parameters
        ----------
        data : dict
            json dictionary include psnap metadata and state data.
        output_directory : str, optional
            Output directory for code_snap else default is to use same directory as code_src.

        Raises
        ------
        RuntimeError
            Issues RuntimeError if output of code_snap matches input code_src.

        Returns
        -------
        dict
            Dictionary containing "code_src" and "code_snap".
        """
        from psnap import state_tracker
        meta_key = state_tracker.StateTracker._meta_key

        infile = data[meta_key]['code_src']
        outfile = data[meta_key]['code_snap']

        if output_directory is not None:
            # Update path in outfile to use output_directory
            output_basename = os.path.basename(outfile)
            outfile = os.path.join(output_directory, output_basename)

        infile_norm = os.path.normpath(infile)
        outfile_norm = os.path.normpath(outfile)
        if infile_norm == outfile_norm:
            raise RuntimeError(f"Output file must not match input code_src: {infile}")

        with open(outfile, "w", encoding="utf-8") as fout:
            with open(infile, encoding="utf-8") as fin:
                for line in fin:
                    line = KeywordExpander._expand_vars(line, data)
                    fout.write(line)

        result = {
            "code_src": infile,
            "code_snap": outfile
        }

        return result

    @staticmethod
    def expand_from_json_file(infile, output_directory=None):
        """
        Given json input file, read code_src and write code_snap.

        Parameters
        ----------
        infile : str
            filename of json dictionary include psnap metadata and state data.
        output_directory : str, optional
            Output directory for code_snap else default is to use same directory as code_src.

        Returns
        -------
        dict
            Dictionary containing "code_src" and "code_snap".
        """
        with open(sys.argv[1], encoding="utf-8") as f:
            data = json.load(f)

        return KeywordExpander.expand_from_json(data, output_directory=output_directory)
