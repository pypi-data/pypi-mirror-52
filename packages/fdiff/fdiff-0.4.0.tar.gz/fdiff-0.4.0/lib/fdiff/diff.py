import asyncio
import os
import tempfile

from fontTools.ttLib import TTFont

from fdiff.exceptions import AIOError
from fdiff.remote import (
    _get_filepath_from_url,
    create_async_get_request_session_and_run,
)
from fdiff.thirdparty.fdifflib import unified_diff
from fdiff.utils import get_file_modtime


def u_diff(
    filepath_a, filepath_b, context_lines=3, include_tables=None, exclude_tables=None
):
    """Performs a unified diff on a TTX serialized data format dump of font binary data using
    a modified version of the Python standard libary difflib module.

    filepath_a: (string) pre-file local file path or URL path
    filepath_b: (string) post-file local file path or URL path
    context_lines: (int) number of context lines to include in the diff (default=3)
    include_tables: (list of str) Python list of OpenType tables to include in the diff
    exclude_tables: (list of str) Python list of OpentType tables to exclude from the diff

    include_tables and exclude_tables are mutually exclusive arguments.  Only one should
    be defined

    :returns: Generator of ordered diff line strings that include newline line endings
    :raises: KeyError if include_tables or exclude_tables includes a mis-specified table
    that is not included in filepath_a OR filepath_b
    :raises: fdiff.exceptions.AIOError if exception raised during execution of async I/O
             GET request for URL or file write
    :raises: fdiff.exceptions.AIOError if GET request to URL returned non-200 response status code"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # define the file paths with either local file requests
        # or pulls of remote files based on the command line request
        urls = []
        if filepath_a.startswith("http"):
            urls.append(filepath_a)
            prepath = _get_filepath_from_url(filepath_a, tmpdirname)
            # keep URL as path name for remote file requests
            pre_pathname = filepath_a
        else:
            prepath = filepath_a
            pre_pathname = filepath_a

        if filepath_b.startswith("http"):
            urls.append(filepath_b)
            postpath = _get_filepath_from_url(filepath_b, tmpdirname)
            # keep URL as path name for remote file requests
            post_pathname = filepath_b
        else:
            postpath = filepath_b
            post_pathname = filepath_b

        # Async IO fetch and write of any remote file requests
        if len(urls) > 0:
            loop = asyncio.get_event_loop()
            tasks = loop.run_until_complete(
                create_async_get_request_session_and_run(urls, tmpdirname)
            )
            for task in tasks:
                if task.exception():
                    # raise exception here to notify calling code that something
                    # did not work
                    raise AIOError(f"{task.exception()}")
                elif task.result().http_status != 200:
                    # handle non-200 HTTP response status codes + file write fails
                    raise AIOError(
                        f"failed to pull '{task.result().url}' with HTTP status code {task.result().http_status}"
                    )

        # instantiate left and right fontTools.ttLib.TTFont objects
        tt_left = TTFont(prepath)
        tt_right = TTFont(postpath)

        # Validation: include_tables request should be for tables that are in one of
        # the two fonts. This otherwise silently passes with exit status code 0 which
        # could lead to the interpretation of no diff between two files when the table
        # entry is incorrectly defined or is a typo.  Let's be conservative and consider
        # this an error, force user to use explicit definitions that include tables in
        # one of the two files, and understand that the diff request was for one or more
        # tables that are not present.
        if include_tables is not None:
            for table in include_tables:
                if table not in tt_left and table not in tt_right:
                    raise KeyError(
                        f"'{table}' table was not identified for inclusion in either font"
                    )

        # Validation: exclude_tables request should be for tables that are in one of
        # the two fonts.  Mis-specified OT table definitions could otherwise result
        # in the presence of a table in the diff when the request was to exclude it.
        # For example, when an "OS/2" table request is entered as "OS2".
        if exclude_tables is not None:
            for table in exclude_tables:
                if table not in tt_left and table not in tt_right:
                    raise KeyError(
                        f"'{table}' table was not identified for exclusion in either font"
                    )

        fromdate = get_file_modtime(prepath)
        todate = get_file_modtime(postpath)

        tt_left.saveXML(
            os.path.join(tmpdirname, "left.ttx"),
            tables=include_tables,
            skipTables=exclude_tables,
        )
        tt_right.saveXML(
            os.path.join(tmpdirname, "right.ttx"),
            tables=include_tables,
            skipTables=exclude_tables,
        )

        with open(os.path.join(tmpdirname, "left.ttx")) as ff:
            fromlines = ff.readlines()
        with open(os.path.join(tmpdirname, "right.ttx")) as tf:
            tolines = tf.readlines()

        return unified_diff(
            fromlines,
            tolines,
            pre_pathname,
            post_pathname,
            fromdate,
            todate,
            n=context_lines,
        )
