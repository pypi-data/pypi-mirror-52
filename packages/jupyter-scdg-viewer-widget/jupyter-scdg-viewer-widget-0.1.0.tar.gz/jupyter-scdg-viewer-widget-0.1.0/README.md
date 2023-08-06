SCDG Viewer Widget
===============================

Jupyter Notebook Widget to view SCDG in the form of graph.

This widget project was initialized using the very handy Cookiecutter [template](https://github.com/jupyter-widgets/widget-cookiecutter).

Example
------------

![](example.png)

Installation
------------

To install use pip:

    $ pip install scdgviewer
    $ jupyter nbextension enable --py --sys-prefix scdgviewer

To install for jupyterlab

    $ jupyter labextension install scdgviewer

For a development installation (requires npm),

    $ git clone git@gitlab.inria.fr:TAMIS/madlab/jupyter-scdg-viewer-widget.git
    $ cd jupyter-scdg-viewer-widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix scdgviewer
    $ jupyter nbextension enable --py --sys-prefix scdgviewer
