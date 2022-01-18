# OneAgent File Change Extension

OneAgent extension for monitoring file change and file count by specifying wildcard patterns.

Extension monitors independently:
- file modification time for patterns
- number of filter for patterns

# Configuration

### File change check parameters
- **File patterns for change check** - List of wildcard patterns for files to be verified for modification time, separated by semicolon."},
- **Pattern change event severity** - Event severity when file modification is not detected.
- **Pattern change modification minutes** - Modification threshold in minutes. Event is created if the file is not modified.
- **Pattern change event text** - Event title, available placeholders [fileName, fileLastModifiedEpoch, dirModificationMinutes, dirPattern]
- **Pattern change event description** - Event description, available placeholders [fileName, fileLastModifiedEpoch, dirModificationMinutes, dirPattern]      

### File count check parameters
- **File patterns for count check** - List of wildcard patterns for files to be counted, separated by semicolon
- **Count check limit** - Maximum allowed number of files for a pattern.
- **Pattern count event severity** - Event severity when file count is over limit.
- **Pattern count event text** - Event title, available placeholders [dirPattern, filePatternSize, filePatternSizeLimit]"
- **Pattern count event description** - Event description, available placeholders [dirPattern, filePatternSize, filePatternSizeLimit]"


# ChangeLog

- 0.01 - initial version