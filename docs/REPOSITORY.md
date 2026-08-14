# HyperOS Repository

## Overview

HyperOS mantiene su propio repositorio de paquetes para distribuir aplicaciones, librerías y servicios específicos de la distribución. El repositorio sigue el formato estándar de Arch Linux, compatible con `pacman`.

## Estructura del Repositorio

```
repository/
├── x86_64/
│   ├── hyperos-core-0.1.0-1-x86_64.pkg.tar.zst
│   ├── hyperos-daemon-0.1.0-1-x86_64.pkg.tar.zst
│   ├── hyper-center-0.1.0-1-x86_64.pkg.tar.zst
│   ├── hyper-settings-0.1.0-1-x86_64.pkg.tar.zst
│   ├── ...
│   ├── hyperos.db.tar.xz       # Base de datos principal
│   ├── hyperos.db              # Symlink o copia
│   └── hyperos.files           # Lista de archivos (opcional)
└── pacman.conf.example         # Configuración de ejemplo
```

## Tipos de Repositorios

### 1. Repositorio Local (Desarrollo)

Ubicación: `build/repository/`

Uso: Desarrollo y testing local

Configuración en `/etc/pacman.conf`:
```ini
[hyperos]
SigLevel = Optional TrustAll
Server = file:///workspace/build/repository
```

### 2. Repositorio Remoto (Producción)

Ubicación: Servidor HTTPS (ej: `repo.hyperos.org`)

Uso: Distribución pública

Configuración en `/etc/pacman.conf`:
```ini
[hyperos]
SigLevel = Required DatabaseOptional
Server = https://repo.hyperos.org/$arch
```

## Creación del Repositorio

### Método Automático (Recomendado)

```bash
./build.sh repo
```

Este comando:
1. Escanea `build/repository/x86_64/` en busca de paquetes `.pkg.tar.zst`
2. Genera la base de datos `hyperos.db.tar.xz` usando `repo-add`
3. Crea archivo de configuración `pacman.conf.example`

### Método Manual

```bash
cd build/repository/x86_64

# Crear base de datos
repo-add hyperos.db.tar.xz *.pkg.tar.zst

# Verificar
ls -la hyperos.db*
```

## Base de Datos del Repositorio

La base de datos contiene metadata de todos los paquetes:

- Nombre del paquete
- Versión
- Descripción
- Dependencias
- Tamaño
- Checksums
- URL de descarga

### Formato

Arch Linux usa `tar.xz` comprimido:
- `hyperos.db.tar.xz` - Base de datos principal (requerida)
- `hyperos.db` - Puede ser symlink o copia sin comprimir

## Firma de Paquetes

### Por qué Firmar

La firma de paquetes garantiza:
- **Autenticidad**: El paquete viene de HyperOS Team
- **Integridad**: El paquete no fue modificado
- **Confianza**: Previene ataques man-in-the-middle

### Configurar Firma

#### 1. Generar Clave GPG

```bash
# Generar clave maestra
gpg --full-generate-key

# Información recomendada:
# - Tipo: RSA and RSA
# - Longitud: 4096 bits
# - Validez: 2y o 5y
# - Nombre: HyperOS Team
# - Email: team@hyperos.org
```

#### 2. Inicializar pacman-key

```bash
sudo pacman-key --init
sudo pacman-key --add-key YOUR_KEY_ID
sudo pacman-key --lsign-key YOUR_KEY_ID
```

#### 3. Configurar makepkg

En `/etc/makepkg.conf`:
```bash
PACKAGER="HyperOS Team <team@hyperos.org>"
GPGKEY="YOUR_KEY_ID"
SIGNPKG="gpg"
```

#### 4. Firmar Paquetes

```bash
# Firmar durante el build
makepkg --sign

# O firmar paquete existente
gpg --detach-sign --no-armor hyperos-core-0.1.0-1-x86_64.pkg.tar.zst
```

#### 5. Actualizar Repositorio con Firmas

```bash
# -s: buscar y agregar firmas
repo-add -s hyperos.db.tar.xz *.pkg.tar.zst
```

### Niveles de Firma (SigLevel)

En `pacman.conf`:

```ini
# Desarrollo (sin verificación estricta)
SigLevel = Optional TrustAll

# Producción (verificación requerida)
SigLevel = Required DatabaseOptional

# Máxima seguridad
SigLevel = Required PackageRequired
```

**Opciones:**
- `Required`: Requiere firma válida
- `Optional`: Acepta paquetes sin firma
- `TrustAll`: Confía en todas las firmas
- `DatabaseOptional`: Base de datos opcionalmente firmada
- `PackageRequired`: Paquetes deben estar firmados

## Actualización del Repositorio

### Agregar Nuevo Paquete

```bash
# 1. Construir paquete
./build.sh package hyper-center

# 2. Mover al repositorio
mv packages/hyper-center/*.pkg.tar.zst build/repository/x86_64/

# 3. Actualizar base de datos
cd build/repository/x86_64
repo-add hyperos.db.tar.xz hyper-center-*.pkg.tar.zst
```

### Remover Paquete Obsoleto

```bash
# 1. Remover archivo del paquete
rm build/repository/x86_64/hyper-center-0.0.9-1-x86_64.pkg.tar.zst

# 2. Regenerar base de datos
cd build/repository/x86_64
rm hyperos.db*
repo-add hyperos.db.tar.xz *.pkg.tar.zst
```

### Actualizar Paquete Existente

```bash
# pacman automáticamente usará la versión más nueva
# basado en pkgver y pkgrel

# Ejemplo: 0.1.0-1 → 0.1.0-2 (rebuild)
# Ejemplo: 0.1.0-1 → 0.2.0-1 (nueva versión)
```

