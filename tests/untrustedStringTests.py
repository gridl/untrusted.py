# This file contains fairly exhaustive tests of almost all the methods
# supported by the Python `str` type, and tests that `untrusted.string` type:
# * correctly supports the same methods
# * accepts `str` and/or `untrusted.string` arguments interchangeably
# * never returns `str` or any iterable of `str`, only an
#   appropriate `untrusted.*` type.
# Also tests that subclassed instances of untrusted.string work


import untrusted
from sys import stderr
import html


class customstring(untrusted.string):
    pass


def same(a, b):
    if type(a) != type(b):
        return False
    if isinstance(a, untrusted.string):
        a = a.value
    if isinstance(b, untrusted.string):
        b = b.value
    if a != b:
        return False
    return True


# Test the test
assert same("cat", "cat")
assert not same("cat", "dog")

assert same(untrusted.string("cat"), untrusted.string("cat"))
assert not same(untrusted.string("cat"), untrusted.string("dog"))

assert not same(untrusted.string("cat"), "cat")
assert not same("cat", untrusted.string("cat"))

assert not same("cat", None)
assert not same(untrusted.string("cat"), None)

assert not same(untrusted.string("cat"), customstring("cat"))

assert same(None, None)


# Test an untrusted.string is never None!
try:
    _ = untrusted.string(None)
    raise AssertionError
except TypeError:
    pass


# Test an untrusted.string doesn't print!
try:
    print(untrusted.string("Hello"))
    raise AssertionError
except TypeError:
    pass # expected!


# Test the subclassed string doesn't print!
try:
    print(customstring("Hello"))
    raise AssertionError
except TypeError:
    pass # expected!



# "Strings implement all of the common sequence operations"
# https://docs.python.org/3.4/library/stdtypes.html#typesseq-common


# membership: x in s
assert "a" in "cat"
assert "a" in untrusted.string("cat")
assert untrusted.string("a") in untrusted.string("cat")

assert not ("b" in "cat")
assert not ("b" in untrusted.string("cat"))
assert not (untrusted.string("b") in untrusted.string("cat"))

assert "cat" in "dogcatmouse"
assert "cat" in untrusted.string("dogcatmouse")
assert untrusted.string("cat") in untrusted.string("dogcatmouse")

assert customstring("a") in untrusted.string("cat")
assert untrusted.string("a") in customstring("a")


# membership: x not in s
assert "b" not in "cat"
assert "b" not in untrusted.string("cat")
assert untrusted.string("b") not in untrusted.string("cat")

assert not ("a" not in "cat")
assert not ("a" not in untrusted.string("cat"))
assert not (untrusted.string("a") not in untrusted.string("cat"))

assert customstring("b") not in untrusted.string("cat")


# concatenation: s + t
assert same("cat"+"dog", "catdog")
assert same(untrusted.string("cat") + "dog", untrusted.string("catdog"))
assert same("cat" + untrusted.string("dog"), untrusted.string("catdog"))
assert same(untrusted.string("cat") + untrusted.string("dog"), untrusted.string("catdog"))

# concatination with subclasses - becomes left-most class
assert same(untrusted.string("a") + customstring("b"), untrusted.string("ab"))
assert same(customstring("a") + untrusted.string("b"), customstring("ab"))


# s * n or n * s - "equivalent to adding s to itself n times"
assert same(3*"cat", "catcatcat")
assert same(3*untrusted.string("cat"), untrusted.string("catcatcat"))
assert same(3*customstring("cat"), customstring("catcatcat"))
assert same("cat"*3, "catcatcat")
assert same(untrusted.string("cat")*3, untrusted.string("catcatcat"))
assert same(customstring("cat")*3, customstring("catcatcat"))

assert same(0*"cat", "")
assert same(0*untrusted.string("cat"), untrusted.string(""))
assert same("cat"*0, "")
assert same(untrusted.string("cat")*0, untrusted.string(""))

# s[i] - item at index i
assert same("cat"[1], "a")
assert same(untrusted.string("cat")[1], untrusted.string("a"))

assert same("cat"[-1], "t")
assert same(untrusted.string("cat")[-1], untrusted.string("t"))

