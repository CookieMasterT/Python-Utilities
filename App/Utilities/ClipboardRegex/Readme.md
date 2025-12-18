# Clipboard Regular expressions
Invoked with Ctrl + Alt + [Number 1-9]

Will use a regular expression on the text inside the clipboard and insert the output back to it

Intended to be used with any copy + paste to speed up specific workflows

Use https://regex101.com/ to create the regular expression.

If the regular expression does not have any groups defined, the script does nothing,
otherwise the clipboard is set to the first group found