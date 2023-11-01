# build compat-libmpc for bootstrapping purposes
%global bootstrap 1
%global bootstrap_version 0.9

Summary: C library for multiple precision complex arithmetic
Name: libmpc
Version: 1.1.0
Release: 9.1%{?dist}
License: LGPLv3+
URL: http://www.multiprecision.org/mpc/
Source0: https://ftp.gnu.org/gnu/mpc/mpc-%{version}.tar.gz
%if 0%{?bootstrap}
Source1: http://www.multiprecision.org/downloads/mpc-%{bootstrap_version}.tar.gz
%endif

BuildRequires: gcc
BuildRequires: gmp-devel >= 5.0.0
BuildRequires: mpfr-devel

Patch0: libmpc-fix-uninit-var.patch

%description

MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%package devel
Summary: Headers and shared development libraries for MPC
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gmp-devel%{?_isa}
Requires: mpfr-devel%{?_isa}

%description devel
Header files and shared library symlinks for the MPC library.

%package doc
Summary: Documentation for the MPC library
License: GFDL
BuildArch: noarch

%description doc
Documentation for the MPC library.

%if 0%{?bootstrap}
%package -n compat-libmpc
Summary: compat/bootstrap mpc-%{bootstrap_version} library

%description -n compat-libmpc
Contains the .so files for mpc version %{bootstrap-version}.
%endif

%prep
%setup -q -n mpc-%{version}
%if 0%{?bootstrap}
%setup -q -n mpc-%{version} -a 1
%endif
%patch0 -p1 -b .uninit~

%build
%configure --disable-static

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build

%if 0%{?bootstrap}
export CPPFLAGS="%{optflags} -std=gnu99"
export CFLAGS="%{optflags} -std=gnu99"
export EGREP=egrep

pushd mpc-%{bootstrap_version}
%configure --disable-static
%make_build
popd
%endif

%install
%if 0%{?bootstrap}
%make_install -C mpc-%{bootstrap_version}

## remove everything but shlib
rm -fv %{buildroot}%{_libdir}/libmpc.so
rm -fv %{buildroot}%{_includedir}/*
rm -fv %{buildroot}%{_infodir}/*
%endif

%make_install
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_infodir}/dir

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
make check

%files
%license COPYING.LESSER
%doc README NEWS
%{_libdir}/libmpc.so.3*

%files devel
%{_libdir}/libmpc.so
%{_includedir}/mpc.h

%files doc
%doc AUTHORS
%{_infodir}/*.info*

%if 0%{?bootstrap}
%files -n compat-libmpc
%{_libdir}/libmpc.so.2*
%endif

%changelog
* Fri Oct 09 2020 Marek Polacek <polacek@redhat.com> - 1.1.0-9.1
- apply my upstream patch to fix using an uninitialized value

* Thu Oct 08 2020 Marek Polacek <polacek@redhat.com> - 1.1.0-9
- mpc-1.1.0 (#1835193)
- update the specfile from Fedora

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.0.2-6
- Add missing %%license macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.2-1
- mpc-1.0.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.0.1-1
- compat-libmpc (for bootsrapping purposes)
- mpc-1.0.1
- update Source URLs
- fix License: tag

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.0-2
- %%files: track lib soname (so bumps aren't a surprise)
- tighten subpkg deps (%%_isa)
- %%build: --disable-static

* Thu Aug  2 2012 Petr Machata <pmachata@redhat.com> - 1.0-1
- Upstream 1.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9-1.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9-1.1
- rebuild with new gmp

* Wed Jun 22 2011  <pmachata@redhat.com> - 0.9-1
- Upstream 0.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-0.3.svn855
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 30 2010 Petr Machata <pmachata@redhat.com> - 0.8.3-0.2.svn855
- Bump for rebuild against the new mpfr

* Fri Nov 19 2010 Petr Machata <pmachata@redhat.com> - 0.8.3-0.1.svn855
- Devel updates (to-be-0.8.3, SVN release 855)
  - New functions mpc_set_dc, mpc_set_ldc, mpc_get_dc, mpc_get_ldc
  - Speed-up mpc_pow_si and mpc_pow_z
  - Bug fixes in trigonometric functions, exp, sqrt
- Upstream 0.8.2
  - Speed-up mpc_pow_ui
- Adjust BuildRequires
- Resolves: #653931

* Wed Jan 20 2010 Petr Machata <pmachata@redhat.com> - 0.8.1-1
- Upstream 0.8.1
  - acosh, asinh, atanh: swap of precisions between real and imaginary parts
  - atan: memory leak
  - log: wrong ternary value in data file; masked by bug in Mpfr 2.4.1
- Resolves: #555471 FTBFS libmpc-0.8-3.fc13

* Fri Nov 13 2009 Petr Machata <pmachata@redhat.com> - 0.8-3
- Require mpfr-devel, gmp-devel in -devel subpackage
- Don't pass --entry to install-info

* Thu Nov 12 2009 Petr Machata <pmachata@redhat.com> - 0.8-2
- Rename the package to libmpc, it's a better choice of name
- %%preun should uninstall mpc's info page, not make's
- Move info page to -devel
- BR on -devel packages
- Drop postscript documentation

* Thu Nov 12 2009 Petr Machata <pmachata@redhat.com> - 0.8-1
- Initial package.
