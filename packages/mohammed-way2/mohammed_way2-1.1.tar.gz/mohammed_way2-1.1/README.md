# mypackage

A testing package for **Digital Kites** processes.

## Installation

Make sure you have [python3](http://nodejs.org/) and [pip](https://www.npmjs.com/) installed.

```sh
pip install mohammed_way2
```


## Usage

```sh
Importing:
   import mohammed_way2 

Create instance of 'Myclass' in mohammed_way2 module
   name = "Mohammed" #name should be required
   colorObj = mohammed_way2.Myclass(name) 

To get help
    colorObj.help()

Calling methods
   requirements = {
    "foreground":"red",
    "background":"green",
    "extra":"underline" 
   }
   #if you pass requirements={ } it will say back in the default color
   colorObj.sayHai(requirements)
              (or)
   colorObj.sayBye(requirements)

To watch options available for requirements
     colortObj.optionsAvailable()
```

#### How to include in your process:

```sh
import mohammed_way2
name = "Mohammed" #your name
colorObj = mohammed_way2.Myclass(name)
# colorObj.help()
requirements = {
    "foreground":"red",
    "background":"blue",
    "extra":"underline" 
}
# you can pass requirements = {}
colorObj.sayHai(requirements)
colorObj.sayBye(requirements)
# colorObj.optionsAvailable()

```