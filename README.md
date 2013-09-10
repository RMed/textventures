TextVentures
============

A simple text-based adventure system written for **Python 2.7**.
- Visit the [TextVentures wiki](https://github.com/RMed/textventures/wiki) for more information regarding the project, adventure creation, etc.
- Visit the [Adventure repository](https://github.com/RMed/textventures_stories) to download adventures to play.


## Building TextVentures
TextVentures uses distutils for building and distributing the code. The ***tools*** directory contains several custom build tools (such as translation compilation scripts). Some of these tools are executed automatically when a setup command is issued (i.e. *buil_trans* is executed with the *build* command).


### Direct build
The setup script will allow you to build the code by navigating to the source root and typing:

```
$ python setup.py build
```

This will result in a new directory named ***build*** that contains a ready to go copy of TextVentures.

NOTE: trying to create a distribution package is not yet supported.

### Compile translations
The translations used for TextVentures are located in the ***po*** directory. If you want/need to only compile these translations, type:

```
$ python setup.py build_trans
```

The resulting **.mo** files can be located under *build/textventures/locale/*.


## Running TextVentures
In order to run TextVentures, simply navigate to the ***build*** directory (after successufully building the source) and type:

```
$ python play_textventures.py
```

