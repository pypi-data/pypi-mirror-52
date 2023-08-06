# sassy

[![Build Status](https://travis-ci.org/jmsmistral/sassy.svg?branch=master)](https://travis-ci.org/jmsmistral/sassy)

A simple but powerful templating language for text interpolation inspired by sas macros.

## How it works

**Sassy** is a command-line program that **interpolates text** by interpreting a set of pre-defined **tags** that control text replacement, and loops, amongst other things.
- A tag starts with a `%` and ends with a `;`.
- Everything that is not a tag, or within open/close tags is interpreted as plaintext and is left untouched.

Below is a description of each tag, with examples.

### Macros
- Macros are named blocks of text enclosed within `%macro` and `%mend` tags, that are interpolated when executed. A macro can be executed at any point after it is defined

- A macro looks a lot like a function, and must be given a name and a list of parameters within parentheses (empty for no parameters): `%macro <name>(<param>, ...);`

- Macros are executed with the `%exec` tag, referencing the macro name, and passing the required parameters (if any)

- When run, macros will interpolate parameters and tags within it's body, and output the resulting string

- Macros currently accept a maximum number of 25 parameters

***test.txt***
```    
%macro testMacro(param1);
    this text will show whenever the macro is called.
    we can reference macro parameters like this: &param1.
%mend;

here's how you call a macro:
%exec testMacro(1);

here's a call to the same macro with a different parameter:
%exec testMacro(a parameter can contain spaces);
```

Running `sassy test.txt` will generate the following... 

```
Here's how you execute a macro:
    This text will be interpolated whenever the macro is executed.
    We can reference macro parameters like this: 1

Here's a call to the same macro with a different parameter:
    This text will be interpolated whenever the macro is executed.
    We can reference macro parameters like this: a parameter can contain spaces
```


### Variables
- Variables are named references to strings, which can be used within macros, and loop blocks

- Variables are declared using the `%let` tag, as follows: `%let <name> = <value>;`

- The value is includes everything after the equal symbol `=`

- Variables can be referenced by wrapping the variable name within `&` and `.`, e.g. `&<name>.`

- Macro parameters are referenced in the same way as variables, `&<param>.`

- Variables references can be nested (see example below)

***test.txt***
```
%let var1 = some value;
%let var2 = some other value;
%let varNum =2;

%macro testMacro(param1);
    Here's how you reference variables: &var1.
    Macro parameters are referenced in the same way as variables: &param1.
    Variables and parameters can be nested to dynamically compose references to other variables: &var&varNum..
%mend;

Here's what that looks like:
%exec testMacro(1);

%exec testMacro(2);
```

Running `sassy test.txt` will generate the following... 
``` 
Here's what that looks like:
    Here's how you reference variables:  some value
    Macro parameters are referenced in the same way as variables: 1
    Variables and parameters can be nested to dynamically compose references to other variables:  some other value

    Here's how you reference variables:  some value
    Macro parameters are referenced in the same way as variables: 2
    Variables and parameters can be nested to dynamically compose references to other variables:  some other value
```


### Loops
- Loops are blocks of text enclosed within `%procloop` and `%pend` tags, that are interpolated multiple times in succession

- Unlike macros, loops do not have names and are interpolated in-place

- A loop is declared as follows: `%procloop (<integer>) <counter_name>;`
    - `<integer>` - Defines the number of times the loop will execute. This can also be a reference to a variable
    - `<counter_name>` - Is a name given to the loop counter, that can be referenced within the loop body as a variable

- The loop counter is zero-based


***test.txt***
```
This is how you execute a loop:
%procloop (3) loopCounter;
    This loop will execute &loopCounter. times.
%pend;

You can also use a variable to set the number of iterations:
%let loopVar0 = first loop;
%let loopVar1 = second loop;
%let loopVar2 = third loop;
%let loopVar3 = fourth loop;
%let numLoops = 4;
%procloop (&numLoops.) counterVar;
    This other loop will execute &counterVar. times, and references a different variable each time: &loopVar&counterVar..
%pend;
```

Running `sassy test.txt` will generate the following... 
```
This is how you execute a loop:
    This loop will execute 0 times.
    This loop will execute 1 times.
    This loop will execute 2 times.

You can also use a variable to set the number of iterations:
    This other loop will execute 0 times, and references a different variable each time:  first loop
    This other loop will execute 1 times, and references a different variable each time:  second loop
    This other loop will execute 2 times, and references a different variable each time:  third loop
    This other loop will execute 3 times, and references a different variable each time:  fourth loop
```

---

## Installation

Here's what you need to do to install sassy:

### Python 3.6+

Sassy is compatible with **Python 3.6 and later**.

On Unix systems, install Python 3.6 (or later) via your package manager (apt, rpm, yum, brew).
Alternatively, you can download an installation package from the [official Python downloads page](https://www.python.org/downloads/)

### Virtual Environment

It is recommended to put all project dependencies into its own virtual
environment - this way we don't pollute the global Python installation.
For this we recommend you use **virtualenvwrapper**. Follow the instructions
[here](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)
to get this installed. Once you have virtualenvwrapper install, create
a new virtual environment with:

```bash
mkvirtualenv sassy
workon sassy
```

Now let's install sassy:

```bash
pip install sassylang
```

### Get help or give help

-  Open a new [issue](https://github.com/jmsmistral/sassy/issues/new) you encounter a problem.
-  Pull requests welcome. You can help with language features!

---

## License

-  sassy is Free Software and licensed under the [GPLv3](https://github.com/jmsmistral/macrosql/blob/master/LICENSE.txt)
-  Main author is [@jmsmistral](https://github.com/jmsmistral)

