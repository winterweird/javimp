**DEPENDENCY NOTE:** This Python script depends on the 3rd party modules `lxml`, `requests` and `pyperclip` for some of its functionality. If you do not have these modules installed with your Python installation, you may still use the program; however, updating the Java class database (`lxml`/`requests`) and utilizing the `-c`option (`pyperclip`) is disabled.

This script has been tested and is known to work with Python versions 2.6, 3.3 and 3.4, and it should theoretically work with any Python 2.x/3.x installation with all the required modules installed.

# javimp.py: Java Importer

A Python script which turns incomplete Java `import` statements (e.g. `import ArrayList;`) into complete ones.

> B-but why?

I'm sick and tired of manually finding where all the things I'm using are located. At the same time, I don't want to use an IDE to get their autocomplete features, because of my less-than-ideal experiences with IDEs and the resulting irrational dislike for them. So I made this, so I can continue to write my code in an editor while not having to struggle too hard to import stuff. It's probably not as good as an IDE, but it's the next best thing.

### DESCRIPTION:

This python script tries to match the arguments you give it to classes in a database, and prints out the results it finds. You can update the list of classes through web scraping by running the program with no arguments.

### USAGE:

`python javimp.py [options] [args]`
or
`python javimp.py [args] [options]`
or
`python javimp.py [args] [options] [more args]`
or whatever.

Please take note that aside from -a mode, only one mode can be in effect at the time. Precedence is -i > -o > -c > None

### OPTIONS:

```
-h: Displays the help message
-a: Show all mode; use in combination with any other option to add any additional matches of a class as a commented import
-i: Insert mode; insert the complete import statements directly in one or more .java source file(s)
    Example: Given a source file containing these lines:
        import Activity;
        import Bundle;
    The script would correctly replace this with:
        import android.app.Activity;
        import android.os.Bundle;
-c: Clipboard mode; copies the correct import statements to your clipboard (requires pyperclip module)
-o: File output; Creates a file in your current working directory which contains the correct import statements
```

### NOTE:

The included `java_classes.list` file should contain all of the standard library classes and the classes for Android app development as of 2016/06/20. It may be incomplete, contain erroneous information, or be otherwise unsuitable for your purposes. This software comes with no warranty or guarantee. Use at own risk.

Sincerely, Butterbeard Studios.
