bolo builds
===========

This repository contains the recipes for building Redhat (RPM) and
Debian/Ubuntu (DEB) packages for bolo, the collectors, and their
build- and run-time dependencies.

These packages are hosted [on the public Internet][pkg], in YUM
and APT repositories, so that everyday RPM- and DEB-based systems
can easily incorporate them into their package lineup.


Configuring The Repos
---------------------

To use the Niftylogic [pkg][pkg] repositories, follow the
instructions at [http://pkg.niftylogic.com][pkg].


Building Packages
-----------------

**NOTE**: This section is probably only of interest to people
maintaining the package repositories over at
[pkg.niftylogic.com][pkg].

To build all of the package, in phases, run

    ./build all

From the top of the repository.  This will run through any number
of _phases_, asking you to stop, sync package files up to the
repositories, and then press `Enter` to continue.  Each phase
builds on the packages in the previous phase.  Packages will be
built for all supported platforms.

To build a subset of packages, provide their names as arguments to
the build script:

    ./build libhiredis rrdtool

To constrain such builds to a subset of available platforms:

    ./build libhiredis rrdtool precise centos6

The keywords `centos` and `ubuntu` are aliases for their
respective platforms (all supported versions).

Compiled packages will be placed in `pub/` in the top-level of the
working directory, and you can use the `push` script to rsync them
somewhere else, i.e.:

    ./push user@host:/tmp/pub

(`/tmp/pub` is as good a place as any to put these files.)


Cleanup
-------

It's probably a good idea to run cleanup routines once in a while:

    ./build clean

You can actually integrate this with other `build` calls:

    ./build clean all


Anatomy of a Build
------------------

Each build lives in a top-level directory, like `libzmq` or
`bolo-collectors`.  It is best practices for these builds to:

1. Build from a release tarball (not origin/master!)
2. Provide packaging artifacts from the build directory
3. Install all dependencies prior to packaging (in Docker)

Each build directory then should contain an `rpm.spec` file for
building RPM packages, and a `debian` directory for building DEB
packages.

Additionally, each build **must** contain a `pkg` script, since
this is the hook that the Docker [rpmbuild/\*][rpmbuild] and
[debuild/\*][debuild] images key off of.  It is usually best to
just copy another builds files and modify to your liking.


Supported Platforms
-------------------

We currently support the following platforms:

- Ubuntu Precise (12.04 LTS)
- Ubuntu Trusty (14.04 LTS)
- Ubuntu Vivid (15.04)
- CentOS 5 (EL 5)
- CentOS 6 (EL 6)
- CentOS 7 (EL 7)

Support derives from the existence of an [rpmbuild/\*][rpmbuild] or
[debuild/\*][debuild] Docker image for running builds in.




[pkg]:      http://pkg.niftylogic.com
[rpmbuild]: https://dockerhub.com/u/rpmbuild
[debuild]:  https://dockerhub.com/u/debuild
