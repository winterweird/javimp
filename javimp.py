# javimp.py

# find probable java import statements for a given list of
# classes specified by root name

import sys, os, fileinput, re, time
MISSING_3RD_PARTY_MODULES = []

try:
    from lxml import html
except ImportError:
    MISSING_3RD_PARTY_MODULES.append("lxml")
try:
    import requests
except ImportError:
    MISSING_3RD_PARTY_MODULES.append("requests")
try:
    import pyperclip
except ImportError:
    MISSING_3RD_PARTY_MODULES.append("pyperclip")

HELP_MESSAGE_STRING = """
DESCRIPTION:
This python script iterates over any arguments you give it, searches a database
of class names for a class that matches the argument, and prints out the full
import statement including the package. Any already complete import statements
or import statements with packages that cannot be found are left alone. If you
run it without any arguments, it uses web scraping to update its database of
Java classes.

USAGE: python %s [option] [args]

OPTIONS:
    -h: Displays this help message
    -a: Show all mode; use in combination with any other option to add any
        additional matches of a class to the next line, commented out. Must
        be the first option.
        Example: "-a -i MyJavaFile.java" is allowed; "-i -a MyJavaFile.java"
        is likely to create problems.
    -i: Insert mode; insert the complete import statements directly in one or
        more .java source file(s)
        Example: Given a source file containing these lines:
            import Activity;
            import Bundle;
        The script would correctly replace this with:
            import android.app.Activity;
            import android.os.Bundle;
    -c: Clipboard mode; copies the correct import statements to your clipboard
    -o: File output; Creates a file in your current working directory which
        contains the correct import statements

NOTE: The included java_classes.list file should contain all of the standard
library classes and the classes for Android app development as of 2016/06/20.
It may be incomplete, contain erroneous information, or be otherwise unsuitable
for your purposes. This software comes with no warranty or guarantee. Use at
own risk.

Sincerely, Butterbeard Studios.
""" %sys.argv[0]

FILELOCATION = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    if "-h" in sys.argv:
        print(HELP_MESSAGE_STRING)
        sys.exit()
    if (MISSING_3RD_PARTY_MODULES):
        sys.stderr.write("Warning - 3rd party modules missing: " + ", ".join(MISSING_3RD_PARTY_MODULES) + "\n")
        sys.stderr.write("Some of this program's functionality will not be available.\n\n")
    
    includeAllMatches = "-a" in sys.argv
    mode = "i" if "-i" in sys.argv else "o" if "-o" in sys.argv else "c" if "-c" in sys.argv else None
    
    if mode == "c":
        if "pyperclip" in MISSING_3RD_PARTY_MODULES:
            print("Error - missing modules: pyperclip")
            sys.exit()
    
    pyperclip_str = "" # needed to accumulate string to paste to clipboard
    
    if len(sys.argv) == 1:
        # only python script supplied
        # update source list
        if not ("lxml" in MISSING_3RD_PARTY_MODULES or "requests" in MISSING_3RD_PARTY_MODULES):
            print("Updating list of classes. This may take a little while...")
            
            # backwards compatible way of not printing a newline at the end
            sys.stdout.write("Fetching Java standard library classes...")
            sys.stdout.flush()
            
            page = requests.get("http://docs.oracle.com/javase/7/docs/api/allclasses-frame.html")
            tree = html.fromstring(page.content)
            
            allStdlibClasses = [a.replace(".html", "").replace("/", ".") for a in tree.xpath('//a[@target="classFrame"]/@href')]
            
            sys.stdout.write("\nFetching Android API classes...")
            sys.stdout.flush()
            
            page = requests.get("https://developer.android.com/reference/classes.html")
            tree = html.fromstring(page.content)
            
            allAndroidClasses = [a.replace("https://developer.android.com/reference/", "").replace(".html", "").replace("/", ".") for a in tree.xpath('//td[@class="jd-linkcol"]/a/@href')]
            allClasses = set(allStdlibClasses+allAndroidClasses)
            
            with open(os.path.join(FILELOCATION, "java_classes.list"), "w") as classlist:
                for a in allClasses:
                    classlist.write(a + "\n")
            
            print("\nList of classes to search for updated.")
        else:
            print("Error - missing modules: " + ("lxml and requests" if "requests" in MISSING_3RD_PARTY_MODULES else "lxml") if "lxml" in MISSING_3RD_PARTY_MODULES else "requests")
    else:
        for i in range(1, len(sys.argv)):
            if sys.argv[i].startswith("-"):
                # option, we don't wanna deal with this
                continue
            found = False # used if includeAllMatches
            if mode == "i":
                # insert mode is special, so we handle it separately
                for line in fileinput.input(sys.argv[i], inplace=True):
                    # A NOTE ON FILEINPUT:
                    #
                    # With the inplace option set to True, fileinput backs up
                    # the file, and sets sys.stdout to the original file for the
                    # duration of the loop. Any calls to sys.stdout.write or
                    # print will therefore be written on top of the original
                    # file.
                    
                    found = False
                    if line.startswith("import"):
                        with open(os.path.join(FILELOCATION, "java_classes.list"), "r") as classlist:
                            for c in classlist:
                                if c.rstrip().endswith(".%s" %re.sub("import |;", "", line.rstrip())):
                                    if found:
                                        # multiple matches; add new matches as comments just in case
                                        # note how found is set to True AFTER this, so if this is the
                                        # first class found, it will still be False from earlier
                                        sys.stdout.write("//")
                                    
                                    sys.stdout.write("import %s;\n" %c.rstrip())
                                    found = True
                                    if not includeAllMatches:
                                        break # fuck it, let's just hope it's the right one
                    if not found:
                        # 1) There was no match for the attempted import
                        # 2) The line didn't start with import, so we jumped straight here
                        # In either case, insert the line as it was
                        sys.stdout.write(line)
            else:
                # the class we're trying to find is passed directly as sys.argv[i]
                import_str = ""
                with open(os.path.join(FILELOCATION, "java_classes.list"), "r") as classlist:
                    for c in classlist:
                        if c.rstrip().endswith(".%s" %sys.argv[i]):
                            if found:
                                # already found, comment out subsequent matches
                                import_str += "//"
                            # we need to use os.linesep here instead of \n because of
                            # clipboard support
                            import_str += "import %s;%s" %(c.rstrip(), os.linesep)
                            found = True
                            if not includeAllMatches:
                                break
                
                # So import_str now holds a single complete import statement[1]
                # corresponding to the class specified in sys.argv[i], or is
                # empty if no match was found[2]. All we need to figure out is
                # how to output it.
                #
                # 1: ... plus an unknown number of subsequent import statements
                #    that are commented out.
                # 2: Or if the specified class to import already had the full
                #    package specified.
                
                if mode == "o":
                    # output to file
                    with open("import_statements.txt", "a") as o:
                        o.write(import_str)
                elif mode == "c":
                    # we still need to iterate over all the other classes so we can
                    # copy it all to the clipboard in one go
                    pyperclip_str += import_str
                else:
                    # write to stdout
                    sys.stdout.write(import_str)
        
        if pyperclip_str:
            # if not -c mode, this was never written to, so it's False
            # if else, it's either empty because there were no matches,
            # or it contains all the imports, and we can copy them to
            # the clipboard
            pyperclip.copy(pyperclip_str)
