rsp-jupyter
===========

This directory contains the rsp-jupyter Jupyter Notebook plugin for integrating Jupyter with various RSP functions. The plugin currently has the following features:

* Writes opened notebooks locations to the user's RStudio state folder, and displays recently opened notebooks on the homepage under recent projects.
* Provides a button within the notebook that can be clicked which will take the user back to the RStudio Server Pro homepage.

# Requirements

- Python 2.7.9 or Python 3.4.0 and higher
- Jupyter Notebook 5.x
- [pip](https://pypi.org/project/pip/)
- [wheel](https://pypi.org/project/wheel/)
- [RStudio Server Pro] v1.2.0 or higher

If using `conda`, `pip` and `wheel` should already be installed.

# Installation

Install the `rsp-jupyter` package with the following command:

```bash
pip install rsp_jupyter
```

Enable the `rsp-jupyter` extension with the following commands:

```bash
# Install `rsconnect-jupyter` as a jupyter extension
jupyter-nbextension install --sys-prefix --py rsp_jupyter

# Enable JavaScript extension
jupyter-nbextension enable --sys-prefix --py rsp_jupyter
```

Note: The above commands only need to be run once when installing
`rsp_jupyter`.

# Uninstalling

First disable and remove the `rsp-jupyter` notebook extension:

```bash
# Remove JavaScript extension
jupyter-nbextension uninstall --sys-prefix --py rsp_jupyter
```

Finally, uninstall the `rsp-jupyter` python package:

```bash
pip uninstall rsp_jupyter
```

# Upgrading

To upgrade `rsp-jupyter`, first uninstall the extension and then re-install it.

