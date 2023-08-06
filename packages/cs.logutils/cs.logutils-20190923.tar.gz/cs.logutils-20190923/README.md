Logging convenience routines.


*Latest release 20190923*:
New `TRACK` constant equal to `logging.INFO+5` to provide a level higher than `INFO`
(which seems unreasonably noisy) and lower than `WARNING`
warning for tracking salient events.
New `track()` function to match.

Logging convenience routines.

The logging package is very useful, but a little painful to use.
This package provides low impact logging setup and some extremely
useful if unconventional context hooks for logging.

The default logging verbosity output format has different defaults
based on whether an output log file is a tty
and whether the environment variable $DEBUG is set, and to what.

On terminals warnings and errors get ANSI colouring.

A mode is available that uses cs.upd.

Some examples:
--------------

Program initialisation::

    from cs.logutils import setup_logging

    def main(argv):
      cmd = os.path.basename(argv.pop(0))
      setup_logging(cmd)

Basic logging from anywhere::

    from cs.logutils import info, warning, error
    [...]
    def some_function(...):
        [...]
        error("nastiness found! bad value=%r", bad_value)

## Function `add_logfile(filename, logger=None, mode='a', encoding=None, delay=False, format=None, no_prefix=False)`

Add a FileHandler logging to the specified `filename`;
return the chosen logger and the new handler.

Parameters:
* `logger`: if supplied and not None, add the FileHandler to that
  Logger, otherwise to the root Logger. If `logger` is a string, call
  `logging.getLogger(logger)` to obtain the logger.
* `mode`, `encoding` and `delay`: passed to the logging.FileHandler
  initialiser.
* `format`: used to override the handler's default format.
* `no_prefix`: if true, do not put the Pfx context onto the front of the message.

## Function `critical(msg, *args, **kwargs)`

Emit a log at `logging.CRITICAL` `level` with the current Pfx prefix.

## Function `D(msg, *args)`

Print formatted debug string straight to sys.stderr if D_mode is true,
bypassing the logging modules entirely.
A quick'n'dirty debug tool.

## Function `debug(msg, *args, **kwargs)`

Emit a log at `logging.DEBUG` `level` with the current Pfx prefix.

## Function `error(msg, *args, **kwargs)`

Emit a log at `logging.ERROR` `level` with the current Pfx prefix.

## Function `exception(msg, *args)`

Emit an exception log with the current Pfx prefix.

## Function `ftrace(func)`

Decorator to trace a function if __module__.DEBUG is true.

## Function `ifdebug()`

Test the `logging_level` against `logging.DEBUG`.

## Function `infer_logging_level(env_debug=None, environ=None, verbose=None)`

Infer a logging level from the `env_debug`, which by default
comes from the environment variable `$DEBUG`.

Usually default to logging.WARNING, but if sys.stderr is a terminal,
default to logging.INFO.

Parse the environment variable $DEBUG as a comma separated
list of flags.

Examine the in sequence flags to affect the logging level:
* `numeric < 1`: `logging.WARNING`
* `numeric >= 1 and < 2`: `logging.INFO`
* `numeric >= 2`: `logging.DEBUG`
* `"DEBUG"`: `logging.DEBUG`
* `"INFO"`: ` logging.INFO`
* `"WARNING"`: `logging.WARNING`
* `"ERROR"`: `logging.ERROR`

Return an object with the following attributes:
* `.level`: A logging level.
* `.flags`: All the words from $DEBUG as separated by commas and uppercased.
* `.module_names`: Module names to be debugged.
* `.function_names`: Functions to be traced in the for "module_name.func_name()".

## Function `info(msg, *args, **kwargs)`

Emit a log at `logging.INFO` `level` with the current Pfx prefix.

## Function `log(level, msg, *args, **kwargs)`

Emit a log at the specified `level` with the current Pfx prefix.

## Function `logException(exc_type, exc_value, exc_tb)`

Replacement for sys.excepthook that reports via the cs.logutils
logging wrappers.

## Class `LogTime`

LogTime is a content manager that logs the elapsed time of the enclosed
code. After the run, the field .elapsed contains the elapsed time in
seconds.

### Method `LogTime.__init__(self, tag, *args, **kwargs)`

Set up a LogTime.

Parameters:
* `tag`: label included at the start of the log entry
* `args`: optional array; if not empty `args` is applied to
  `tag` with `%`
* `level`: keyword argument specifying a log level for a
  default log entry, default `logging.INFO`
* `threshold`: keyword argument specifying minimum time to
  cause a log, default None (no minimum)
* `warning_level`: keyword argument specifying the log level
  for a warning log entry, default `logging.WARNING`
* `warning_threshold`: keyword argument specifying a time
  which raises the log level to `warning_level`

## Function `logTo(filename, logger=None, mode='a', encoding=None, delay=False, format=None, no_prefix=False)`

Add a FileHandler logging to the specified `filename`;
return the chosen logger and the new handler.

Parameters:
* `logger`: if supplied and not None, add the FileHandler to that
  Logger, otherwise to the root Logger. If `logger` is a string, call
  `logging.getLogger(logger)` to obtain the logger.
* `mode`, `encoding` and `delay`: passed to the logging.FileHandler
  initialiser.
* `format`: used to override the handler's default format.
* `no_prefix`: if true, do not put the Pfx context onto the front of the message.

## Class `NullHandler`

MRO: `logging.Handler`, `logging.Filterer`  
A Handler which discards its requests.

## Function `OBSOLETE(func)`

Decorator for obsolete functions.

Use:

    @OBSOLETE
    def f(...):

