# HyperOS Packaging System

## Overview

HyperOS utiliza el sistema de empaquetado estándar de Arch Linux (`makepkg`/`pacman`) para distribuir sus componentes. Cada aplicación, librería y servicio es un paquete independiente que puede ser instalado, actualizado y removido usando las herramientas estándar de Arch.

## Estructura del Sistema de Paquetes

```
packages/
├── PKGBUILD.common       # Template común para todos los paquetes
├── hyper-center/         # Aplicación individual
│   ├── PKGBUILD          # Definición del paquete
│   ├── src/              # Código fuente
│   │   ├── pyproject.toml
│   │   └── hyper_center/
│   ├── data/             # Archivos de datos (.desktop, icons)
│   └── assets/           # Recursos gráficos
├── hyper-settings/
├── hyper-store/
└── ...
```

## PKGBUILD Anatomy

Cada paquete HyperOS sigue esta estructura:

```bash
# Maintainer: HyperOS Team <team@hyperos.org>
pkgname=hyper-center
pkgver=0.1.0
pkgrel=1
pkgdesc="HyperOS central control center"
arch=('x86_64')
url="https://hyperos.org"
license=('GPL-3.0-or-later')
depends=('python' 'python-pyside6' 'hyperos-core')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
source=("hyper-center-${pkgver}.tar.gz")
sha256sums=('SKIP')  # Reemplazar con checksum real en producción

build() {
    cd "${srcdir}/hyper-center-${pkgver}"
    python -m build --wheel --no-isolation
}

package() {
    cd "${srcdir}/hyper-center-${pkgver}"
    python -m installer --destdir="${pkgdir}" dist/*.whl
    
    # Instalar archivo .desktop
    install -Dm644 "${srcdir}/../data/hyper-center.desktop" \
        "${pkgdir}/usr/share/applications/hyper-center.desktop"
    
    # Instalar icono
    install -Dm644 "${srcdir}/../assets/icons/hyper-center.svg" \
        "${pkgdir}/usr/share/icons/hicolor/scalable/apps/hyper-center.svg"
}
```

## Construcción de Paquetes

### Build Individual

```bash
cd packages/hyper-center
makepkg --cleanbuild --force
```

### Build con el Sistema HyperOS

```bash
# Construir un paquete específico
./build.sh package hyper-center

# Construir todos los paquetes
./build.sh packages

# Construir solo hyperos-core
./build.sh core
```

## Proceso de Build

1. **Preparación**: El script crea un tarball del código fuente
2. **Build**: `python -m build` genera una wheel
3. **Package**: `python -m installer` instala la wheel en el directorio de destino
4. **Assets**: Se instalan archivos .desktop e iconos
5. **Resultado**: `.pkg.tar.zst` listo para instalación

## Repositorio Local

### Crear Repositorio

```bash
./build.sh repo
```

Esto genera:
```
build/repository/
├── x86_64/
│   ├── hyper-center-0.1.0-1-x86_64.pkg.tar.zst
│   ├── hyper-settings-0.1.0-1-x86_64.pkg.tar.zst
│   ├── ...
│   └── hyperos.db.tar.xz  # Base de datos del repo
└── pacman.conf.example
```

### Configurar Pacman

Agregar a `/etc/pacman.conf`:

```ini
[hyperos]
SigLevel = Optional TrustAll
Server = file:///path/to/hyperos/build/repository
```

O copiar el ejemplo generado:
```bash
sudo cp build/repository/pacman.conf.example /etc/pacman.d/hyperos.conf
sudo pacman -Sy
```

## Firma de Paquetes (Producción)

Para producción, los paquetes deben estar firmados:

### 1. Generar Clave

```bash
pacman-key --init
pacman-key --new-key "HyperOS Team <team@hyperos.org>"
```

### 2. Configurar makepkg.conf

En `/etc/makepkg.conf`:
```bash
SIGNPKG="gpg"
GPGKEY="YOUR_KEY_ID"
```

### 3. Firmar Paquete

```bash
makepkg --sign
```

### 4. Actualizar Repositorio con Firmas

```bash
repo-add -s hyperos.db.tar.xz *.pkg.tar.zst.sig
```

## Dependencias entre Paquetes HyperOS

Los paquetes HyperOS tienen dependencias internas:

```
hyper-center      → hyperos-core
hyper-settings    → hyperos-core
hyper-store       → hyperos-core, hyperos-daemon
hyper-update      → hyperos-core, hyperos-daemon
hyper-drivers     → hyperos-core
hyper-backup      → hyperos-core, snapper
hyper-assistant   → hyperos-core
hyper-welcome     → hyperos-core
hyper-installer   → hyperos-core, hyperos-daemon
hyper-gaming      → hyperos-core
hyper-tools       → (independiente)
hyper-kernel      → (independiente)
hyper-cli         → hyperos-core, hyperos-daemon
hyperos-daemon    → hyperos-core
```

