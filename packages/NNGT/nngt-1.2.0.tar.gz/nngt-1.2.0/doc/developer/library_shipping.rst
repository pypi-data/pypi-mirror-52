================
Library shipping
================

Multiplatform usage:

* NNGT can be used in pure-python mode on any platform
* Compilation of the multithreading algorithms can also be done on all
  available platforms
* To simplify things, precompiled binaries for Linux and Mac (@todo windows)
  are provided directly on PyPi.


The manylinux wheels
====================

To prepare the ``manylinux`` wheels, one must use the docker containers
provided by https://github.com/pypa/manylinux

    docker pull quay.io/pypa/manylinux1_x86_64
    docker start -i dockerID

Once in the container, I wrote an automatic install file (``build_wheels.sh``)
to build NNGT

    #!/bin/bash
    set -e -x

    # Compile wheels
    for PYBIN in /opt/python/*/bin; do
        "${PYBIN}/pip" install -r requirements.txt
        "${PYBIN}/pip" wheel NNGT/ -w wheelhouse/
    done

    # Bundle external shared libraries into the wheels
    for whl in wheelhouse/*.whl; do
        auditwheel repair "$whl" -w wheelhouse/
    done

associated to a ``requirements.txt`` file

    scipy
    networkx
    shapely
    dxfgrabber
    svg.path
    matplotlib

Save these as on the same level as the root ``NNGT`` folder (the one containing
the ``setup.py``), and create a ``wheelhouse`` folder also next to it, then
just run ``build_wheels.sh``.

Once the "repaired" wheels have been saved, you can extract them from the
docker container using

    

NB: unfortunately one must remove manually all unnecessary files from the
wheels before running the build to prevent them from being included...
