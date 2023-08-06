%define python python
%define __python /usr/bin/python
%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           cubicweb-file
Version:        2.2.1
Release:        logilab.1%{?dist}
Summary:        file component for the CubicWeb framework
Group:          Applications/Internet
License:        LGPL
Source0:        cubicweb-file-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  %{python} %{python}-setuptools
Requires:       cubicweb >= 3.24.0
Requires:       python-imaging

%description
file component for the CubicWeb framework

%prep
%setup -q -n cubicweb-file-%{version}

%install
%{__python} setup.py --quiet install --no-compile --prefix=%{_prefix} --root="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_python_sitelib}/*

