%define		distro pld
%define		polyinstatiate n
%define		POLICYVER 20
Summary:	SELinux policy configuration
Summary(pl.UTF-8):	Konfiguracja polityki SELinuksa
Name:		refpolicy
Version:	20070629
Release:	0.2
License:	GPL
Group:		Base
Source0:	http://oss.tresys.com/files/refpolicy/%{name}-%{version}.tar.bz2
# Source0-md5:	8762233602b1e660636373102e6f6db4
Source1:	%{name}-modules-targeted.conf
Source2:	%{name}-booleans-targeted.conf
Source3:	%{name}-setrans-targeted.conf
Source4:	%{name}-modules-mls.conf
Source5:	%{name}-booleans-mls.conf
Source6:	%{name}-setrans-mls.conf
Source7:	%{name}-modules-strict.conf
Source8:	%{name}-booleans-strict.conf
Source9:	%{name}-setrans-strict.conf
Source10:	%{name}-config
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-pld.patch
URL:		http://oss.tresys.com/projects/refpolicy/
BuildRequires:	checkpolicy >= 1.33.1
BuildRequires:	gawk
BuildRequires:	m4
BuildRequires:	policycoreutils >= 1.30
BuildRequires:	rpm-pythonprov
Requires:	policycoreutils >= 1.30
Obsoletes:	policy
Obsoletes:	selinux-policy-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_seconfdir %{_sysconfdir}/selinux

%description
SELinux Reference Policy - modular.

%description -l pl.UTF-8
Wzorcowa polityka SELinuksa - modularna.

%package mls
Summary:	SELinux mls base policy
Summary(pl.UTF-8):	Podstawowa polityka mls SELinuksa
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	coreutils
Requires:	policycoreutils >= 1.30
Provides:	selinux-policy-base
Obsoletes:	selinux-policy-mls-sources

%description mls
SELinux Reference policy mls base module.

%description mls -l pl.UTF-8
Podstawowy moduł mls wzorcowej polityki SELinuksa.

%package strict
Summary:	SELinux strict base policy
Summary(pl.UTF-8):	Podstawowa surowa polityka SELinuksa
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	coreutils
Requires:	policycoreutils >= 1.30
Provides:	selinux-policy-base
Obsoletes:	selinux-policy-strict-sources

%description strict
SELinux Reference policy strict base module.

%description strict -l pl.UTF-8
Podstawowy moduł surowej (strict) wzorcowej polityki SELinuksa.

%package targeted
Summary:	SELinux targeted base policy
Summary(pl.UTF-8):	Postawowa polityka SELinuksa targeted
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	coreutils
Requires:	policycoreutils >= 1.30
Provides:	selinux-policy-base
Obsoletes:	selinux-policy-targeted-sources

%description targeted
SELinux Reference policy targeted base module.

%description targeted -l pl.UTF-8
Podstawowy moduł wzorzowej polityki SELinuksa targeted.

%define ARGS NAME=\%1 TYPE=\%2 DISTRO=%{distro} DIRECT_INITRC=\%3 MONOLITHIC=n POLY=\%3

%define installCmds() \
%{__make} %ARGS bare \
%{__make} %ARGS conf \
cp -f ${RPM_SOURCE_DIR}/%{name}-modules-%1.conf  ./policy/modules.conf \
cp -f ${RPM_SOURCE_DIR}/%{name}-booleans-%1.conf ./policy/booleans.conf \
%{__make} %ARGS base.pp \
%{__make} %ARGS modules \
%{__make} %ARGS DESTDIR=$RPM_BUILD_ROOT install install-appconfig \
%{__make} %ARGS DESTDIR=$RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_seconfdir}/%1/users/{local,system}.users \
%{__cp} *.pp $RPM_BUILD_ROOT/%{_usr}/share/selinux/%1/ \
%{__make} %ARGS enableaudit \
%{__make} %ARGS -W base.conf base.pp \
install base.pp $RPM_BUILD_ROOT%{_usr}/share/selinux/%1/enableaudit.pp \
rm -rf $RPM_BUILD_ROOT%{_seconfdir}/%1/booleans \
install ${RPM_SOURCE_DIR}/%{name}-setrans-%1.conf $RPM_BUILD_ROOT%{_seconfdir}/%1/setrans.conf \
ln -sf ../devel/include $RPM_BUILD_ROOT%{_usr}/share/selinux/%1/include \
%{nil}