This emits a warning log message before calling the decorated function.

## Class `PfxFormatter`

MRO: `logging.Formatter`  
A Formatter subclass that has access to the program's cmd and Pfx state.

### Method `PfxFormatter.__init__(self, fmt=None, datefmt=None, cmd=None)`

Initialise the PfxFormatter.

`fmt` and `datefmt` are passed to Formatter.
If `fmt` is None, DEFAULT_PFX_FORMAT is used.
If `cmd` is not None, the message is prefixed with the string `cmd`.

## Function `setup_logging(cmd_name=None, main_log=None, format=None, level=None, flags=None, upd_mode=None, ansi_mode=None, trace_mode=None, module_names=None, function_names=None, verbose=None)`

Arrange basic logging setup for conventional UNIX command
line error messaging; return an object with informative attributes.

Parameters:
* `cmd_name`: program name, default from `basename(sys.argv[0])`.
  Side-effect: sets `cs.pfx.cmd` to this value.
* `main_log`: default logging system.
  If None, the main log will go to sys.stderr;
  if `main_log` is a string, is it used as a filename to
  open in append mode;
  otherwise main_log should be a stream suitable
  for use with `logging.StreamHandler()`.
  The resulting log handler is added to the `logging` root logger.
* `format`: the message format for `main_log`.
  If `None`, use `DEFAULT_PFX_FORMAT_TTY`
  when `main_log` is a tty or FIFO,
  otherwise `DEFAULT_PFX_FORMAT`.
* `level`: `main_log` logging level.
  If None, infer a level from the environment
  using `infer_logging_level()`.
* `flags`: a string containing debugging flags separated by commas.
  If `None`, infer the flags from the environment using
  `infer_logging_level()`.
  The following flags have meaning:
  `D`: set cs.logutils.D_mode to True;
  `TDUMP`: attach a signal handler to SIGHUP to do a thread stack dump;
  `TRACE`: enable various noisy tracing facilities;
  `UPD`, `NOUPD`: set the default for `upd_mode` to True or False respectively.
* `upd_mode`: a Boolean to activate cs.upd as the `main_log` method;
  if `None`, set it to `True` if `flags` contains 'UPD',
  otherwise to `False` if `flags` contains 'NOUPD',
  otherwise set it to `False` (was from main_log.isatty()).
  A true value causes the root logger to use `cs.upd` for logging.
* `ansi_mode`: if `None`, set it from `main_log.isatty()`.
  A true value causes the root logger to colour certain logging levels
  using ANSI terminal sequences (currently only if `cs.upd` is used).
* `trace_mode`: if `None`, set it according to the presence of
  'TRACE' in flags. Otherwise if `trace_mode` is true, set the
  global `trace_level` to `logging_level`; otherwise it defaults
  to `logging.DEBUG`.
* `verbose`: if `None`, then if stderr is a tty then the log
  level is `INFO` otherwise `WARNING`. Otherwise, if `verbose` is
  true then the log level is `INFO` otherwise `WARNING`.

## Function `status(msg, *args, **kwargs)`

Write a message to the terminal's status line.

Parameters:
* `msg`: message string
* `args`: if not empty, the message is %-formatted with `args`
* `file`: optional keyword argument specifying the output file.
  Default: `sys.stderr`.

Hack: if there is no status line use the xterm title bar sequence :-(

## Function `trace(msg, *args, **kwargs)`

Emit a log message at `trace_level` with the current Pfx prefix.

## Function `track(msg, *args, **kwargs)`

Emit a log at `TRACK` `level` with the current Pfx prefix.

## Function `upd(msg, *args)`

If we're using an UpdHandler,
update the status line otherwise write an info message.

## Class `UpdHandler`

MRO: `logging.StreamHandler`, `logging.Handler`, `logging.Filterer`  
A `StreamHandler` subclass whose `.emit` method
uses a `cs.upd.Upd` for transcription.

### Method `UpdHandler.__init__(self, strm=None, nl_level=None, ansi_mode=None)`

Initialise the UpdHandler.

Parameters:
* `strm`: the output stream, default `sys.stderr`.
* `nl_level`: the logging level at which conventional line-of-text
  output is written; log messages of a lower level go via the
  update-the-current-line method.
  Default: `logging.WARNING`.
* `ansi_mode`: if `None`, set from `strm.isatty()`.
  A true value causes the handler to colour certain logging levels
  using ANSI terminal sequences.

## Function `warning(msg, *args, **kwargs)`

Emit a log at `logging.WARNING` `level` with the current Pfx prefix.

## Function `with_log(filename, **kw)`

Context manager to add a Logger to the output logs temporarily.



# Release Log

*Release 20190923*:
New `TRACK` constant equal to `logging.INFO+5` to provide a level higher than `INFO`
(which seems unreasonably noisy) and lower than `WARNING`
warning for tracking salient events.
New `track()` function to match.

*Release 20190220*:
Improvements to upd_mode.

*Release 20190103*:
Documentation updates.

*Release 20190101*:
Bugfix for @contextmanager usage.

*Release 20171030*:
Assorted fixes from recent module reshuffle. Other small features and cleanups. Drop a couple of unused functions.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
Pfx: import __exit__ handler
Preliminary per-module and per-function syntax accepted in $DEBUG envvar.
Improvements to X(), add DP() and XP() prefixed flavours.
status() function to update terminal status line.
New X_via_tty global flag: directs X() to tty instead of sys.stderr.
Assorted other minor improvements.

*Release 20150118*:
metadata updates

*Release 20150110*:
Initial PyPI release.
