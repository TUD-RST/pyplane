%bcond_without tests

%global _description %{expand:
PyPlane is a free software for phase plane analysis of second order dynamical
systems written in PYTHON and PyQT5. Comparable to MATLAB's pplane.}

%global forgeurl https://github.com/TUD-RST/pyplane

Name:           pyplane
Version:        2.0.0
Summary:        Phase plane analysis of nonlinear systems

%global  tag PyPlane_v%{version}
%forgemeta

Release:        %autorelease
License:        GPLv3
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        pyplane.metainfo.xml

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  libappstream-glib
%if %{with tests}
BuildRequires:  %{py3_dist pytest}
# bits not mentioned in install_requires
BuildRequires:  texlive-latex
BuildRequires:  texlive-dvipng
%endif

# Optional but readme says they improve the graphs etc., so add them as weak
# dependencies
Recommends:     texlive-latex
Recommends:     texlive-dvipng

# Add virtual provides to help users find it
Provides:       python3-pyplane

%description %_description

%prep
%forgesetup

%generate_buildrequires
# the install requirements seem to be required for tests, so include them
%pyproject_buildrequires %{?with_tests:-r}

# correct import in test script
sed -i -e '/sys.path.append/ d' -e 's/import core./import pyplane.core./' tests/test_core.py

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pyplane

%check
%if %{with tests}
%{pytest}
%endif

appstream-util validate-relax --nonet %{buildroot}/pyplane.metainfo.xml

%files -f %{pyproject_files}
%doc README.md AUTHORS
%{_bindir}/pyplane

%changelog
%autochangelog
