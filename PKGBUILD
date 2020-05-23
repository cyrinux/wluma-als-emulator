# Maintainer: Cyrinux <pkgbuilds AT levis DOT name>

pkgname=wluma-als-emulator-git
_gitname=wluma-als-emulator
pkgver=master
pkgrel=6
pkgdesc="Fake light sensor for wluma, write lux from webcam or time based to a file"
license=(MIT)
url=https://github.com/cyrinux/fake-light-sensor
depends=()
optdepends=('wluma' 'python-pillow' 'ffmpeg')
arch=(any)
makedepends=('git')
conflicts=('fake-light-sensor')
provides=('fake-light-sensor')
source=('git://github.com/cyrinux/wluma-als-emulator')
md5sums=('SKIP')

pkgver() {
    cd "${srcdir}/wluma-als-emulator"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
    cd "${srcdir}/wluma-als-emulator"
    install -D -m0755 \
        "${srcdir}/wluma-als-emulator/wluma-als-emulator" \
        "$pkgdir/usr/bin/wluma-als-emulator"
}
