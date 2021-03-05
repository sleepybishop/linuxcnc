%global srcname Yapps

Name:           python-%{srcname}
Version:        2.2.0
Release:        1%{?dist}
Summary:        Yet Another Python Parser System

License:        MIT
URL:            https://github.com/smurfix/yapps
Source0:        %{pypi_source}
Patch0:         70a146b66de396c0d2c6bb6979d2cf58a79f4d7b.patch

BuildArch:      noarch

%global _description \
YAPPS is an easy to use parser generator that is written in Python and\
generates Python code. There are several parser generator systems already\
available for Python, but this parser has different goals: Yapps is simple,\
very easy to use, and produces human-readable parsers.

%description %{_description}

%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel python2-setuptools

%description -n python2-%{srcname} %{_description}
Python 2 version.

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel python3-setuptools
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}
Python 3 version.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
%{__python3} setup.py test

# Note that there is no %%files section for the unversioned python module
%files -n python2-%{srcname}
%{python2_sitelib}/%{srcname}-*.egg-info/
%{python2_sitelib}/yapps/
%{_bindir}/yapps2

%files -n python3-%{srcname}
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/yapps/
%{_bindir}/yapps2

