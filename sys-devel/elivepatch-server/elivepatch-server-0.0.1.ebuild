# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

PYTHON_COMPAT=( python2_7 python3_{4,5,6} )
PYTHON_REQ_USE='bzip2(+)'

inherit distutils-r1

DESCRIPTION="elivepatch server"
HOMEPAGE="https://wiki.gentoo.org/wiki/User:Aliceinwire/elivepatch"
SRC_URI="https://github.com/aliceinwire/elivepatch-server/archive/${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="GPL-2+"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE=""

DEPEND=""
RDEPEND="${DEPEND}"


python_prepare_all() {
    distutils-r1_python_prepare_all
}

python_install() {
    # Install sbin scripts to bindir for python-exec linking
    # they will be relocated in pkg_preinst()
    distutils-r1_python_install \
        --system-prefix="${EPREFIX}/usr" \
        --bindir="$(python_get_scriptdir)" \
        --docdir="${EPREFIX}/usr/share/doc/${PF}" \
        --htmldir="${EPREFIX}/usr/share/doc/${PF}/html" \
        --sbindir="$(python_get_scriptdir)" \
        --sysconfdir="${EPREFIX}/etc" \
        "${@}"
}


