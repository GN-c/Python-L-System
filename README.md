# Python L-System
### Command Line Utility for L-system pattern generation and export
#### for Simply generating pattern input:
 ###### each input has own validation, so do not worry about messing up
- Axiom
- Turning angle
- Evolution
- Rules In Format - In=>Out -,Seperate Rules With Commas
- Svg export Yes/No

#### Required Python Modules
- [PyInquirer](https://github.com/CITGuru/PyInquirer "PyInquirer") for rich terminal interface
- Turtle for drawing | *Comes with Python by default*
- string for string interpolation
- io for saving UTF-8 file

##### turtle window will open up for drawing, also in directory where main.py is located there will be created svg file if chosen so

------------
![](https://github.com/GN-c/turtle-L-systems/blob/main/bg.png?raw=true)
###### svg export sample file

------------
### Avaliable predefined commands
| Command  | action  |
| ------------ | ------------ |
|  F | move forward |
| f  | move forward  |
| B  |  move backward |
| b  |  move backward |
| +  |  turn left by angle |
| -  |  turn right by angle |
| [  |  push state |
| ]  |  pop state |


------------

##### Originaly made for university presentation
##### &copy; GN
