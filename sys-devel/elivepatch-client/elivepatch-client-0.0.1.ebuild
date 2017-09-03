# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

PYTHON_COMPAT=( python{2_7,3_4,3_5,3_6} )

inherit distutils-r1

DESCRIPTION="elivepatch server"
HOMEPAGE="https://wiki.gentoo.org/wiki/User:Aliceinwire/elivepatch"
SRC_URI="https://github.com/aliceinwire/elivepatch-client/archive/${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="GPL-2+"
SLOT="0"
KEYWORDS="~amd64 ~x86"

RDEPEND="
dev-python/git-python[${PYTHON_USEDEP}]
dev-python/requests[${PYTHON_USEDEP}]
"
DEPEND="${iRDEPEND}
dev-python/setuptools[${PYTHON_USEDEP}]"
