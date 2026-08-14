# 📖 Guía Completa de Instalación de HyperOS v1.0.0

## Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Descarga de la ISO](#descarga-de-la-iso)
3. [Preparación del Medio de Instalación](#preparación-del-medio-de-instalación)
4. [Arranque desde USB](#arranque-desde-usb)
5. [Instalación Gráfica Paso a Paso](#instalación-gráfica-paso-a-paso)
6. [Post-Instalación](#post-instalación)
7. [Solución de Problemas](#solución-de-problemas)

---

## Requisitos Previos

### Hardware Mínimo

| Componente | Requisito Mínimo | Recomendado |
|------------|------------------|-------------|
| **CPU** | Dual-core 64-bit | Quad-core moderno |
| **RAM** | 4 GB | 8 GB o más |
| **Almacenamiento** | 20 GB | 60 GB SSD |
| **GPU** | Compatible con Wayland | Intel/AMD/NVIDIA reciente |
| **Resolución** | 1280x720 | 1920x1080 |
| **Conexión** | Opcional | Internet recomendado |

### Hardware Verificado

✅ **Procesadores**
- Intel: 8va generación o superior
- AMD: Ryzen 2000 o superior

✅ **Tarjetas Gráficas**
- Intel: UHD Graphics, Iris Xe
- AMD: Radeon RX, Vega, RDNA
- NVIDIA: GTX 10xx, RTX 20xx/30xx/40xx (driver propietario)

✅ **Red**
- WiFi: Intel AX200/AX210, Atheros, algunos Realtek
- Ethernet: La mayoría de controladores integrados

---

## Descarga de la ISO

### Opción 1: Sitio Web Oficial
Visitar https://hyperos.org/download

### Opción 2: Terminal
```bash
wget https://github.com/hyperos/hyperos/releases/download/v1.0.0/HyperOS-1.0.0-x86_64.iso
```

### Opción 3: Torrent
```bash
wget https://github.com/hyperos/hyperos/releases/download/v1.0.0/HyperOS-1.0.0-x86_64.iso.torrent
```

### Verificación de Integridad
```bash
sha256sum HyperOS-1.0.0-x86_64.iso
# Comparar con hash oficial en releases
```

---

## Preparación del Medio de Instalación

### Método 1: dd (Linux/macOS)
```bash
sudo dd if=HyperOS-1.0.0-x86_64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

### Método 2: balenaEtcher (GUI)
1. Descargar desde https://balena.io/etcher
2. Seleccionar ISO y USB
3. Click en "Flash!"

### Método 3: Rufus (Windows)
1. Descargar desde https://rufus.ie
2. Configurar GPT para UEFI
3. Grabar ISO

---

## Arranque desde USB

1. Reiniciar computadora
2. Presionar F2/F12/Del para entrar a BIOS
3. Deshabilitar Secure Boot temporalmente
4. Cambiar boot order para priorizar USB
5. Guardar cambios y reiniciar
6. Seleccionar "Try or Install HyperOS"

---

## Instalación Gráfica Paso a Paso

### Paso 1: Bienvenida
- Click en "Comenzar"

### Paso 2: Verificación de Requisitos
- El sistema verifica automáticamente espacio, RAM, energía
- Click en "Continuar"

### Paso 3: Configuración Regional
- Idioma: Español (u otro)
- Teclado: Spanish
- Zona horaria: Europe/Madrid
- Click en "Continuar"

### Paso 4: Particionado
**Opción A: Automático (Recomendado)**
- Crea automáticamente: EFI (512MB), Root (Btrfs), Home (Btrfs), Swap
- ⚠️ Borra TODO el disco seleccionado
- Marcar checkbox de confirmación
- Click en "Continuar"

**Opción B: Manual**
- Crear particiones personalizadas
- Esquema recomendado:
  - /boot/efi: 512MB FAT32
  - /: 50-100GB Btrfs
  - /home: Restante Btrfs
  - swap: 4-16GB

### Paso 5: Usuario
- Nombre completo
- Nombre de usuario
- Contraseña (mínimo 8 caracteres)
- ☑ Iniciar sesión automáticamente
- ☑ Hacerme administrador (sudo)
- Click en "Continuar"

### Paso 6: Resumen e Instalación
- Revisar configuración
- Click en "INSTALAR AHORA"
- Esperar 5-15 minutos según hardware

### Paso 7: Completado
- Click en "Reiniciar"
- Retirar USB cuando se solicite
- ¡Listo!

---

## Post-Instalación

### Primeras Tareas Recomendadas

1. **Actualizar sistema**
```bash
sudo pacman -Syu
```

2. **Instalar drivers propietarios (si es necesario)**
```bash
hyper-drivers
```

3. **Configurar backups**
```bash
hyper-backup
```

4. **Personalizar escritorio**
```bash
hyper-settings
```

### Comandos Útiles

```bash
# Verificar estado del sistema
hyper diagnose --full

# Ver logs
journalctl -b

# Gestionar servicios
systemctl --user status
```

---

## Solución de Problemas

### No arranca desde USB
- Verificar que USB esté bien grabado
- Probar otro puerto USB
- Deshabilitar Secure Boot en BIOS
- Verificar modo UEFI/Legacy

### Error de particionado
- Asegurar disco no está montado
- Verificar tabla de particiones existente
- Usar opción manual si hay problemas

### Sin conexión a internet
- Verificar drivers WiFi
- Probar conexión por cable
- Reiniciar NetworkManager

### Pantalla negra después de instalar
- Probar modo seguro en bootloader
- Verificar drivers GPU
- Revisar logs con Ctrl+Alt+F2

---

**Soporte**: https://github.com/hyperos/hyperos/issues
**Comunidad**: https://discord.gg/hyperos
