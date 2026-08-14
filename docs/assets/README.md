# 📸 Assets de HyperOS

Este directorio contiene las imágenes y recursos visuales para la documentación de HyperOS.

## Imágenes Requeridas

Para una documentación completa, se deben agregar las siguientes imágenes:

### Capturas de Pantalla Principales

1. **banner.png** (1200x400px)
   - Banner principal con logo de HyperOS
   - Usado en: README.md, sitio web, releases

2. **desktop-screenshot.png** (1920x1080px)
   - Escritorio completo de HyperOS
   - Debe mostrar: Hyprland, Waybar, Hyper Center, terminal
   - Resolución recomendada: 1920x1080 o superior

3. **hyper-center.png** (800x600px)
   - Ventana de Hyper Center mostrando métricas
   - Debe mostrar: CPU, RAM, Disk, GPU, Battery

4. **installer-screenshot.png** (1024x768px)
   - Asistente de instalación en paso de particionado
   - Debe mostrar: diálogo de confirmación, progreso

5. **store-screenshot.png** (1024x768px)
   - Hyper Store con lista de aplicaciones
   - Debe mostrar: categorías, búsqueda, botones de instalar

6. **settings-screenshot.png** (1024x768px)
   - Hyper Settings con panel de configuración
   - Debe mostrar: múltiples secciones de configuración

### Diagramas y Gráficos

7. **architecture-diagram.png** (1200x800px)
   - Diagrama de arquitectura del sistema
   - Mostrar capas: Apps → Core → Daemon → System

8. **installation-flow.png** (800x600px)
   - Flujo del proceso de instalación
   - Diagrama de secuencia

9. **performance-chart.png** (800x400px)
   - Gráfico comparativo de rendimiento
   - Comparar con Ubuntu, Fedora, Arch, openSUSE

### Iconos y Logos

10. **logo.svg** (vectorial)
    - Logo oficial de HyperOS en SVG
    - Versiones: color, blanco, negro

11. **icon-512.png** (512x512px)
    - Icono de aplicación
    - Para launcher, dock, menú

12. **icon-256.png** (256x256px)
    - Versión reducida del icono

13. **icon-128.png** (128x128px)
    - Versión pequeña para notificaciones

### Fondos de Pantalla

14. **wallpaper-default.png** (3840x2160px)
    - Fondo predeterminado de HyperOS
    - Tema Catppuccin, diseño abstracto

15. **wallpaper-dark.png** (3840x2160px)
    - Variante oscura del fondo

16. **wallpaper-light.png** (3840x2160px)
    - Variante clara del fondo

## Cómo Contribuir con Imágenes

### Requisitos Técnicos

- **Formato**: PNG para capturas, SVG para logos/iconos
- **Compresión**: Optimizar con `pngquant` o `optipng`
- ** DPI**: 72 DPI para web, 300 DPI para impresión
- **Espacio de color**: sRGB

### Proceso

1. Capturar pantalla con `grim` (Wayland) o `scrot` (X11)
2. Editar con GIMP, Krita o Figma
3. Exportar en formato requerido
4. Optimizar tamaño:
   ```bash
   pngquant --quality=65-80 imagen.png
   optipng -o7 imagen.png
   ```
5. Agregar al repositorio con commit descriptivo

### Herramientas Recomendadas

```bash
# Captura de pantalla en Wayland
grim -g "$(slurp)" captura.png

# Optimización de imágenes
sudo pacman -S pngquant optipng

# Creación de diagramas
sudo pacman -S drawio-desktop
# O usar: https://app.diagrams.net
```

## Licencia de Assets

Todos los assets visuales están licenciados bajo:
- **Logos e iconos**: CC BY-SA 4.0
- **Capturas de pantalla**: CC0 (dominio público)
- **Fondos de pantalla**: CC BY-SA 4.0

---

**Nota**: Las imágenes marcadas como "placeholder" en la documentación serán reemplazadas con capturas reales antes del lanzamiento final v1.0.0.