try:
    _ = "cat"[4]
    raise AssertionError
except IndexError:
    pass # expected!

try:
    _ = untrusted.string("cat")[4]
    raise AssertionError
except IndexError:
    pass # expected!


# s[i:j:k] - slice i to j with step k
assert same("dogcatmouse"[3:6], "cat")
assert same(untrusted.string("dogcatmouse")[3:6], untrusted.string("cat"))
assert same(customstring("dogcatmouse")[3:6], customstring("cat"))

assert same("dogcatmouse"[3:6:2], "ct")
assert same(untrusted.string("dogcatmouse")[3:6:2], untrusted.string("ct"))
assert same(customstring("dogcatmouse")[3:6:2], customstring("ct"))


# len(s)
assert len("cat") == 3
assert len(untrusted.string("cat")) == 3


#min(s)	smallest item of s	 
assert same(min("cat"), "a")
assert same(min(untrusted.string("cat")), untrusted.string("a"))


#max(s)	largest item of s	 
assert same(max("cat"), "t")
assert same(max(untrusted.string("cat")), untrusted.string("t"))


# s.index(x[, i[, j]])
# "index of the first occurrence of x in s
# (at or after index i and before index j)"
assert "cat".index("a") == 1
assert untrusted.string("cat").index("a") == 1

assert "dogcatmouse".index("cat") == 3
assert untrusted.string("dogcatmouse").index("cat") == 3
assert untrusted.string("dogcatmouse").index(untrusted.string("cat")) == 3


# s.count(x) - occurrences of x in s
assert "cat".count("a") == 1
assert untrusted.string("cat").count("a") == 1
assert untrusted.string("cat").count(untrusted.string("a")) == 1

assert "cataclasm".count("a") == 3
assert untrusted.string("cataclasm").count("a") == 3
assert untrusted.string("cataclasm").count(untrusted.string("a")) == 3

assert "cat attack".count("at") == 2
assert untrusted.string("cat attack").count("at") == 2
assert untrusted.string("cat attack").count(untrusted.string("at")) == 2


# x.join(y)
assert same(''.join([]), "")
assert same(untrusted.string('').join([]), untrusted.string(""))
assert same(''.join("cat"), "cat")
assert same(untrusted.string('').join("cat"), untrusted.string("cat"))
assert same(untrusted.string('').join(untrusted.string("cat")), untrusted.string("cat"))

# sorry, ''.join(untrusted.string(...)) won't work
# but let's make sure we get an exception
# to be certain that an untrusted.string doesn't ever leak into a normal str
try:
    _ = ''.join(untrusted.string("hello"))
    raise AssertionError
except TypeError:
    pass # expected

try:
    _ = ''.join(customstring("hello"))
    raise AssertionError
except TypeError:
    pass # expected


# x.reversed()
assert ''.join(reversed("cat")) == "tac"
assert untrusted.string('').join(reversed(untrusted.string("cat"))) == untrusted.string("tac")


# iteration
for i in "cat":
    assert same(i, "c") or same(i, "a") or same(i, "t")

for i in untrusted.string("cat"):
    assert same(i, untrusted.string("c")) or same(i, untrusted.string("a")) or same(i, untrusted.string("t"))



# string methods
# https://docs.python.org/3.4/library/stdtypes.html#string-methods

# str.capitalize()
assert same("cAt".capitalize(), "Cat")
assert same(untrusted.string("cAt").capitalize(), untrusted.string("Cat"))


# str.casefold()
assert same("Catß".casefold(), "catss")
assert same(untrusted.string("Catß").casefold(), untrusted.string("catss"))

# str.center(width[, fillchar])
assert same("cat".center(7), "  cat  ")
assert same(untrusted.string("cat").center(7), untrusted.string("  cat  "))
assert same("cat".center(7, "-"), "--cat--")
assert same(untrusted.string("cat").center(7, "-"), untrusted.string("--cat--"))
assert same(untrusted.string("cat").center(7, untrusted.string("-")), untrusted.string("--cat--"))

# str.count(sub[, start[, end]])
assert "dogcatmousecat".count("cat", 0, 3) == 0
assert "dogcatmousecat".count("cat", 3, 6) == 1
assert "dogcatmousecat".count("cat", 3) == 2