## Configuración de Pacman

### Archivo de Configuración

`/etc/pacman.conf`:

```ini
[options]
Architecture = auto
Color
CheckSpace
VerbosePkgLists

# Repositorios oficiales de Arch
[core]
Include = /etc/pacman.d/mirrorlist

[extra]
Include = /etc/pacman.d/mirrorlist

# Repositorio HyperOS
[hyperos]
SigLevel = Required DatabaseOptional
Server = https://repo.hyperos.org/x86_64
# Para desarrollo local:
# Server = file:///workspace/build/repository
```

### mirrorlist

Para repositorios remotos, crear `/etc/pacman.d/hyperos-mirrorlist`:

```
## HyperOS Mirrorlist
Server = https://repo.hyperos.org/$arch
Server = https://mirror2.hyperos.org/$arch
```

## Comandos Útiles

### Listar Paquetes Disponibles

```bash
# Buscar en repositorio
pacman -Sl hyperos

# Buscar específico
pacman -Ss hyper-center
```

### Instalar Paquete

```bash
sudo pacman -S hyper-center
```

### Actualizar Todo HyperOS

```bash
sudo pacman -Syu hyperos
```

### Verificar Estado del Repositorio

```bash
# Verificar base de datos
pacman -Sy

# Listar todos los paquetes de hyperos
pacman -Sl hyperos | column -t
```

## Problemas Comunes

### Error: Invalid signature

**Causa**: Paquetes no firmados o clave no importada

**Solución**:
```bash
# Importar clave
sudo pacman-key --recv-keys KEY_ID
sudo pacman-key --lsign-key KEY_ID

# O desactivar verificación temporalmente (solo desarrollo)
SigLevel = Optional TrustAll
```

### Error: Failed to synchronize database

**Causa**: URL incorrecta o servidor inaccesible

**Solución**:
```bash
# Verificar conectividad
curl -I https://repo.hyperos.org/x86_64/hyperos.db.tar.xz

# Forzar actualización
pacman -Syy
```

### Error: Package not found

**Causa**: Paquete no está en la base de datos

**Solución**:
```bash
# Regenerar base de datos
cd /path/to/repo/x86_64
repo-add hyperos.db.tar.xz *.pkg.tar.zst

# Actualizar cache local
pacman -Syy
```

### Conflictos de Versión

**Causa**: Múltiples versiones del mismo paquete

**Solución**:
```bash
# Mantener solo la versión más reciente
# Eliminar versiones antiguas manualmente
rm hyper-center-0.0.*-*.pkg.tar.zst

# Regenerar base de datos
repo-add hyperos.db.tar.xz *.pkg.tar.zst
```

## Hosting del Repositorio

### Opciones de Hosting

1. **GitHub Pages** (gratuito, solo HTTP)
2. **GitLab Pages** (gratuito, HTTPS disponible)
3. **AWS S3 + CloudFront** (pago, escalable)
4. **Servidor propio** (control total)

### Ejemplo: GitHub Pages

```bash
# 1. Crear rama gh-pages
git checkout --orphan gh-pages
git reset --hard

# 2. Copiar archivos del repositorio
mkdir -p x86_64
cp build/repository/x86_64/* x86_64/

# 3. Commit y push
git add .
git commit -m "Deploy repository"
git push origin gh-pages
```

URL resultante: `https://username.github.io/repo/x86_64/`

### Ejemplo: Servidor Nginx

```nginx
server {
    listen 443 ssl;
    server_name repo.hyperos.org;

    ssl_certificate /etc/ssl/certs/hyperos.crt;
    ssl_certificate_key /etc/ssl/private/hyperos.key;

    root /var/www/hyperos-repo;
    index hyperos.db.tar.xz;

    location / {
        autoindex on;
        types {
            application/x-xz hyperos.db.tar.xz;
            application/zstd *.pkg.tar.zst;
        }
    }
}
```

## Seguridad del Repositorio

### Mejores Prácticas

1. **HTTPS siempre**: Nunca servir repositorio sobre HTTP en producción
2. **Firmar paquetes**: Usar GPG para todos los paquetes
3. **Rotar claves**: Renovar claves GPG antes de expiración
4. **Backup de claves**: Mantener backup seguro de claves privadas
5. **Access control**: Limitar quién puede subir paquetes
6. **Audit logs**: Registrar todas las operaciones

### Checklist de Seguridad

- [ ] Clave GPG generada y configurada
- [ ] Todos los paquetes firmados
- [ ] SigLevel = Required en producción
- [ ] HTTPS configurado correctamente
- [ ] Certificados SSL válidos
- [ ] Backup de claves privadas
- [ ] Procedimiento de revocación definido

## Métricas del Repositorio

### Monitoreo

- Número de paquetes
- Tamaño total del repositorio
- Descargas por paquete
- Errores de sincronización
- Tiempo de respuesta del servidor

### Estadísticas Actuales (v0.5)

| Métrica | Valor |
|---------|-------|
| Paquetes totales | 15 |
| Tamaño estimado | ~50 KB (placeholders) |
| Arquitectura | x86_64 |
| Estado | Desarrollo |

## Referencias

- [Arch Wiki - Package Repository](https://wiki.archlinux.org/title/Creating_packages#Package_repository)
- [repo-add Man Page](https://man.archlinux.org/man/repo-add.8)
- [Pacman.conf Man Page](https://man.archlinux.org/man/pacman.conf.5)
- [Arch Signing Guidelines](https://wiki.archlinux.org/title/Pacman/Package_signing)
