# Created by pyp2rpm-3.3.2
%global pypi_name Yapps2

Name:           python-%{pypi_name}
Version:        2.2.0
Release:        1%{?dist}
Summary:        Yet Another Python Parser System

License:        MIT
URL:            https://github.com/mk-fg/yapps
Source0:        https://files.pythonhosted.org/packages/source/y/%{pypi_name}/Yapps2-%{version}.tar.gz
BuildArch:      noarch

    
%global _description\
Yapps (Yet Another Python Parser System) is an easy to use parser generator \
that is written in Python and generates Python code. \
Yapps is simple, is easy to use, and produces human-readable parsers. \
It is not the fastest, most powerful, or most flexible parser. \
Yapps is designed to be used when regular expressions are not enough and \
other parser systems are too much: situations where you may write your own \
recursive descent parser. \
Yapps 2 is more like an imperative language (more verbose grammars of the \
form if/while you see this, do this).


%description %{_description}


%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
BuildRequires:  python2-devel
BuildRequires:  python2dist(setuptools)
 
Requires:       python2dist(setuptools)
%description -n python2-%{pypi_name} %{_description}

This package provides the Python 2 version.


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
 
Requires:       python3dist(setuptools)
%description -n python3-%{pypi_name} %{_description}

This package provides the Python 3 version.


%prep
%autosetup -n Yapps2-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install


%files -n python2-%{pypi_name}
%{python2_sitelib}/yapps
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info


%files -n python3-%{pypi_name}
%{_bindir}/yapps2
%{python3_sitelib}/yapps
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info


%changelog
* Mon Apr 13 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.2.0-1
- Initial package.