assert untrusted.string("dogcatmousecat").count("cat", 0, 3) == 0
assert untrusted.string("dogcatmousecat").count("cat", 3, 6) == 1
assert untrusted.string("dogcatmousecat").count("cat", 3) == 2

assert untrusted.string("dogcatmousecat").count(untrusted.string("cat"), 0, 3) == 0
assert untrusted.string("dogcatmousecat").count(untrusted.string("cat"), 3, 6) == 1
assert untrusted.string("dogcatmousecat").count(untrusted.string("cat"), 3) == 2


# str.encode
# disabled on purpose for untrusted.string!!!

assert same("cat".encode("ascii"), b"cat")

try:
    _ = untrusted.string("cat").encode("ascii")
    raise AssertionError
except TypeError:
    pass # expected!


# str.endswith(suffix[, start[, end]])
assert "catdogmouse".endswith("mouse")
assert untrusted.string("catdogmouse").endswith("mouse")
assert untrusted.string("catdogmouse").endswith(untrusted.string("mouse"))

assert not "catdogmouse".endswith("cat")
assert not untrusted.string("catdogmouse").endswith("cat")
assert not untrusted.string("catdogmouse").endswith(untrusted.string("cat"))

assert "catdogmouse".endswith("dog", 0, 6)
assert untrusted.string("catdogmouse").endswith("dog", 0, 6)
assert untrusted.string("catdogmouse").endswith(untrusted.string("dog"), 0, 6)

assert not "catdogmouse".endswith("dog", 4)
assert not untrusted.string("catdogmouse").endswith("dog", 4)
assert not untrusted.string("catdogmouse").endswith(untrusted.string("dog"), 4)


# str.expandtabs(tabsize=8)
assert same("\tHello\tworld!".expandtabs(), "        Hello   world!")
assert same(untrusted.string("\tHello\tworld!").expandtabs(), untrusted.string("        Hello   world!"))


# str.find(sub[, start[, end]])
assert "dogcatmouse".find("cat") == 3
assert untrusted.string("dogcatmouse").find("cat") == 3
assert untrusted.string("dogcatmouse").find(untrusted.string("cat")) == 3

assert "dogcatmouse".find("cat", 4) == -1
assert untrusted.string("dogcatmouse").find("cat", 4) == -1
assert untrusted.string("dogcatmouse").find(untrusted.string("cat"), 4) == -1


# str.format(*args, **kwargs)

# with numeric argument:

assert same(
    "Hello {0}, UserID: {1}".format("Sarah", 123),
    "Hello Sarah, UserID: 123"
)

assert same(
    untrusted.string("Hello {0}, UserID: {1}").format("Sarah", 123),
    untrusted.string("Hello Sarah, UserID: 123")
)

assert same(
    untrusted.string("Hello {0}, UserID: {1}").format(untrusted.string("Sarah"), 123),
    untrusted.string("Hello Sarah, UserID: 123")
)


# ensure untrusted.string never leaks into a str...
try:
    _ =  "Hello {0}, UserID: {1}".format(untrusted.string("Sarah"), 123),
    raise AssertionError
except TypeError:
    pass # expected!



# with named arguments:

assert same(
    "Hello {name}, UserID: {uid}".format(name="Sarah", uid=123),
    "Hello Sarah, UserID: 123"
)

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format(name="Sarah", uid=123),
    untrusted.string("Hello Sarah, UserID: 123")
)

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format(name=untrusted.string("Sarah"), uid=123),
    untrusted.string("Hello Sarah, UserID: 123")
)



# str.format_map(mapping)
assert same(
    "Hello {name}, UserID: {uid}".format_map({"name": "Sarah", "uid": 123}),
    "Hello Sarah, UserID: 123"
)

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format_map({"name": "Sarah", "uid": 123}),
    untrusted.string("Hello Sarah, UserID: 123")
)

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format_map({"name": untrusted.string("Sarah"), "uid": "123"}),
    untrusted.string("Hello Sarah, UserID: 123")
)


