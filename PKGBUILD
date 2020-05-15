# Maintainer: Cyrinux <pkgbuilds AT levis DOT name>

pkgname=fake-light-sensor-git
_gitname=fake-light-sensor
pkgver=master
pkgrel=1
pkgdesc="Fake light sensor for wluma, write lux from webcam to a file"
license=( MIT )
url=https://github.com/cyrinux/fake-light-sensor
depends=( 'python-pillow' 'ffmpeg' )
optdepends=( 'wluma' )
arch=( any )
makedepends=( 'git' )
conflicts=( 'fake-light-sensor' )
provides=( 'fake-light-sensor'  )
source=( 'git://github.com/cyrinux/fake-light-sensor' )
md5sums=('SKIP')

pkgver() {
    cd "${srcdir}/fake-light-sensor"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
    cd "${srcdir}/fake-light-sensor"
    install -D -m0755 \
        "${srcdir}/fake-light-sensor/fake-light-sensor" \
        "$pkgdir/usr/bin/fake-light-sensor"
    install -D -m0644 \
        "${srcdir}/fake-light-sensor/fake-light-sensor.service" \
        "$pkgdir/usr/lib/systemd/user/fake-light-sensor.service"
}
