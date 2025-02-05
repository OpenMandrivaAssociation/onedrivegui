%define sname	OneDriveGUI

Summary:	A simple GUI for OneDrive Linux client, with multi-account support
Name:		onedrivegui
Version:	1.1.1a
Release:	1
Group:		Graphical desktop/KDE
License:	GPLv3
URL:		https://github.com/bpozdena/OneDriveGUI
Source0:	https://github.com/bpozdena/OneDriveGUI/archive/v%{version}/%{name}-v%{version}.tar.gz
BuildRequires:	imagemagick

BuildArch:	noarch
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{py_ver}dist(pip)
#BuildRequires:	python%{py_ver}dist(pyside6)
#BuildRequires:	python%{py_ver}dist(requests)
#BuildRequires:	python%{py_ver}dist(setuptools)
#BuildRequires:	python%{py_ver}dist(wheel)

Requires:	onedrive
Requires:	pyside6-devel
Requires:	shiboken6
Requires:	python%{py_ver}dist(requests)
#Requires:	python%{py_ver}dist(shiboken6)

%description
A simple GUI for OneDrive Linux client, with multi-account support.

Feature highlights:
  * Management and configuration of multiple OneDrive accounts
  * Asynchronous real-time monitoring of multiple OneDrive accounts
  * Setup wizard for easy OneDrive profile creation and import
  * Auto-sync on GUI startup
  * Support for GUI based login process
  * System tray (if supported by your desktop environment)
  * Start minimized to tray/dock
  * Input validation to prevent configuration of incompatible OneDrive
	client options
  * Import and management of Business Shared Folders
  * Import and management of SharePoint Shared Libraries
  * ToolTips with brief explanation of various OneDrive Client
	configuration options.
  * Prompt for re-sync authorization to prevent unexpected data loss.


%files
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/%{sname}/
%{_datadir}/applications/*%{sname}.desktop
%{_datadir}/pixmaps/*%{name}*
%{_iconsdir}/hicolor/*/apps/*.png
#{python_sitelib}/%{sname}-%{version}*-info
#{python_sitelib}/%{sname}/

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n  %{sname}-%{version}

%build
#py_build

%install
#py_install

# libs
install -dpm 0755 %{buildroot}%{_libdir}/%{sname}
install -Dm 0755 src/%{sname}.py %{buildroot}%{_libdir}/%{sname}/%{sname}.py
cp -ra src/{resources,ui} %{buildroot}%{_libdir}/%{sname}/

# resources
#install -dpm 0755 %{buildroot}%{_libdir}/%{sname}/resources
#install -D src/resources/* %{buildroot}%{_libdir}/%{sname}/resources
#echo foo
# ui
#install -dpm 0755 %{buildroot}%{_libdir}/%{sname}/ui
#install -Dm 0644 src/ui/* %{buildroot}%{_libdir}/%{sname}
#echo bar

# binary
install -dpm 0755 %{buildroot}%{_bindir}
ln -fs %{_libdir}/%{sname}/%{sname}.py %{buildroot}%{_bindir}/%{name}

# icons
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps
	convert src/resources/images/%{sname}.png -scale ${d}x${d} \
		%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -background none src/resources/images/%{sname}.png \
	-scale 32x32 %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# .desktop
desktop-file-install \
	--vendor="%{vendor}" \
	--set-key="Exec" \
	--set-value="%{name}" \
	--set-key="Icon" \
	--set-value="%{name}" \
	--remove-key="Path" \
	--add-category="Network" \
	--dir %{buildroot}%{_datadir}/applications \
	src/resources/%{sname}.desktop

