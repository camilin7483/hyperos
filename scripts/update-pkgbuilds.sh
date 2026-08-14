#!/bin/bash
# Script para actualizar todos los PKGBUILDs con la estructura correcta

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

update_pkgbuild() {
    local pkg_dir="$1"
    local pkg_name
    pkg_name=$(basename "$pkg_dir")
    local pkgbuild="${pkg_dir}/PKGBUILD"
    
    if [[ ! -f "$pkgbuild" ]]; then
        echo "SKIP: $pkg_name (no PKGBUILD)"
        return
    fi
    
    # Leer metadata existente
    local pkgdesc depends_line has_python has_pyside6 has_hyperos_core
    pkgdesc=$(grep "^pkgdesc=" "$pkgbuild" | cut -d'"' -f2)
    depends_line=$(grep "^depends=" "$pkgbuild")
    has_python=$(echo "$depends_line" | grep -c "'python'" || true)
    has_pyside6=$(echo "$depends_line" | grep -c "'python-pyside6'" || true)
    has_hyperos_core=$(echo "$depends_line" | grep -c "'hyperos-core'" || true)
    
    # Verificar si es paquete Python con src/
    local has_src=false
    if [[ -d "${pkg_dir}/src" ]] && [[ -f "${pkg_dir}/src/pyproject.toml" ]]; then
        has_src=true
    fi
    
    # Determinar tipo de paquete
    local pkg_type="python"
    if [[ "$has_pyside6" -eq 0 ]] && [[ "$has_python" -gt 0 ]]; then
        pkg_type="python-simple"
    elif [[ "$has_python" -eq 0 ]]; then
        pkg_type="bash"
    fi
    
    # Construir nuevo PKGBUILD
    cat > "$pkgbuild" << EOF
# Maintainer: HyperOS Team <team@hyperos.org>
pkgname=${pkg_name}
pkgver=0.1.0
pkgrel=1
pkgdesc="${pkgdesc}"
arch=('x86_64')
url="https://hyperos.org"
license=('GPL-3.0-or-later')
EOF

    # Agregar dependencias
    if [[ "$pkg_type" == "python" ]] || [[ "$pkg_type" == "python-simple" ]]; then
        if [[ "$has_pyside6" -gt 0 ]]; then
            echo "depends=('python' 'python-pyside6'$( [[ "$has_hyperos_core" -gt 0 ]] && echo " 'hyperos-core'" ))" >> "$pkgbuild"
        else
            echo "depends=('python'$( [[ "$has_hyperos_core" -gt 0 ]] && echo " 'hyperos-core'" ))" >> "$pkgbuild"
        fi
        echo "makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')" >> "$pkgbuild"
    else
        # Bash scripts - mantener dependencias originales si existen
        echo "depends=('bash' 'coreutils')" >> "$pkgbuild"
    fi
    
    # Source
    if [[ "$has_src" == true ]]; then
        echo 'source=(".")' >> "$pkgbuild"
    else
        echo 'source=()' >> "$pkgbuild"
    fi
    
    echo "sha256sums=('SKIP')" >> "$pkgbuild"
    echo "" >> "$pkgbuild"
    
    # Build function
    if [[ "$has_src" == true ]]; then
        cat >> "$pkgbuild" << 'EOF'
build() {
    cd "${srcdir}/src"
    python -m build --wheel --no-isolation
}

EOF
    fi
    
    # Package function
    echo "package() {" >> "$pkgbuild"
    
    if [[ "$has_src" == true ]]; then
        cat >> "$pkgbuild" << 'EOF'
    cd "${srcdir}/src"
    python -m installer --destdir="${pkgdir}" dist/*.whl
EOF
    elif [[ "$pkg_type" == "bash" ]]; then
        # Mantener lógica original para bash scripts
        if [[ -f "${pkg_dir}/src/main.py" ]]; then
            echo "    install -Dm755 \"\${srcdir}/src/main.py\" \"\${pkgdir}/usr/bin/\${pkgname}\"" >> "$pkgbuild"
        elif [[ -d "${pkg_dir}/src" ]]; then
            {
                echo "    for script in \"\${srcdir}/\"*; do"
                echo "        [ -f \"\$script\" ] && install -Dm755 \"\$script\" \"\${pkgdir}/usr/bin/\""
                echo "    done"
            } >> "$pkgbuild"
        fi
    fi
    
    # Desktop files e icons si existen
    if [[ -f "${pkg_dir}/data/${pkg_name}.desktop" ]]; then
        echo "    install -Dm644 \"\${srcdir}/../data/${pkg_name}.desktop\" \"\${pkgdir}/usr/share/applications/${pkg_name}.desktop\"" >> "$pkgbuild"
    fi
    
    if [[ -f "${pkg_dir}/assets/icons/${pkg_name}.svg" ]]; then
        echo "    install -Dm644 \"\${srcdir}/../assets/icons/${pkg_name}.svg\" \"\${pkgdir}/usr/share/icons/hicolor/scalable/apps/${pkg_name}.svg\"" >> "$pkgbuild"
    fi
    
    echo "}" >> "$pkgbuild"
    
    echo "OK: $pkg_name (${pkg_type})"
}

# Main
echo "Actualizando PKGBUILDs..."
for pkg_dir in "${SCRIPT_DIR}/packages/"*/; do
    update_pkgbuild "$pkg_dir"
done

# Actualizar core
update_pkgbuild "${SCRIPT_DIR}/core/"

echo "Completado!"
