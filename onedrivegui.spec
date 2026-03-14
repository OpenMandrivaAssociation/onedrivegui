%define sname	OneDriveGUI

Summary:	A simple GUI for OneDrive Linux client, with multi-account support
Name:	onedrivegui
Version:	1.3.0
Release:	1
License:	GPLv3
Group:	Graphical desktop/KDE
Url:		https://github.com/bpozdena/OneDriveGUI
Source0:	https://github.com/bpozdena/OneDriveGUI/archive/v%{version}/%{sname}-%{version}.tar.gz
Patch0:	onedrivegui-1.2.1-fix-python-shebang.patch
Patch1:	onedrivegui-1.3.0-refactor-logging-levels.patch
Patch2:	onedrivegui-1.3.0-update-tray-and-tooltip-only-if-needed.patch
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{py_ver}dist(pip)
BuildRequires:	python%{py_ver}dist(pyside6)
BuildRequires:	python%{py_ver}dist(requests)
BuildRequires:	python%{py_ver}dist(urllib3)
BuildArch:	noarch
Requires:	onedrive
Requires:	pyside6
Requires:	shiboken6
Requires:	python%{py_ver}dist(requests)
Requires:	python%{py_ver}dist(urllib3)

%description
A simple GUI for OneDrive Linux client, with multi-account support.
Feature highlights:
* Management and configuration of multiple OneDrive accounts.
* Asynchronous real-time monitoring of multiple OneDrive accounts.
* Setup wizard for easy OneDrive profile creation and import.
* Auto-sync on GUI startup.
* Support for GUI based login process.
* System tray (if supported by your desktop environment).
* Start minimized to tray/dock.
* Input validation to prevent configuration of incompatible OneDrive client
	options.
* Import and management of Business Shared Folders.
* Import and management of SharePoint Shared Libraries.
* ToolTips with brief explanation of various OneDrive Client configuration
	options.
* Prompt for re-sync authorization to prevent unexpected data loss.

%files
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/%{sname}/
%{_datadir}/applications/*%{sname}.desktop
%{_datadir}/pixmaps/*%{name}*
%{_iconsdir}/hicolor/*/apps/*.png
#{python_sitelib}/%%{sname}-%%{version}*-info
#{python_sitelib}/%%{sname}/

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n  %{sname}-%{version}


%build
# No setuptools support: nothing to do


%install
# No setuptools support: install manually
# Install main script and resources
install -dpm 0755 %{buildroot}%{_libdir}/%{sname}
install -Dm 0755 src/%{sname}.py %{buildroot}%{_libdir}/%{sname}/%{sname}.py
cp -ra src/{resources,ui} %{buildroot}%{_libdir}/%{sname}/

# Install "binary"
install -dpm 0755 %{buildroot}%{_bindir}
ln -fs %{_libdir}/%{sname}/%{sname}.py %{buildroot}%{_bindir}/%{name}

# Install more icons
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps
	magick src/resources/images/%{sname}.png -scale ${d}x${d} \
		%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
magick -background none src/resources/images/%{sname}.png \
	-scale 32x32 %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# Fix and install .desktop file from sources
desktop-file-install \
	--set-key="Exec" --set-value="%{name}" \
	--set-key="Icon" --set-value="%{name}" \
	--remove-key="Path" \
	--add-category="Network" \
	--dir %{buildroot}%{_datadir}/applications \
	src/resources/%{sname}.desktop
