#!/usr/bin/env bash
# HyperOS Build System - FASE C: Packaging Real
# Este script construye todos los paquetes HyperOS de manera reproducible

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SCRIPT_DIR}"
PACKAGES_DIR="${WORKSPACE}/packages"
CORE_DIR="${WORKSPACE}/core"
DAEMON_DIR="${WORKSPACE}/packages/hyperos-daemon"
BUILD_DIR="${WORKSPACE}/build"
REPO_DIR="${BUILD_DIR}/repository"
ARTIFACTS_DIR="${BUILD_DIR}/artifacts"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    cat << EOF
HyperOS Build System v0.5

Uso: $0 <comando> [opciones]

Comandos:
  package <nombre>   Construir un paquete específico
  packages           Construir todos los paquetes HyperOS
  core               Construir hyperos-core
  repo               Crear repositorio local con paquetes
  clean              Limpiar directorios de build
  all                Ejecutar: core → packages → repo
  test               Ejecutar tests básicos
  help               Mostrar esta ayuda

Ejemplos:
  $0 package hyper-center
  $0 packages
  $0 all

EOF
    exit 1
}

setup_build_env() {
    log_info "Configurando entorno de build..."
    mkdir -p "${BUILD_DIR}" "${REPO_DIR}/x86_64" "${ARTIFACTS_DIR}"
    
    # Verificar dependencias básicas
    if ! command -v makepkg >/dev/null 2>&1; then
        log_warn "makepkg no encontrado. Modo simulación activado."
        export HYPEROS_SIMULATION=true
    fi
    
    command -v python >/dev/null 2>&1 || { log_error "python no encontrado."; exit 1; }
    
    if [[ "${HYPEROS_SIMULATION:-false}" == "true" ]]; then
        log_info "Entorno de build configurado (modo simulación)"
    else
        log_success "Entorno de build configurado"
    fi
}