# advanced! format_map with an untrusted.mapping!!
myUntrustedDict = untrusted.mapping({'name': 'Sarah', "uid": "123"})

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format_map(myUntrustedDict),
    untrusted.string("Hello Sarah, UserID: 123")
)


# ensure untrusted.mapping never leaks into a str...
try:
    _ =  "Hello {name}, UserID: {uid}".format_map(myUntrustedDict),
    raise AssertionError
except TypeError:
    pass # expected!


# str.index(sub[, start[, end]])
# "Like find(), but raise ValueError when the substring is not found."

assert "dogcatmouse".index("cat") == 3
assert untrusted.string("dogcatmouse").index("cat") == 3
assert untrusted.string("dogcatmouse").index(untrusted.string("cat")) == 3

try:
    _ = "dogcatmouse".index("tiger")
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").index("tiger")
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").index(untrusted.string("tiger"))
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = "dogcatmouse".index("cat", 4)
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").index("cat", 4)
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").index(untrusted.string("cat"), 4)
    raise AssertionError
except ValueError:
    pass # expected


# str.isalnum()
assert "cat".isalnum()
assert untrusted.string("cat").isalnum()
assert not "£123".isalnum()
assert not untrusted.string("£123").isalnum()

# str.isalpha()
assert "cat".isalpha()
assert untrusted.string("cat").isalpha()
assert not "123".isalpha()
assert not untrusted.string("123").isalpha()

# str.isdecimal()
assert "123".isdecimal()
assert untrusted.string("123").isdecimal()
assert not "cat".isdecimal()
assert not untrusted.string("cat").isdecimal()

# str.isdigit()
assert "2²".isdigit()
assert untrusted.string("2²").isdigit()

# str.isidentifier()
assert "hello".isidentifier()
assert untrusted.string("hello").isidentifier()
assert not "123".isidentifier()
assert not untrusted.string("123").isidentifier()

# str.islower()
assert "hello".islower()
assert untrusted.string("hello").islower()
assert not "Hello".islower()
assert not untrusted.string("Hello").islower()

# str.isnumeric()
assert "123".isnumeric()
assert untrusted.string("123").isnumeric()
assert not "hello".isnumeric()
assert not untrusted.string("hello").isnumeric()

# str.isprintable()
assert "123".isprintable()
assert untrusted.string("123").isprintable()
assert not "\01".isprintable()
assert not untrusted.string("\01").isprintable()

# str.isspace()
assert "    \t\r\n".isspace()
assert untrusted.string("    \t\r\n").isspace()
assert not "cat".isspace()
assert not untrusted.string("cat").isspace()

# str.istitle()
assert "Hello World".istitle()
assert untrusted.string("Hello World").istitle()
assert not "hello world".istitle()
assert not untrusted.string("hello world").istitle()

# str.isupper()
assert "CAT".isupper()
assert untrusted.string("CAT").isupper()
assert not "cat".isupper()
assert not untrusted.string("cat").isupper()

# str.join(iterable) - done

# str.ljust(width[, fillchar])
assert same("CAT".ljust(8, "-"), "CAT-----")
assert same(untrusted.string("CAT").ljust(8, "-"), untrusted.string("CAT-----"))

# str.lower()
assert same("Cat".lower(), "cat")
assert same(untrusted.string("Cat").lower(), untrusted.string("cat"))

# str.lstrip([chars])
assert same(" cat".lstrip(), "cat")
assert same(untrusted.string(" cat".lstrip()), untrusted.string("cat"))
assert same(" cat".lstrip(" ca"), "t")
assert same(untrusted.string(" cat").lstrip(" ca"), untrusted.string("t"))
assert same(untrusted.string(" cat").lstrip(untrusted.string(" ca")), untrusted.string("t"))
assert same(untrusted.string(" cat").lstrip(customstring(" ca")), untrusted.string("t"))


# str.partition(sep)

# no result
parts = "cat,dog,mouse".partition("X")
a, b, c = parts
assert same(a, "cat,dog,mouse")
assert same(b, "")
assert same(c, "")

parts = untrusted.string("cat,dog,mouse").partition("X")
a, b, c = parts
assert same(a, untrusted.string("cat,dog,mouse"))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string(""))

