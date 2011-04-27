#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%define		rel	1
Summary:	RTSP connection tracking modules
Name:		kernel%{_alt_kernel}-net-nf_rtsp
Version:	0.6.21
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2+
Group:		Base/Kernel
Source0:	http://mike.it-loops.com/rtsp/rtsp-module-2.6.36.tar.gz
# Source0-md5:	788693bab8af0424ad1969f690065660
URL:		https://github.com/maru-sama/rtsp-linux-v2.6
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.36}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RTSP extension for IP connection tracking.

%prep
%setup -q -n rtsp-linux-v2.6

grep '#define IP_NF_RTSP_VERSION "%{version}"' nf_conntrack_rtsp.h

# prepare makefile:
cat > Makefile << EOF
obj-m += nf_conntrack_rtsp.o nf_nat_rtsp.o
EOF

%build
%build_kernel_modules -m nf_conntrack_rtsp,nf_nat_rtsp

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m nf_conntrack_rtsp,nf_nat_rtsp -d kernel/net

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
