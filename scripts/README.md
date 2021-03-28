# Scripts Folder

- contains jupyter notebooks which generate latex files which include chordpro and pdf files

## Conda Environment

```shell
conda create -n chordpro-song-book python=3.9 pandas numpy jinja2

conda install -c conda-forge jupyterlab

conda install -c conda-forge nbstripout

# cd to root of repo
nbstripout --install

# Check if nbstripout is installed in the current repository (exits with code 0 if installed, 1 otherwise):
nbstripout --is-installed

# Print status of nbstripout installation in the current repository and configuration summary of filter and attributes if installed (exits with code 0 if installed, 1 otherwise):
nbstripout --status
```

## Write Latex files with python

- [slides-ziegenhagen-python.pdf](https://tug.org/tug2019/slides/slides-ziegenhagen-python.pdf)
