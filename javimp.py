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
    -i: Insert mode; insert the complete import statements directly in one or
        more .java source file(s)
        Example: Given a source file containing these lines:
            import Activity;
            import Bundle;
        The script would correctly replace this with:
            import android.app.Activity;
            import android.os.Bundle;
    -c: Clipboard mode; copies the correct import statements to your clipboard
        (not yet implemented)
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
        print("Warning - 3rd party modules missing: " + ", ".join(MISSING_3RD_PARTY_MODULES))
        print("Some of this program's functionality will not be available.\n")
    
    if len(sys.argv) == 1:
        # only python script supplied
        # update source list
        if not ("lxml" in MISSING_3RD_PARTY_MODULES or "requests" in MISSING_3RD_PARTY_MODULES):
            print("Updating list of classes. This may take a little while...")
            
            # backwards compatible way of not printing a newline at the end
            sys.stdout.write("Fetching Java standard library classes")
            
            page = requests.get("http://docs.oracle.com/javase/7/docs/api/allclasses-frame.html")
            tree = html.fromstring(page.content)
            
            # I can do "sys.stdout.write(".") and ..." here because the write method returns
            # the number of characters written, and so it will always be 1, i.e. truthful
            allStdlibClasses = [sys.stdout.write(".") and a.replace(".html", "").replace("/", ".") for a in tree.xpath('//a[@target="classFrame"]/@href')]
            
            page = requests.get("https://developer.android.com/reference/classes.html")
            tree = html.fromstring(page.content)
            
            sys.stdout.write("\nFetching Android API classes")
            allAndroidClasses = [sys.stdout.write(".") and a.replace("https://developer.android.com/reference/", "").replace(".html", "").replace("/", ".") for a in tree.xpath('//td[@class="jd-linkcol"]/a/@href')]
            allClasses = set(allStdlibClasses+allAndroidClasses)
            
            with open(os.path.join(FILELOCATION, "java_classes.list"), "w") as classlist:
                for a in allClasses:
                    classlist.write(a + "\n")
            
            print("\nList of classes to search for updated.")
        else:
            print("Error - missing modules: " + ("lxml and requests" if "requests" in MISSING_3RD_PARTY_MODULES else "lxml") if "lxml" in MISSING_3RD_PARTY_MODULES else "requests")
    else:
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-i":
                # insert mode; insert directly in java files specified
                # by the following arguments
                for line in fileinput.input(files=sys.argv[i+1:], inplace=True):
                    # fileinput is kinda strange, but it works
                    # For reference, here's what happens:
                    # 1) The original files are moved to backup files
                    # 2) The standard output is redirected to the original files
                    #    within the loop
                    # 3) Thus any calls to print write back to the original files
                    #
                    # Thanks to http://stackoverflow.com/a/290494 for the tip
                    
                    if line.startswith("import"):
                        with open(os.path.join(FILELOCATION, "java_classes.list"), "r") as classlist:
                            for c in classlist:
                                if c.rstrip().endswith("." + re.sub("import |;", "", line.rstrip())):
                                    print("import %s;" %c.rstrip())
                                    break
                            else:
                                # the loop was unbroken; default to the original line
                                print(line.rstrip("\n"))
                    else:
                        # not an import line; let's keep it
                        print(line.rstrip("\n"))
                break # because we just looped over everything
            elif sys.argv[i] == "-o":
                # output mode; output import statements to file in cwd
                with open("import_statements.txt", "a") as o:
                    # loop over the rest of the args
                    for cti in sys.argv[i+1:]:
                        with open(os.path.join(FILELOCATION, "java_classes.list"), "r") as classlist:
                            for c in classlist:
                                if c.rstrip().endswith(".%s" %cti):
                                    o.write("import %s;\n" %c.rstrip())
                                    break
                print("Output at ./import_statements.txt")
                break # because we just looped over everything
            elif sys.argv[i] == "-c":
                # clipboard mode; paste import statements to clipboard
                if "pyperclip" not in MISSING_3RD_PARTY_MODULES:
                    import_str = ""
                    for cti in sys.argv[i+1:]:
                        with open(os.path.join(FILELOCATION, "java_classes.list"), "r") as classlist:
                            for c in classlist:
                                if c.rstrip().endswith(".%s" %cti):
                                    import_str += "import %s;%s" %(c.rstrip(), os.linesep)
                                    break
                    pyperclip.copy(import_str)
                    break # same as above
                else:
                    print("Error - missing modules: pyperclip")
                    sys.exit()
            else:
                # regular mode; output to stdout
                with open(os.path.join(FILELOCATION, "java_classes.list"), "r") as classlist:
                    for c in classlist:
                        if c.rstrip().endswith("." + re.sub("import |;", "", sys.argv[i])):
                            print("import %s;" %c.rstrip())
                            break