build_core() {
    log_info "Construyendo hyperos-core..."
    
    cd "${CORE_DIR}"
    
    local pkgver="0.1.0"
    
    # Fixear PKGBUILD si es necesario
    if grep -q 'source=()' PKGBUILD; then
        log_info "Actualizando PKGBUILD de core..."
        cat > PKGBUILD << 'EOF'
# Maintainer: HyperOS Team <team@hyperos.org>
pkgname=hyperos-core
pkgver=0.1.0
pkgrel=1
pkgdesc="HyperOS shared core library"
arch=('x86_64')
url="https://hyperos.org"
license=('GPL-3.0-or-later')
depends=('python' 'python-pyside6')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
source=("hyperos-core-${pkgver}.tar.gz")
sha256sums=('SKIP')

prepare() {
    cp -a "${srcdir}/." "${srcdir}/hyperos-core-${pkgver}"
}

build() {
    cd "${srcdir}/hyperos-core-${pkgver}"
    python -m build --wheel --no-isolation
}

package() {
    cd "${srcdir}/hyperos-core-${pkgver}"
    python -m installer --destdir="${pkgdir}" dist/*.whl
    
    # Instalar metadatos adicionales
    install -Dm644 pyproject.toml "${pkgdir}/usr/share/hyperos/core/pyproject.toml"
}
EOF
    fi
    
    # Crear tarball para source
    if [[ -d "hyperos_core" ]]; then
        tar -czf "hyperos-core-${pkgver}.tar.gz" \
            --exclude='*.egg-info' \
            --exclude='dist' \
            --exclude='build' \
            hyperos_core pyproject.toml README.md 2>/dev/null || true
        
        log_info "Tarball creado: hyperos-core-${pkgver}.tar.gz"
    else
        log_warn "Directorio hyperos_core no encontrado"
    fi
    
    # Construir paquete (o simular)
    if [[ "${HYPEROS_SIMULATION:-false}" == "true" ]]; then
        log_info "Simulando build de hyperos-core..."
        mkdir -p "${REPO_DIR}/x86_64"
        touch "${REPO_DIR}/x86_64/hyperos-core-${pkgver}-1-x86_64.pkg.tar.zst"
        log_success "hyperos-core simulado (paquete placeholder creado)"
    else
        # Construir paquete real con makepkg
        makepkg --cleanbuild --force --noconfirm 2>&1 | tail -20
        
        # Mover al directorio de repositorio
        find . -name "*.pkg.tar.zst" -exec mv {} "${REPO_DIR}/x86_64/" \;
        
        log_success "hyperos-core construido"
    fi
}

build_package() {
    local pkg_name="$1"
    local pkg_dir="${PACKAGES_DIR}/${pkg_name}"
    
    if [[ ! -d "${pkg_dir}" ]]; then
        log_error "Paquete '${pkg_name}' no existe en ${pkg_dir}"
        return 1
    fi
    
    log_info "Construyendo ${pkg_name}..."
    cd "${pkg_dir}"
    
    # Leer versión del PKGBUILD
    local pkgver=$(grep '^pkgver=' PKGBUILD | cut -d'=' -f2)
    
    # Fixear source si está vacío
    if grep -q 'source=(".")' PKGBUILD || grep -q 'source=()' PKGBUILD; then
        log_info "Actualizando PKGBUILD con source correcto..."
        
        # Crear tarball del código fuente
        if [[ -d "src" ]]; then
            tar -czf "${pkg_name}-${pkgver}.tar.gz" \
                --exclude='*.egg-info' \
                --exclude='dist' \
                --exclude='build' \
                src data assets 2>/dev/null || true
            
            # Actualizar PKGBUILD
            sed -i 's|source=(".")|source("'"${pkg_name}-${pkgver}"'.tar.gz")|' PKGBUILD
            sed -i "s|source=()|source(\"${pkg_name}-${pkgver}.tar.gz\")|" PKGBUILD
        else
            log_warn "No se encontró directorio src en ${pkg_dir}"
        fi
    fi
    
    # Construir paquete
    if command -v makepkg >/dev/null 2>&1; then
        makepkg --cleanbuild --force --noconfirm 2>&1 | tail -20 || {
            log_error "Falló la construcción de ${pkg_name}"
            return 1
        }
        
        # Mover al directorio de repositorio
        find . -name "*.pkg.tar.zst" -exec mv {} "${REPO_DIR}/x86_64/" \; 2>/dev/null || true
        log_success "${pkg_name} construido"
    else
        log_warn "makepkg no disponible, simulando build de ${pkg_name}"
        # Simulación para entornos sin makepkg
        mkdir -p "${REPO_DIR}/x86_64"
        touch "${REPO_DIR}/x86_64/${pkg_name}-${pkgver}-1-x86_64.pkg.tar.zst"
    fi
}

build_all_packages() {
    log_info "Construyendo todos los paquetes HyperOS..."
    
    local packages=(
        "hyper-assistant"
        "hyper-backup"
        "hyper-center"
        "hyper-cli"
        "hyper-drivers"
        "hyper-gaming"
        "hyper-installer"
        "hyper-kernel"
        "hyper-settings"
        "hyper-store"
        "hyper-tools"
        "hyper-update"
        "hyper-welcome"
        "hyperos-daemon"
    )
    
    local failed=0
    for pkg in "${packages[@]}"; do
        if [[ -d "${PACKAGES_DIR}/${pkg}" ]]; then
            build_package "${pkg}" || ((failed++))
        else
            log_warn "Paquete ${pkg} no encontrado, saltando..."
        fi
    done
    
    if [[ ${failed} -gt 0 ]]; then
        log_warn "${failed} paquete(s) fallaron"
    else
        log_success "Todos los paquetes construidos"
    fi
}

create_repository() {
    log_info "Creando repositorio local HyperOS..."
    
    mkdir -p "${REPO_DIR}/x86_64"
    cd "${REPO_DIR}/x86_64"
    
    # Verificar si hay paquetes
    if ! ls *.pkg.tar.zst 1>/dev/null 2>&1; then
        log_warn "No se encontraron paquetes .pkg.tar.zst en ${REPO_DIR}/x86_64"
        return 1
    fi
    
    # Crear base de datos del repositorio
    if command -v repo-add >/dev/null 2>&1; then
        repo-add hyperos.db.tar.xz *.pkg.tar.zst 2>&1 | tail -10
        log_success "Repositorio creado con repo-add"
    else
        log_warn "repo-add no disponible, creando estructura básica..."
        # Crear archivos de base de datos manualmente (fallback)
        ls -1 *.pkg.tar.zst > hyperos.files
        log_info "Lista de paquetes guardada en hyperos.files"
    fi
    
    # Configurar pacman para usar el repositorio local
    cat > "${REPO_DIR}/pacman.conf.example" << EOF
# HyperOS Local Repository Configuration
# Agregar esto a /etc/pacman.conf

[hyperos]
SigLevel = Optional TrustAll
Server = file://${REPO_DIR}
EOF
    
    log_success "Repositorio configurado en ${REPO_DIR}"
}

run_tests() {
    log_info "Ejecutando tests básicos..."
    
    # Test 1: Verificar estructura de directorios
    [[ -d "${PACKAGES_DIR}" ]] || { log_error "packages/ no existe"; return 1; }
    [[ -d "${CORE_DIR}" ]] || { log_error "core/ no existe"; return 1; }
    
    # Test 2: Verificar PKGBUILDs existentes
    local pkgbuild_count=$(find "${PACKAGES_DIR}" -name "PKGBUILD" | wc -l)
    log_info "Encontrados ${pkgbuild_count} PKGBUILDs"
    
    # Test 3: Verificar pyproject.toml en cada paquete
    local pyproject_count=$(find "${PACKAGES_DIR}" -name "pyproject.toml" | wc -l)
    log_info "Encontrados ${pyproject_count} pyproject.toml"
    
    # Test 4: Verificar hyperos-core
    [[ -f "${CORE_DIR}/pyproject.toml" ]] || { log_error "core/pyproject.toml no existe"; return 1; }
    
    log_success "Tests básicos pasados"
}

clean_build() {
    log_info "Limpiando directorios de build..."
    
    # Limpiar core
    cd "${CORE_DIR}" && rm -rf build dist *.egg-info *.tar.gz
    
    # Limpiar paquetes
    find "${PACKAGES_DIR}" -type d \( -name "build" -o -name "dist" -o -name "*.egg-info" \) -exec rm -rf {} + 2>/dev/null || true
    find "${PACKAGES_DIR}" -name "*.tar.gz" -delete 2>/dev/null || true
    find "${PACKAGES_DIR}" -name "*.pkg.tar.zst" -delete 2>/dev/null || true
    
    # Limpiar build dir
    rm -rf "${BUILD_DIR}"
    
    log_success "Limpieza completada"
}

build_all() {
    log_info "=== HYPEROS FULL BUILD ==="
    
    setup_build_env
    build_core
    build_all_packages
    create_repository
    
    log_success "=== BUILD COMPLETADO ==="
    log_info "Paquetes disponibles en: ${REPO_DIR}/x86_64/"
    log_info "Para instalar el repositorio:"
    log_info "  sudo cp ${REPO_DIR}/pacman.conf.example /etc/pacman.d/hyperos.conf"
    log_info "  sudo pacman -Sy"
}

# Main
if [[ $# -lt 1 ]]; then
    usage
fi

case "$1" in
    package)
        [[ -z "${2:-}" ]] && { log_error "Nombre de paquete requerido"; exit 1; }
        setup_build_env
        build_package "$2"
        ;;
    packages)
        setup_build_env
        build_all_packages
        ;;
    core)
        setup_build_env
        build_core
        ;;
    repo)
        setup_build_env
        create_repository
        ;;
    clean)
        clean_build
        ;;
    all)
        build_all
        ;;
    test)
        run_tests
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        log_error "Comando desconocido: $1"
        usage
        ;;
esac
