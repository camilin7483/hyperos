#!/bin/bash
# Script para subir HyperOS a GitHub

set -e

echo "🚀 Preparando HyperOS para GitHub..."

# Verificar que estamos en el directorio correcto
if [ ! -f "build.sh" ]; then
    echo "❌ Error: No se encontró build.sh. ¿Estás en el directorio raíz de HyperOS?"
    exit 1
fi

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Verificar git
echo -e "${YELLOW}Paso 1: Verificando Git...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git no está instalado${NC}"
    echo "Instalar con: sudo pacman -S git"
    exit 1
fi
echo -e "${GREEN}✅ Git disponible${NC}"

# Paso 2: Inicializar repositorio si no existe
echo -e "${YELLOW}Paso 2: Inicializando repositorio...${NC}"
if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✅ Repositorio inicializado${NC}"
else
    echo -e "${GREEN}✅ Repositorio ya existe${NC}"
fi

# Paso 3: Crear .gitignore si no existe
if [ ! -f ".gitignore" ]; then
    echo "Creando .gitignore..."
    cat > .gitignore << 'GITIGNORE'
# Build artifacts
build/
dist/
*.iso
*.pkg.tar.zst
repo/x86_64/*.pkg.tar.zst
repo/hyperos.db
repo/hyperos.files

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/
.eggs/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
journal/

# Temp
tmp/
temp/
*.tmp

# Keys (nunca subir claves privadas)
*.gpg
*.key
private/
GITIGNORE
    echo -e "${GREEN}✅ .gitignore creado${NC}"
fi

# Paso 4: Añadir remote
echo -e "${YELLOW}Paso 4: Configurando remote de GitHub...${NC}"
echo "Ingresa tu usuario de GitHub:"
read -r GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo -e "${RED}❌ Usuario no puede estar vacío${NC}"
    exit 1
fi

REPO_URL="https://github.com/${GITHUB_USER}/hyperos.git"

# Eliminar remote existente si hay
git remote remove origin 2>/dev/null || true

echo "¿Quieres usar HTTPS o SSH? (h/s):"
read -r PROTOCOL

if [ "$PROTOCOL" = "s" ] || [ "$PROTOCOL" = "ssh" ]; then
    REPO_URL="git@github.com:${GITHUB_USER}/hyperos.git"
fi

git remote add origin "$REPO_URL"
echo -e "${GREEN}✅ Remote configurado: $REPO_URL${NC}"

# Paso 5: Revisar cambios
echo -e "${YELLOW}Paso 5: Revisando cambios...${NC}"
git status

echo ""
echo "¿Quieres proceder con el commit? (y/n):"
read -r CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Operación cancelada"
    exit 0
fi

# Paso 6: Añadir todos los archivos
echo -e "${YELLOW}Paso 6: Añadiendo archivos...${NC}"
git add -A
echo -e "${GREEN}✅ Archivos añadidos${NC}"

# Paso 7: Commit
echo -e "${YELLOW}Paso 7: Creando commit...${NC}"
git commit -m "feat: HyperOS v1.0.0 - Stable Release

- Distribución Linux completa basada en Arch Linux
- Hyprland/Wayland como entorno de escritorio
- 13 aplicaciones HyperOS nativas
- Instalador gráfico UEFI/GPT funcional
- Daemon central con D-Bus IPC
- Repositorio propio con firma GPG
- ISO booteable con archiso
- Testing suite completo
- CI/CD pipeline
- Documentación completa

Signed-off-by: HyperOS Team <team@hyperos.org>"

echo -e "${GREEN}✅ Commit creado${NC}"

# Paso 8: Tag
echo -e "${YELLOW}Paso 8: Creando tag v1.0.0...${NC}"
git tag -a v1.0.0 -m "HyperOS v1.0.0 - Stable Release

Primera versión estable de HyperOS:
✅ ISO booteable
✅ Instalador gráfico funcional
✅ 13 aplicaciones nativas
✅ Repositorio con firma GPG
✅ Testing completo
✅ Documentación completa

Release date: $(date +%Y-%m-%d)"

echo -e "${GREEN}✅ Tag v1.0.0 creado${NC}"

# Paso 9: Push
echo -e "${YELLOW}Paso 9: Subiendo a GitHub...${NC}"
echo ""
echo "⚠️  Antes de continuar, asegúrate de:"
echo "   1. Haber creado el repositorio 'hyperos' en tu cuenta de GitHub"
echo "   2. Tener permisos de escritura"
echo ""
echo "Presiona Enter cuando estés listo..."
read -r

git branch -M main
git push -u origin main --tags

echo -e "${GREEN}✅ ¡Subido exitosamente!${NC}"

# Paso 10: Instrucciones finales
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🎉 ¡HyperOS v1.0.0 subido a GitHub!            ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo "📍 Tu repositorio está en:"
echo "   https://github.com/${GITHUB_USER}/hyperos"
echo ""
echo "📝 Próximos pasos:"
echo "   1. Configurar GitHub Actions (ya incluidos en .github/workflows/)"
echo "   2. Agregar descripción y website al repositorio"
echo "   3. Crear Release en GitHub desde el tag v1.0.0"
echo "   4. Adjuntar la ISO construida al Release"
echo "   5. Compartir en redes sociales"
echo ""
echo "🔗 Enlaces útiles:"
echo "   - Issues: https://github.com/${GITHUB_USER}/hyperos/issues"
echo "   - Releases: https://github.com/${GITHUB_USER}/hyperos/releases"
echo "   - Actions: https://github.com/${GITHUB_USER}/hyperos/actions"
echo ""
echo "¡Gracias por contribuir a HyperOS! 🚀"
