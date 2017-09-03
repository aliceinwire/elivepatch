# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

PYTHON_COMPAT=( python{2_7,3_4,3_5,3_6} )

inherit distutils-r1

DESCRIPTION="elivepatch server"
HOMEPAGE="https://wiki.gentoo.org/wiki/User:Aliceinwire/elivepatch"
SRC_URI="https://github.com/aliceinwire/elivepatch-server/archive/${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="GPL-2+"
SLOT="0"
KEYWORDS="~amd64 ~x86"

RDEPEND="
dev-python/flask[${PYTHON_USEDEP}]
dev-python/flask-restful[${PYTHON_USEDEP}]"
DEPEND="${RDEPEND}
dev-python/setuptools[${PYTHON_USEDEP}]"