parts = untrusted.string("cat,dog,mouse").partition(untrusted.string("X"))
a, b, c = parts
assert same(a, untrusted.string("cat,dog,mouse"))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string(""))

parts = customstring("cat,dog,mouse").partition(untrusted.string("X"))
a, b, c = parts
assert same(a, customstring("cat,dog,mouse"))
assert same(b, customstring(""))
assert same(c, customstring(""))

parts = untrusted.string("cat,dog,mouse").partition(customstring("X"))
a, b, c = parts
assert same(a, untrusted.string("cat,dog,mouse"))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string(""))

# result
parts = "cat,dog,mouse".partition(",")
a, b, c = parts
assert same(a, "cat")
assert same(b, ",")
assert same(c, "dog,mouse")

parts = untrusted.string("cat,dog,mouse").partition(",")
a, b, c = parts
assert same(a, untrusted.string("cat"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("dog,mouse"))

parts = untrusted.string("cat,dog,mouse").partition(untrusted.string(","))
a, b, c = parts
assert same(a, untrusted.string("cat"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("dog,mouse"))

parts = customstring("cat,dog,mouse").partition(untrusted.string(","))
a, b, c = parts
assert same(a, customstring("cat"))
assert same(b, customstring(","))
assert same(c, customstring("dog,mouse"))

parts = untrusted.string("cat,dog,mouse").partition(customstring(","))
a, b, c = parts
assert same(a, untrusted.string("cat"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("dog,mouse"))


# TODO str % thing


# TODO tests for:
'''
TODO


str.replace(old, new[, count])
Return a copy of the string with all occurrences of substring old replaced by new. If the optional argument count is given, only the first count occurrences are replaced.

str.rfind(sub[, start[, end]])
Return the highest index in the string where substring sub is found, such that sub is contained within s[start:end]. Optional arguments start and end are interpreted as in slice notation. Return -1 on failure.

str.rindex(sub[, start[, end]])
Like rfind() but raises ValueError when the substring sub is not found.

str.rjust(width[, fillchar])
Return the string right justified in a string of length width. Padding is done using the specified fillchar (default is an ASCII space). The original string is returned if width is less than or equal to len(s).

str.rpartition(sep)
Split the string at the last occurrence of sep, and return a 3-tuple containing the part before the separator, the separator itself, and the part after the separator. If the separator is not found, return a 3-tuple containing two empty strings, followed by the string itself.

str.rsplit(sep=None, maxsplit=-1)
Return a list of the words in the string, using sep as the delimiter string. If maxsplit is given, at most maxsplit splits are done, the rightmost ones. If sep is not specified or None, any whitespace string is a separator. Except for splitting from the right, rsplit() behaves like split() which is described in detail below.

str.rstrip([chars])
Return a copy of the string with trailing characters removed. The chars argument is a string specifying the set of characters to be removed. If omitted or None, the chars argument defaults to removing whitespace. The chars argument is not a suffix; rather, all combinations of its values are stripped:

>>>
>>> '   spacious   '.rstrip()
'   spacious'
>>> 'mississippi'.rstrip('ipz')
'mississ'
str.split(sep=None, maxsplit=-1)
Return a list of the words in the string, using sep as the delimiter string. If maxsplit is given, at most maxsplit splits are done (thus, the list will have at most maxsplit+1 elements). If maxsplit is not specified or -1, then there is no limit on the number of splits (all possible splits are made).

If sep is given, consecutive delimiters are not grouped together and are deemed to delimit empty strings (for example, '1,,2'.split(',') returns ['1', '', '2']). The sep argument may consist of multiple characters (for example, '1<>2<>3'.split('<>') returns ['1', '2', '3']). Splitting an empty string with a specified separator returns [''].

For example:

>>>
>>> '1,2,3'.split(',')
['1', '2', '3']
>>> '1,2,3'.split(',', maxsplit=1)
['1', '2,3']
>>> '1,2,,3,'.split(',')
['1', '2', '', '3', '']
If sep is not specified or is None, a different splitting algorithm is applied: runs of consecutive whitespace are regarded as a single separator, and the result will contain no empty strings at the start or end if the string has leading or trailing whitespace. Consequently, splitting an empty string or a string consisting of just whitespace with a None separator returns [].

For example:

>>>
>>> '1 2 3'.split()
['1', '2', '3']
>>> '1 2 3'.split(maxsplit=1)
['1', '2 3']
>>> '   1   2   3   '.split()
['1', '2', '3']
str.splitlines([keepends])
Return a list of the lines in the string, breaking at line boundaries. Line breaks are not included in the resulting list unless keepends is given and true.

This method splits on the following line boundaries. In particular, the boundaries are a superset of universal newlines.

Representation	Description
\n	Line Feed
\r	Carriage Return
\r\n	Carriage Return + Line Feed
\v or \x0b	Line Tabulation
\f or \x0c	Form Feed
\x1c	File Separator
\x1d	Group Separator
\x1e	Record Separator
\x85	Next Line (C1 Control Code)
\u2028	Line Separator
\u2029	Paragraph Separator
Changed in version 3.2: \v and \f added to list of line boundaries.

For example:

>>>
>>> 'ab c\n\nde fg\rkl\r\n'.splitlines()
['ab c', '', 'de fg', 'kl']
>>> 'ab c\n\nde fg\rkl\r\n'.splitlines(keepends=True)
['ab c\n', '\n', 'de fg\r', 'kl\r\n']
Unlike split() when a delimiter string sep is given, this method returns an empty list for the empty string, and a terminal line break does not result in an extra line:

>>>
>>> "".splitlines()
[]
>>> "One line\n".splitlines()
['One line']
For comparison, split('\n') gives:

>>>
>>> ''.split('\n')
['']
>>> 'Two lines\n'.split('\n')
['Two lines', '']
str.startswith(prefix[, start[, end]])
Return True if string starts with the prefix, otherwise return False. prefix can also be a tuple of prefixes to look for. With optional start, test string beginning at that position. With optional end, stop comparing string at that position.

str.strip([chars])
Return a copy of the string with the leading and trailing characters removed. The chars argument is a string specifying the set of characters to be removed. If omitted or None, the chars argument defaults to removing whitespace. The chars argument is not a prefix or suffix; rather, all combinations of its values are stripped:

>>>
>>> '   spacious   '.strip()
'spacious'
>>> 'www.example.com'.strip('cmowz.')
'example'
str.swapcase()
Return a copy of the string with uppercase characters converted to lowercase and vice versa. Note that it is not necessarily true that s.swapcase().swapcase() == s.

str.title()
Return a titlecased version of the string where words start with an uppercase character and the remaining characters are lowercase.

For example:

>>>
>>> 'Hello world'.title()
'Hello World'
The algorithm uses a simple language-independent definition of a word as groups of consecutive letters. The definition works in many contexts but it means that apostrophes in contractions and possessives form word boundaries, which may not be the desired result:

>>>
>>> "they're bill's friends from the UK".title()
"They'Re Bill'S Friends From The Uk"
A workaround for apostrophes can be constructed using regular expressions:

>>>
>>> import re
>>> def titlecase(s):
...     return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
...                   lambda mo: mo.group(0)[0].upper() +
...                              mo.group(0)[1:].lower(),
...                   s)
...
>>> titlecase("they're bill's friends.")
"They're Bill's Friends."
str.translate(table)
Return a copy of the string in which each character has been mapped through the given translation table. The table must be an object that implements indexing via __getitem__(), typically a mapping or sequence. When indexed by a Unicode ordinal (an integer), the table object can do any of the following: return a Unicode ordinal or a string, to map the character to one or more other characters; return None, to delete the character from the return string; or raise a LookupError exception, to map the character to itself.

You can use str.maketrans() to create a translation map from character-to-character mappings in different formats.

See also the codecs module for a more flexible approach to custom character mappings.

str.upper()
Return a copy of the string with all the cased characters [4] converted to uppercase. Note that str.upper().isupper() might be False if s contains uncased characters or if the Unicode category of the resulting character(s) is not “Lu” (Letter, uppercase), but e.g. “Lt” (Letter, titlecase).

The uppercasing algorithm used is described in section 3.13 of the Unicode Standard.

str.zfill(width)

'''

