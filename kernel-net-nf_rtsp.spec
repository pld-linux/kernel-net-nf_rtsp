#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%define		rel	0.1
Summary:	RTSP conntrack module
Name:		kernel%{_alt_kernel}-net-nf_rtsp
Version:	2.6.36
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://mike.it-loops.com/rtsp/rtsp-module-%{version}.tar.gz
# Source0-md5:	788693bab8af0424ad1969f690065660
URL:		http://mike.it-loops.com/rtsp/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.36}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RTSP conntrack module

%prep
%setup -q -n rtsp-linux-v2.6

%build
%build_kernel_modules -m nf_conntrack_rtsp nf_nat_rtsp

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m nf_conntrack_rtsp nf_nat_rtsp -d kernel/net

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc README.rst
/lib/modules/%{_kernel_ver}/kernel/net/*.ko*