%define fileList() \
%defattr(644,root,root,755) \
%dir %{_seconfdir}/%1 \
%dir %{_seconfdir}/%1/contexts \
%config(noreplace) %verify(not md5 mtime size) %{_seconfdir}/%1/contexts/*_context* \
%config(noreplace) %verify(not md5 mtime size) %{_seconfdir}/%1/contexts/*_type* \
%dir %{_seconfdir}/%1/contexts/files \
%ghost %{_seconfdir}/%1/contexts/files/file_contexts \
%ghost %{_seconfdir}/%1/contexts/files/homedir_template \
%ghost %{_seconfdir}/%1/contexts/files/file_contexts.homedirs \
%config(noreplace) %verify(not md5 mtime size) %{_seconfdir}/%1/contexts/files/media \
%config(noreplace) %verify(not md5 mtime size) %{_seconfdir}/%1/setrans.conf \
%ghost %{_seconfdir}/%1/seusers \
%dir %{_seconfdir}/%1/modules \
%{_seconfdir}/%1/modules/semanage.read.LOCK \
%{_seconfdir}/%1/modules/semanage.trans.LOCK \
%attr(700,root,root) %dir %{_seconfdir}/%1/modules/active \
#%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_seconfdir}/%1/modules/active/seusers \
%dir %{_seconfdir}/%1/policy/ \
%ghost %{_seconfdir}/%1/policy/policy.* \
%{_usr}/share/selinux/%1 \
%dir %{_seconfdir}/%1/users \
%config(noreplace) %verify(not md5 mtime size) %{_seconfdir}/%1/users/*.users \

%define rebuildpolicy() \
( cd /usr/share/selinux/%1; \
x=`ls *.pp | grep -v -e base.pp -e enableaudit.pp | awk '{ print "-i " $1 }'`; \
semodule -b base.pp $x -s %1; \
);\

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install man/man8/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -D %{SOURCE10} $RPM_BUILD_ROOT%{_seconfdir}/config

for pol in mls targeted strict; do
install -d $RPM_BUILD_ROOT%{_seconfdir}/$pol/{policy,modules/active,contexts/files}
#install -d $RPM_BUILD_ROOT%{_seconfdir}/$pol/modules/active
#install -d $RPM_BUILD_ROOT%{_seconfdir}/$pol/contexts/files
#install -D config/local.users $RPM_BUILD_ROOT%{_seconfdir}/$pol/users/local.users
touch $RPM_BUILD_ROOT%{_seconfdir}/$pol/modules/semanage.read.LOCK
touch $RPM_BUILD_ROOT%{_seconfdir}/$pol/modules/semanage.trans.LOCK
touch $RPM_BUILD_ROOT%{_seconfdir}/$pol/seusers
touch $RPM_BUILD_ROOT%{_seconfdir}/$pol/policy/policy.%{POLICYVER}
touch $RPM_BUILD_ROOT%{_seconfdir}/$pol/contexts/files/file_contexts
touch $RPM_BUILD_ROOT%{_seconfdir}/$pol/contexts/files/homedir_template
touch $RPM_BUILD_ROOT%{_seconfdir}/$pol/contexts/files/file_contexts.homedirs
done

%{__make} NAME=devel TYPE=targeted DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} DESTDIR=$RPM_BUILD_ROOT PKGNAME=%{name}-%{version} POLY=n install-headers install-docs
rm -f $RPM_BUILD_ROOT%{_usr}/share/selinux/devel/include/include

%installCmds targeted targeted y  n
%installCmds strict strict y n
%installCmds mls strict-mls n y

%clean
rm -rf $RPM_BUILD_ROOT

%post mls
%rebuildpolicy mls

%post strict
%rebuildpolicy strict

%post targeted
%rebuildpolicy targeted

%files
%defattr(644,root,root,755)
%{_mandir}/man8/*
#%%doc %{_usr}/share/doc/%{name}-%{version}
%doc doc/example.*
%dir %{_seconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_seconfdir}/config
%dir %{_usr}/share/selinux
%dir %{_usr}/share/selinux/devel
%{_usr}/share/selinux/devel/include

%files mls
%fileList mls

%files strict
%fileList strict

%files targeted
%fileList targeted
