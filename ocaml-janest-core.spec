Name:           ocaml-janest-core
Version:        0.5.3
Release:        %mkrel 2
Summary:        Jane Street Capital's alternative standard library for OCaml
License:        LGPL + linking exception
Group:          Development/Other
URL:            http://www.janestcapital.com/ocaml/
Source0:        http://www.janestreet.com/ocaml/core-%{version}.tgz
Patch0:         0003-add-missing-META-dep-on-unix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ncurses-devel
BuildRequires:  ocaml-findlib
BuildRequires:  camlp4
BuildRequires:  ocaml-res-devel
BuildRequires:  ocaml-sexplib-devel
BuildRequires:  ocaml-type-conv
BuildRequires:  ocaml-bin-prot-devel
BuildRequires:  ocaml-ounit-devel

%description
Core is Jane Street Capital's alternative standard library for OCaml.

Core does a number of things: it provides tail recursive versions of
non tail recursive functions in the standard library; changes the
signature of many of the standard modules; includes generic
serialization for most types, and adds some entirely new modules and
new functionality within existing modules.

Beware: Core extends some functionality from OCaml's standard
library, and outright changes or replaces other. The goal is not to
preserve complete compatibility with the standard.

Summary of functionalities:

 - Bag (set type with duplicates)
 - Bigbuffer (unlimited Buffer type)
 - Bigstring (unlimited String type)
 - 8/16/32/64-bit signed/unsigned binary packing functions
 - Bool type
 - Safe finalization for reading/writing files
 - Function composition operators
 - Enhanced versions of stdlib modules such as Arg, Array, Printf, etc.
 - Mutexes
 - CRC functions
 - Dequeue type
 - Doubly-linked list type
 - Enhanced exception module
 - Fast hash table
 - Force once (thunk that can be forced only once)
 - Functional queue type
 - Min-heap type
 - Enhanced input/output channels
 - Closed interval type
 - Interval set type
 - Read files as lines
 - Linux-specific syscalls such as sendfile, get/set TCP options, epoll, splice
 - Memoization
 - Piece-wise linear interpolation of floats
 - Polymorphic map and set
 - Find size of OCaml structures
 - Space-efficient tuples
 - Synchronized queues
 - Thread-safe queues
 - Convenience functions for Unix times
 - Timed events
 - Tuple convenience functions
 - Extended Unix module filling in some missing syscalls such as sync,
   getrusage, initgroups, etc.

Most enhanced types are sexp-able and bin-prot-able.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n core-%{version}

%build
make

mkdir doc
pushd doc
ocamldoc -html -sort \
  -I +threads -I +sexplib -I +bin-prot -I +res -I +type-conv \
  -I ../lib \
  -pp cpp \
  ../lib/*.ml{,i} ||:
popd


%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
export DLLDIR=$OCAMLFIND_DESTDIR/stublibs
mkdir -p $OCAMLFIND_DESTDIR/stublibs
mkdir -p $OCAMLFIND_DESTDIR/core
make install

strip $OCAMLFIND_DESTDIR/stublibs/dll*.so
chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so

pushd lib
cp  bigstring.mli bucket.ml common.mli core_array.mli core_char.mli core_int.mli core_int32.mli core_int64.mli core_list.mli core_nativeint.mli core_sexp.mli core_stack.mli core_string.mli core_unix.mli dequeue.mli fast_hashtbl.mli float.mli interval.mli interval_set.mli linux_ext.mli option.mli pMap.mli piecewise_linear.mli result.mli std.ml time.mli unix_ext.mli word_size.mli tuple.mli stringable.ml size.mli setable.ml robustly_comparable.ml pretty_printer.mli pSet.mli out_channel.mli monad.ml memo.mli fqueue.mli force_once.mli floatable.ml equatable.ml crc.mli core_printf.mli core_hashtbl.mli container.ml comparable.ml caml.ml backtrace.ml space_safe_tuple.mli sexpable.ml ordered_collection_common.mli int_conversions.ml in_channel.mli heap.mli hash_set.ml exn.mli error_check.ml doubly_linked.mli core_sys.ml core_arg.mli binable.ml bigbuffer.mli ref.mli hash_queue.ml core_queue.mli core_mutex.mli bag.mli thread_safe_queue.mli hashable.ml month.mli interfaces.ml core_gc.mli bool.mli std_internal.ml interned.ml int_intf.ml unique_id.ml timer.mli squeue.mli quickcheck.ml linebuf.mli core_filename.mli binary_packing.mli OUnit_utils.ml  $OCAMLFIND_DESTDIR/core/
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT LICENSE INSTALL README CHANGES
%dir %{_libdir}/ocaml/core
%{_libdir}/ocaml/core/META
%{_libdir}/ocaml/core/*.cma
%{_libdir}/ocaml/core/*.cmi
%{_libdir}/ocaml/stublibs/*.so*

%files devel
%defattr(-,root,root)
%doc doc
%{_libdir}/ocaml/core/*.a
%{_libdir}/ocaml/core/*.cmxa
%{_libdir}/ocaml/core/*.ml
%{_libdir}/ocaml/core/*.mli

