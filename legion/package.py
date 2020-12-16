# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class Legion(CMakePackage):
    """Legion is a data-centric parallel programming system for writing
       portable high performance programs targeted at distributed heterogeneous
       architectures. Legion presents abstractions which allow programmers to
       describe properties of program data (e.g. independence, locality). By
       making the Legion programming system aware of the structure of program
       data, it can automate many of the tedious tasks programmers currently
       face, including correctly extracting task- and data-level parallelism
       and moving data around complex memory hierarchies. A novel mapping
       interface provides explicit programmer controlled placement of data in
       the memory hierarchy and assignment of tasks to processors in a way
       that is orthogonal to correctness, thereby enabling easy porting and
       tuning of Legion applications to new architectures.
    """
    homepage = "http://legion.stanford.edu/"
    url      = "https://github.com/StanfordLegion/legion/tarball/legion-20.09.0"
    git      = "https://github.com/StanfordLegion/legion.git"

    version('master', branch='master')
    version('stable',  branch='stable')
    version('20.12.0', tag='legion-20.12.0')
    version('20.09.0', tag='legion-20.09.0')
    version('20.06.0', tag='legion-20.06.0')
    version('20.03.0', tag='legion-20.03.0')
    version('19.12.0', tag='legion-19.12.0')
    version('19.09.1', tag='legion-19.09.1')
    version('19.09.0', tag='legion-19.09.0')
    version('19.06.0', tag='legion-19.06.0')
    version('19.04.0', tag='legion-19.04.0')
    version('18.12.0', tag='legion-18.12.0')
    version('18.09.0', tag='legion-18.09.0')
    version('18.02.0', tag='legion-18.02.0')
    version('ctrl-rep', branch='control_replication')

    variant('shared_libs', default=False,
            description="Build shared libraries.")

    variant('network', default='none', 
            values=("gasnetex", "mpi", "none"), 
            description="The network communications layer to use.", 
            multi=False)

    variant('bounds_checks', default=False,
            description="Enable bounds checking in Legion accessors.")
    variant('privilege_checks', default=False,
            description="Enable runtime privildge checks in Legion accessors.")
    variant('enable_tls', default=False,
            description="Enable thread-local-storage of the Legion context.")
    variant('output_level', default='warning',
            # Note: values are dependent upon Legion's cmake parameters...
            values=("spew", "debug", "info", "print", "warning", "error", "fatal", "none"),
            description="Set the compile-time logging level.", 
            multi=False)
    variant('spy', default=False, 
            description="Enable detailed logging for Legion Spy debugging.")

    variant('cuda', default=False, 
            description="Enable CUDA support.")
    variant('cuda_hijack', default=False,
            description="Hijack application calls into the CUDA runtime (implies +cuda).")
    # note on arch values: 60=pascal, 70=volta, 75=turing
    cuda_arch_list = ("60", "70", "75")
    variant('cuda_arch', default='70', # default to supporting volta
            values=cuda_arch_list,
            description="GPU/CUDA architecture to build for.",
            multi=True)
    variant('fortran', default=False, 
            description="Enable Fortran bindings.")
    variant('hdf5', default=False,
            description="Enable support for HDF5.")
    variant('hwloc', default=False,
            description="Use hwloc for topology awareness.")
    variant('kokkos', default=False,
            description="Enable support for interoperability with Kokkos.")
    variant('libdl', default=True, 
            description="Enable support for dynamic loading (via libdl).")
    variant('llvm', default=False,
            description="Enable support for LLVM IR JIT  within the Realm runtime.")
    variant('link_llvm_libs', default=False,
            description="Link LLVM libraries into the Realm runtime library.")
    variant('openmp', default=False,
            description="Enable support for OpenMP within Legion tasks.")
    variant('papi', default=False, 
            description="Enable PAPI performance measurements.")
    variant('python', default=False, 
            description="Enable Python support.")
    variant('zlib', default=True, 
            description="Enable zlib support.")

    variant('redop_complex', default=False,
            description="Use reduction operators for complex types.")
    

    variant('build_all', default=False,
            description="Build everything: all bindings, examples, tutorials, tests, apps, etc.")
    variant('build_apps', default=False,
            description="Build the sample applicaitons.")
    variant('build_bindings', default=False,
            description="Build all the language bindings (C, Fortran, Python, etc.).")
    variant('build_examples', default=False,
            description="Build the (small'ish) examples.")
    variant('build_tests', default=False,
            description="Build the test suite.")
    variant('build_tutorial', default=False,
            description="Build the Legion tutorial examples.")
    


    variant('max_dims', values=int, default=3,
            description="Set the maximum number of dimensions available in a logical region.")
    variant('max_fields', values=int, default=512,
            description="Maximum number of fields allowed in a logical region.")

    conflicts('+cuda_hijack', when='~cuda')

    depends_on("cmake@3.1:", type='build')
    depends_on('mpi', when='network=mpi')
    depends_on('gasnetex', when='network=gasnetex')
    depends_on('hdf5', when='+hdf5')
    depends_on('llvm@7.1.0', when='+llvm')
    depends_on('llvm@7.1.0', when='+link_llvm_libs')
    depends_on('cuda@10:', when='+cuda')
    depends_on('hdf5', when='+hdf5')
    depends_on('zlib@1.2.11', when="zlib")
    depends_on('kokkos@3.1:', when='+kokkos')
    depends_on('kokkos-nvcc-wrapper~mpi', when='%gcc+kokkos+cuda')
    depends_on('kokkos+wrapper', when='%gcc+kokkos+cuda')
    for ca in cuda_arch_list:
        depends_on(
            'kokkos+cuda cuda_arch=%s' % ca,
            when='+kokkos+cuda cuda-arch=%s' % ca)


    def cmake_args(self):
        cmake_cxx_flags = [ ]
        options = [ ]
        if '+shared_libs' in self.spec:
            options.append('-DBUILD_SHARED_LIBS=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')

        if '+bounds_checks' in self.spec:
            # default is off. 
            options.append('-DLegion_BOUNDS_CHECKS=ON')
        if '+privilege_checks' in self.spec:
            # default is off. 
            options.append('-DLegion_PRIVILEGE_CHECKS=ON')
        if '+enable_tls' in self.spec:
            # default is off.
            options.append('-DLegion_ENABLE_TLS=ON')
        if 'output_level' in self.spec:
            level = str.upper(self.spec.variants['output_level'].value)
            options.append('-DLegion_OUTPUT_LEVEL=%s' % level)
        if '+spy' in self.spec:
            # default is off. 
            options.append('-DLegion_SPY=ON')
  
        if 'network=gasnet' in self.spec:
            options.append('-DLegion_NETWORKS=gasnet1')
        elif 'network=mpi' in self.spec: 
            options.append('-DLegion_NETWORKS=mpi')
        # else is no-op... 
        
        if '+cuda' in self.spec:
            cuda_arch = list(self.spec.variants['cuda_arch'].value)
            arch_str = ','.join(cuda_arch)
            options.append('-DLegion_USE_CUDA=ON')
            options.append('-DLegion_GPU_REDUCTIONS=ON')
            options.append('-DLegion_CUDA_ARCH=%s' % arch_str)
            if '+cuda_hijack' in self.spec:
                options.append('-DLegion_HIJACK_CUDART=ON')
            else:
                options.append('-DLegion_HIJACK_CUDART=OFF')
        
        if '+fortran' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_Fortran=ON')

        if '+hdf5' in self.spec:
            # default is off.
            options.append('-DLegion_USE_HDF5=ON')

        if '+hwloc' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_HWLOC=ON')

        if '+kokkos' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_Kokkos=ON')
            os.environ['KOKKOS_CXX_COMPILER'] = self.spec['kokkos'].kokkos_cxx

        if '+libdl' in self.spec:
            # default is on.
            options.append('-DLegion_USE_LIBDL=ON')
        else:
            options.append('-DLegion_USE_LIBDL=OFF')
        
        if '+llvm' in self.spec:
            # default is off.
            options.append('-DLegion_USE_LLVM=ON')
        if '+link_llvm_libs' in self.spec:
            options.append('-DLegion_LINK_LLVM_LIBS=ON')
            # TODO: What do we want to do w/ this option?
            options.append('-DLegion_ALLOW_MISSING_LLVM_LIBS=OFF')

        if '+openmp' in self.spec:
            # default is off.
            options.append('-DLegion_USE_OpenMP=ON')

        if '+papi' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_PAPI=ON')

        if '+python' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_Python=ON')

        if '+zlib' in self.spec:
            # default is on. 
            options.append('-DLegion_USE_ZLIB=ON')
        else:
            options.append('-DLegion_USE_ZLIB=OFF')


        if '+redop_complex' in self.spec:
            # default is off.
            options.append('-DLegion_REDOP_COMPLEX=ON')


        if '+build_all' in self.spec:
            # default is off. 
            options.append('-DLegion_BUILD_ALL=ON')
        if '+build_apps' in self.spec:
            # default is off.
            options.append('-DLegion_BUILD_APPS=ON')
        if '+build_bindings' in self.spec:
            # default is off.
            options.append('-DLegion_BUILD_BINDINGS=ON')
        if '+build_examples' in self.spec:
            options.append('-DLegion_BUILD_EXAMPLES=ON')
        if '+build_tests' in self.spec:
            options.append('-DLegion_BUILD_TESTS=ON')
        if '+build_tutorial' in self.spec:
            options.append('-DLegion_BUILD_TUTORIAL=ON')

        if self.spec.variants['build_type'].value == 'Debug':
            cmake_cxx_flags.extend([
                '-DDEBUG_REALM',
                '-DDEBUG_LEGION',
                '-ggdb',
            ])


        maxdim = self.spec.variants['max_dims'].value
        options.append('-DLegion_MAX_DIM=%s' % maxdim)

        maxfields = self.spec.variants['max_fields'].value
        options.append('-DLegion_MAX_FIELDS=%s' % maxfields)

        # currently failing on zen2 architectures... investigating...  
        #options.append('-DBUILD_MARCH:STRING=%s' % self.spec.architecture.target)

        options.append('-DCMAKE_CXX_FLAGS=%s' % (" ".join(cmake_cxx_flags)))

        return options
