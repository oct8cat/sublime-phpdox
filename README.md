PhpDox
======

Why?
----
This plugin allows you to generate valid PHPDoc comments for your PHP code by pressing just one hotkey, automatically resolving most of required tags.

Current version supports:

+ Classes
    + ***@uses*** - If the class is extends another class, parent class name will be resolved.
    + ***@category***, ***@package*** - Packaging information.
    + ***@author*** - author information, such as name and email (resolves from Sublime environment).
    + ***@link***, ***@license*** - additional information.

+ Interfaces - same as classes.

+ Class's methods and properties:
    + ***@var*** - Property type. *array*, *string* and *int* types currently supported.
    + ***@param*** - Method's arguments. Arguments' names and types will be resolved and aligned correctly.
    + ***@static*** - *static* modifier resolving.
    + ***@access*** - Access modifer resolving (*public*, *protected*, *private* supported) - defaults to *public*.
    + ***@return*** - Returned value's type and description (Currently hardcoded to *mixed* type).


Where?
------
    https://github.com/oct8cat/sublime-phpdox

How?
----
+ Place cursor to a line with class, interface, method or property declaration.
+ Press **F5**
