**DEPENDENCY NOTE:** This Python script depends on the 3rd party modules `lxml`, `requests` and `pyperclip` for some of its functionality. If you do not have these modules installed with your Python installation, you may still use the program; however, updating the Java class database (`lxml`/`requests`) and utilizing the `-c`option (`pyperclip`) is disabled.

This script has been tested and is known to work with Python versions 2.6, 3.3 and 3.4, and it should theoretically work with any Python 2.x/3.x installation with all the required modules installed.

# javimp.py: Java Importer

A Python script which turns incomplete Java `import` statements (e.g. `import ArrayList;`) into complete ones.

> B-but why?

I'm sick and tired of manually finding where all the things I'm using are located. At the same time, I don't want to use an IDE to get their autocomplete features, because of my less-than-ideal experiences with IDEs and the resulting irrational dislike for them. So I made this, so I can continue to write my code in an editor while not having to struggle too hard to import stuff. It's probably not as good as an IDE, but it's the next best thing.

### DESCRIPTION:

This Python script iterates over any arguments you give it, searches a database of class names for a class that matches the argument, and prints out the full `import` statement including the package. Any already complete `import` statements or `import` statements with packages that cannot be found are left alone. If you run it without any arguments, it uses web scraping to update its database of Java classes.

### USAGE:

`python javimp.py [option] [args]`

### OPTIONS:

```
-h: Displays the help message
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