**Orden de construcción recomendado:**
1. `hyperos-core` (base)
2. `hyperos-daemon` (servicios)
3. Resto de aplicaciones

## Versionado

HyperOS sigue versionado semántico:

```
pkgver=0.1.0  # Major.Minor.Patch
pkgrel=1      # Release del paquete (rebuilds)
```

- **Major**: Cambios incompatibles
- **Minor**: Nuevas funcionalidades compatibles
- **Patch**: Bug fixes
- **pkgrel**: Rebuilds sin cambios de versión (ej: fix de PKGBUILD)

## Problemas Comunes y Soluciones

### source=() vacío

**Problema**: PKGBUILD tiene `source=()` o `source=(".")`

**Solución**: El script `build.sh` automáticamente:
1. Crea tarball del código fuente
2. Actualiza el campo `source=` con el nombre correcto

### Dependencia circular

**Problema**: Paquete A depende de B, y B depende de A

**Solución**: Refactorizar dependencias comunes en `hyperos-core`

### Falta de pyproject.toml

**Problema**: El paquete no tiene `pyproject.toml` válido

**Solución**: Crear `pyproject.toml` con metadata mínima:
```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "hyper-center"
version = "0.1.0"
dependencies = ["PySide6>=6.6", "hyperos-core>=0.1.0"]
```

## Testing de Paquetes

### Verificar Integridad

```bash
# Verificar que el paquete se construye
./build.sh package hyper-center

# Verificar que las dependencias son correctas
makepkg --printsrcinfo

# Listar archivos del paquete
tar -tzf hyper-center-*.pkg.tar.zst
```

### Install Test

```bash
# Instalar en entorno de prueba
sudo pacman -U hyper-center-*.pkg.tar.zst

# Verificar instalación
which hyper-center
ls /usr/share/applications/hyper-center.desktop
```

## Estado Actual (v1.0.0)

Todos los paquetes se construyen reales en CI (workflow build-iso.yml, usuario `builduser`, `makepkg` + `repo-add`) y se publican en cada release:

| Paquete | PKGBUILD | Source | Buildable | Notas |
|---------|----------|--------|-----------|-------|
| hyperos-core | ✅ | ✅ | ✅ | Librería base (PySide6) |
| hyperos-daemon | ✅ | ✅ | ✅ | Daemon del sistema |
| hyper-center | ✅ | ✅ | ✅ | |
| hyper-settings | ✅ | ✅ | ✅ | |
| hyper-store | ✅ | ✅ | ✅ | |
| hyper-update | ✅ | ✅ | ✅ | |
| hyper-drivers | ✅ | ✅ | ✅ | |
| hyper-backup | ✅ | ✅ | ✅ | |
| hyper-assistant | ✅ | ✅ | ✅ | |
| hyper-welcome | ✅ | ✅ | ✅ | |
| hyper-installer | ✅ | ✅ | ✅ | |
| hyper-gaming | ✅ | ✅ | ✅ | main.py en /usr/bin |
| hyper-tools | ✅ | ✅ | ✅ | source=() + sha256sums=() |
| hyper-kernel | ✅ | ✅ | ✅ | main.py en /usr/bin |
| hyper-cli | ✅ | ✅ | ✅ | main.py en /usr/bin |

### Errores corregidos en v1.0.0 (CI-validado)

- `python-pyside6` → **`pyside6`** (nombre real en repos oficiales; `python-pyside6` no existe)
- `source("...")` → `source=("...")` (sintaxis válida de PKGBUILD)
- core `prepare()`: `cp -r` sobre sí mismo fallaba → `mv` idempotente
- hyper-tools: `sha256sums=('SKIP')` con `source=()` rompía la integridad → `sha256sums=()`
- rofi-lbonn-wayland (AUR) → `rofi` en `archiso/packages.x86_64`

**Leyenda:**
- ✅ Completo
- ⚠️ Parcial/Requiere atención
- ❌ Faltante

## Próximos Pasos

1. **Implementar builds reales** en Arch Linux con makepkg
2. **Configurar firma de paquetes** para producción
3. **Crear repositorio remoto** accesible vía HTTPS
4. **Automatizar releases** con CI/CD
5. **Agregar tests de integración** post-instalación

## Referencias

- [Arch Wiki - Creating Packages](https://wiki.archlinux.org/title/Creating_packages)
- [Arch Wiki - Package Repository](https://wiki.archlinux.org/title/Creating_packages#Package_repository)
- [PKGBUILD(5) Man Page](https://man.archlinux.org/man/PKGBUILD.5)
- [Python Packaging Guide](https://packaging.python.org/)
