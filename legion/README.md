# Legion-Centric Spack Documentation

The Legion Spack package follows the underlying approach used in Legion's CMake-based build infrastructure.  If you are not familiar with using Spack, we encourage you to start with the **[Spack 101 Tutorial](https://spack-tutorial.readthedocs.io/en/latest/)**.  For more background on Legion please visit the project [website](https://legion.stanford.edu). There you can find information on getting started, tutorials, and supporting documentation.

## Versions

---

We strongly recommend the majority of users start with the latest **stable** branch of Legion.  This will guarantee the most regularly tested and debugged version of the code.  We also strive to have quarterly tagged release throughout the calendar year starting March (e.g., legion-YY.MM.0 where MM starts at *'03'* and runs through *'12'* for any calendar year).  These versioned downloads are captured via the [Legion GitHub page](https://github.com/StanfordLegion/legion) and captured in the Spack package for individual use via the naming convention above.  The details for each release are captured in the CHANGES.txt file at the top-level of the repository.

## Spack Usage and Details

---

Assuming you have a working installation of Spack as outlined in the tutorial the following parameters can be used to download, configure, and build legion.  As of its latest release Legion uses features from C++11 and can be build using either GCC or Clang (and likely any other compilers with full C++11 support).  For example,

    spack install legion %clang@10.0 

will build and install Legion using version 10.0 of the clang compiler.  Additional compiler flags (beyond those automatically enabled by the underlying Legion CMake configuration) may be specified by using the `cppflags` option to Spack: 

    spack install legion %clang@10.0 cppflags=-Wall

You can find more details about customizing the compiler with Spack [here](https://spack-tutorial.readthedocs.io/en/latest/tutorial_basics.html#customizing-compilers).

Finally there are a number of configuration parameters for Legion, known as *variants* in Spack, that can be provided via the command line.  To see a complete listing of these variants you can use the following command: 

    spack info legion

In the output, under the `Variants` section, you will see numerous options with a note on their default setting, allowed values, and a brief summary of what they do.  Here is an example of a portion of the output of the variants supported by the Legion *"spackage"*. 

    Name [Default]                 Allowed values          Description
    ===========================    ====================    =========================================
    bounds_checks [off]            on, off                 Enable bounds checking in Legion accessors.
    build_all [off]                on, off                 Build everything: bindings, examples, etc.
    build_apps [off]               on, off                 Build the sample applicaitons.
    build_bindings [off]           on, off                 Build all the language bindings...
    build_examples [off]           on, off                 Build the (small'ish) examples.
    build_tests [off]              on, off                 Build the test suite.
    build_tutorial [off]           on, off                 Build the Legion tutorial examples.
    build_type [RelWithDebInfo]    Debug, Release,         CMake build type.
                                   RelWithDebInfo,         
                                   MinSizeRel
    ...                                    

These variants may then be used on the Spack command line to customize the build of Legion you would like to install.  For boolean-based variants the `+`, `-`, or `~` *sigils* can be used. In this case, the `+` specifies a `True` value and either `-` or `~` can be used for the `False` setting (two values for `False` are provided to avoid conflicts with shell command line parameters. For example, 

    spack install legion@stable~cuda+hdf5%clang10.0

will build/install the stable version of Legion without CUDA and with HDF5 support; using Clang 10.0 as the compiler.

## Overview of Legion's Spack Variants

---

This section provides an overview of the variants that are available for builds and installations of Legion and the underlying Realm runtime libraries.  These variants range from important configuration parameters for many users, to more involved and low-level details more likely to be leveraged when debugging correctness and performance issues.  For these last set of use cases we encourage users to visit the Legion [Debugging](https://legion.stanford.edu/debugging/) and [Profiling](https://legion.stanford.edu/profiling/) pages.

Note that any variants with a default of `on` or `off` are boolean values and may be configured on the Spack command line using the `+`, or `-` (or `~`) sigils.

Finally, to build the highest performing installation of Legion requires an appropriate configuration and installation of GASNet-Ex (while we have support for an MPI transport layer it is still in testing and evaluation for achieving the best possible performance).  See the following section for details on the steps needed to build a high-performance install of Legion using Spack.

* **`bounds_checks`**:  This variant supports `on` or `off` values and enables, or disables bounds checking within the runtime's data accessors.  This is helpful for debugging but  does have the potential to degrade performance (therefore it is disabled in the default build).  `default=off`

* **`build_all`**:  This variant supports `on` or `off` and specifies that a build/install of Legion should include "*everything*".  This includes all bindings, examples, tutorials, tests, and applications that are included in the project's repository. `default=off`

* **`build_apps`**: This variant supports `on` or `off` and builds the sample applications that are included as part of the source code repository.  `default=off`

* **`build_bindings`**: This variant supports `on` or `off` and builds all language bindings for Legion.  In addition to the required C++ interface, this currently includes C, Python, and Fortran.

* **`build_examples`**: This variant supports `on` or `off` and builds all example applications (generally smaller, in terms of *lines-of-code*, than those specified by `build_apps`).  `default=off`

* **`build_tests`**:  This variant supports `on` or `off` and builds the test/regression suite. `default=off`

* **`build_tutorial`**: This variant supports `on` or `off` and builds the set of examples from the Legion tutorial. `default=off`

* **`build_type`**: This variant exposes the CMake build type setting.  Following directly from CMake these available values for this variant are [`Debug`, `RelWithDebInfo`, and `Release`]. `default=RelWithDebInfo`

* **`cuda`**: This variant supports `on` or `off` and enables CUDA support within Legion.  `default=off`

* **`cuda_arch`**: This variant specifics the specific CUDA architecture to support within the Legion build/installation.  Currently this variant must be one of [`60`, `70`, or `75`].  Where `60` is the Pascal architecture, `70` is the Volta architecture, and `75` is for the Turing architecture.  `default=70`

* **`cuda_hijack`**:  This variant supports `on` or `off` and determines if the build enables performance enhancements by "*hijacking* entry points into CUDA's runtime API; thus, it obviously implies `+cuda`.This is a performance enhancement and not necessary but suggested for production use cases on NVIDIA-based systems.  `default=off` 

* **`enable_tls`**: This variant supports `on` or `off` and enables thread-local-storage of the Legion runtime context.  `default=off`
                                                           context.
* **`fortran`**: This variant supports `on` or `off` and enables building of Fortran language bindings for Legion. `default=off`

* **`hdf5`**: This variant supports `on` or `off` and enables building of HDF5 support within the runtime. `default=off` 

* **`hwloc`**: Build using "libhwloc" support for numa-aware topology support within Realm (Legion's low-level runtime layer).  `default=off`

* **`ipo`**: Enable inter-procedural optimizations. `default=off`

[//]: <> (TOOD: More details here on Kokkos interop?)

* **`kokkos`**: Enable support for interoperability with [Kokkos](https://github.com/kokkos) use in Legion tasks. `default=off`

* **`libdl`**: Enable support for dynamic object loading (via "libdl").  `default=off`

* **`link_llvm_libs`**:  Link the [LLVM](https://llvm.org) libraries into the Realm runtime library. `default=off`

* **`llvm`**: Enable support for [LLVM](https://llvm.org) IR JIT support in the Realm runtime. `default=off`

* **`max_dims`**: This variant provides an integral value for the maximum number of dimensions in a logical region that are supported by the build/install.  `default=3`

* **`max_fileds`**: This variant provides an integral value for the maximum number of fields that may be stored within a logical region.  `default=512`

* **`network`**: This variant specifies what transport layer Legion/Realm should use for moving data across the distributed memories in a machine.  The options are currently: [`gasnetex`, `mpi`, or `none`].  The most tested and reliable interface for distributed memory systems is `gasnetetx` -- however, this will require you to build and configure [GASNet-EX](https://gasnet.lbl.gov) on your particular platform.  The `mpi` layer is more widely available but has not been as thoroughly tested and debugged.  Finally, if you want to run on a single system (e.g., a desktop or laptop) you may specify `none`.  `default=none`

[//]: <> (TOOD: More details here on OpenMP interop?)

* **`openmp`**: This variant enables OpenMP support within Legion tasks (and within the Realm runtime). Please note that the full OpenMP feature set (e.g. OpenMP 5.0) may not be fully supported when enabling this feature.  `default=off`

* **`output_level`**: This variant enables the (dynamic) debugging level for the runtime.  It can be one of the following values: [`spew`, `debug`, `info`, `print`, `warning`, `error`, `fatal`, or `none`].  `default=warning`

[//]: <> (TOOD: More details here? For tasks? The full runtime? Other?)

* **`papi`**: This variant enables PAPI performance measurements.  `default=off`

* **`privilege_checks`**: This variant enables the runtime checking of data privileges in Legion's data accessors. This can helpful in debugging applications. `default=off`

* **`python`**: This variant enables Python support in terms of both bindings and runtime support (where instance(s) of the Python interpreter must be available.) `default=off`

[//]: <> (TOOD: More details here -- not sure about the use case for complex types?)

* **`redop_complex`** This variant enables support for the reduction of complex types. `default=off`

* **`shared_libs`**: Build shared libraries for Legion and Realm. `default=off`

* **`spy`**: This variant enables applications to produce detailed logging information for debugging with Legion [Spy](https://legion.stanford.edu/debugging/#legion-spy).  `default=off`

[//]: <> (TOOD: Need some details as to why someone might want zlib.)

* **`zlib`**: This variant enables support for zlib. `default=off`

## Example Configuration of a High-Performance Legion Variant

---

TODO: Need to finish this section.

## Example Configuration of a Debugging Legion Variant

---

TODO: Need to finish this section.
