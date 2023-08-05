﻿jk_rawhtml
==========

Introduction
------------

This python module provides support for programmatically generating HTML5 code.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-rawhtml)
* [pypi.python.org](https://pypi.python.org/pypi/jk_rawhtml)

Motivation
----------

In most use cases it is very convenient to use one of the many template languages to create HTML output.
But using a template engine will require ...

* including another module in the source
* packing a variety of additional files into your software

While including another Python module is probably the least of your concern unfortunately there are some
use cases where a more simplistic approach would be much more convenient: Whenever you do *not* want to
include more files into the software you provide or whenever you do very simple things and don't want to
overcomplicate your software.

This work has been inspired by some old work of Tavis Rudd
(https://bitbucket.org/tavisrudd/throw-out-your-templates) which - at the
time of this writing - seems to have been abandoned as his code is neither a real python module nor does
it support Python 3.

The goal of this new module `jk_rawhtml` is to provide an easy way of generating state-of-the-art HTML5
code programmatically and being well suited to use in recent Python prorgams. A completely new implementation
approach has been taken in order to implement this module `jk_rawhtml` in Python 3 as a state-of-the-art module.
The idea of `jk_rawhtml` is to provide a simple, well structured, maintainable approach for HTML generation
with support for CSS and SVG (in the long run) by intentionally leaving out older HTML standards
as these are obsolete now obsolete.

As this module is quite new and not every detail has yet been implemented, it already is ready to be used
and should not have any serious bugs. If you find any issues, please feel free to report them.

How to use this module
----------------------

### Loading the module

If you want to use the functionality provided by this module you're best adviced to include the module with following statement:

    from jk_rawhtml import *

Creating a HTML page
--------------------

### The HTML tag generator object

In order to create a HTML page you need to use an instance of `HTML5Scope` which provides ways to instantiate HTML 5 tags. Example:

```
with HTML5Scope() as H:
	ret = H.html(foo="bar")[
		H.head()[
			H.title[
				"My great web page!"
			]
		],
		H.body(bar="foo")[
		....
		]
	]
```

The HTML 5 scope object is stored in `H` here. It is used to generate all page components.

NOTE: Creating the HTML 5 scope object in a `with`-context is just a matter of taste. Note that this object is just a regular generator
object and does nothing more than generating the HTML page components. You can safely use it in a regular instantiation way as well
if required: `H = HTML5Scope()`

### Creating HTML tags

In order to learn how to create a HTML page please have a look at this example right away:

```
with HTML5Scope() as H:
	ret = H.html(foo="bar")[
		H.head()[
			H.title[
				"My great web page!"
			]
		],
		H.body(bar="foo")[
		H.ul()[
			H.li()[
			"This is a ",
			H.b()["bold"],
			" ",
			H.a(href="https://google.de")[
				"text with > and <"
			],
			"."
			]
		]
		]
	]
```

Every statement such as `H.title[...]` or `H.ul()` or `H.li()[...]` will create and return a HTML tag object that is initialized with data.
In the genereator object stored in `H` a suitable factory member is provided for every valid HTML tag.

During creating of HTML tag objects two kinds of conventions are used:

* Attributes for HTML tags are provided within round brackes.
* Components that are children of another HTML tag element are provided within square brackets.

Examples:

| Example			| Comment		|
|-------------------|---------------|
| `H.a(href="http://example.org")`	| Create a link tag referring to `http://example.org`	|
| `H.a(href="http://example.org")["Test"]`	| Create a link tag referring to `http://example.org` and text `Test`	|
| `H.a["Test"]`	| Create a link tag with text "`Test`"	|
| `H.a()["Test"]`	| Create a link tag with text "`Test`"	|
| `H.a()[]`	| Invalid	|
| `H.a()["A ", "great ", "web ", "site"]`	| Create a link tag with text "`A great web site`". (Components are simply concatenated.)	|
| `H.a()["A ", H.b["great"], " web site"]`	| Create a link tag with text "`A great web site`" where "`great`" is enclosed in a `b`-tag.	|
| `H.ol[ H.li[ "Item A" ], H.li[ "Item B" ] ]`	| Create a ordered list with two list items.	|
| `H.span(style="color: black;")[ "Test" ]`	| Create a span tag with style information and text "`Test`"	|
| `H.span(_style="color: black;")[ "Test" ]`	| Create a span tag with style information and text "`Test`"	|
| `H.span(_class="sth")[ "Test" ]`	| Create a span tag with assigned CSS-class "`sth`" and text "`Test`"	|

Please note that in regular HTML elements ...

* within round brackets ...
	* only key value pairs are allowed
	* any string values get HTML-encoded
	* any trailing underscore will automatically be removed to avoid conflicts with python keywords (f.e. "`_class`" will become "`class`")
* within square brackets ...
	* any strings get HTML-encoded
	* HTML tags and text can be mixed
	* multiple components get concatenated; text gets concatenated without spaces

### Specifying CSS data

As it is convention in HTML style data can be specified for attributes named "`style`". For this you have two options:

* specify style information as a plaintext string: In this case the string will simply be copied to the output without encoding.
* specify style information as a `CSSMAP` object: In this case the object's data will be converted to valid CSS for the output.

Example:

```
H.span(style="color: black;")[
	"The quick brown fox jumps over the lazy dog."
]
```

This will produce the following output:

```
<span style="color: black;">The quick brown fox jumps over the lazy dog.</span>
```

Example:

```
H.span(
	style=CSSMap(
		color="black"
	)
)[
	"The quick brown fox jumps over the lazy dog."
]
```

This will produce the same output:

```
<span style="color: black;">The quick brown fox jumps over the lazy dog.</span>
```

### Creating comments

Multiline comments in HTML can be created as well. Example:

```
H.comment(
	"This is a comment line.",
	"This is another comment line."
)
```

The output is this:

```
<!-- 
This is a comment line.
This is another comment line.
-->
```

As you can see comment data can be provided within round brackets.

But you can use the square bracket syntax as well. Example:

```
H.comment[
	"This is a comment line.",
	"This is another comment line."
]
```

The output is this:

```
<!-- 
This is a comment line.This is another comment line.
-->
```

By convention data within square brackets will be taken "as is" and no additional spaces will be inserted.

### Raw CSS data

You can provide raw CSS data. Example:

```
H.head()[
	H.raw_style_css(
		"p {",
		"	color: black",
		"}"
	)
]
```

This will produce the following output:

```
<head>
	<meta charset="UTF-8">
	<style type="text/css">
		p {
			color: black
		}
	</style>
</head>
```

NOTE: The meta tag is inserted automatically in `<head>` as long as you don't specify it explicitely.

Serializing to string for output
-----------------------

### Serializing

Given that you created a HTML page model using something like this ...

```
with HTML5Scope() as H:
	myData = H.html()[
		H.head()[
			...
		],
		H.body()[
			...
		]
	]

```

... you could convert this to plain teext using the following statement:

```
plaintext = str(myData)
```

Writing the output to a file could therefor be accomplished this way:

```
with open("myhtmlfile.html", "w") as f:
	f.write(str(myData))
```

### HTML 5 output formatting

One more word to HTML 5 output formatting: The current implementation produces pretty printed HTML 5. In order to achieve this specific
tags such as `<b>` or `<a>` or `<span>` will be written inline (without spaces between them) while structural HTML tags such as `<div>`
will produce an indented section and introduce line breaks into the output. Additionally tags such as `<p>` or `<li>` begin a new
indented section but the tag's content will be written in a single line.

Bugs
----

Yes, there will still be some bugs. If you find a bug please report it as an issue on GitHub. Please provide the following information:

* a small python snipplet required to reproduce the bug
* the output of the python snipplet
* the result that you would expect

Thank you!

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



