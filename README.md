# Fiscalización Legislativa - Región de Aysén

Sistema web para monitorear la actividad legislativa de los parlamentarios que representan a la Región de Aysén del General Carlos Ibáñez del Campo.

## 📊 Parlamentarios Monitoreados

### Senadores (Circunscripción 14)
- **Miguel Ángel Calisto Águila** - Independiente
- **Ximena Ordenes Neira** - Independiente

### Diputados (Distrito 27)
- **René Alinco Bustos** - IND/FRVS
- **Andrea Macías Palma** - Partido Socialista
- **Alejandra Valdebenito Torres** - Unión Demócrata Independiente

## 🎯 Métricas Monitoreadas

Para cada parlamentario se muestra:
- ✅ Proyectos de ley presentados
- 📊 Asistencia a sesiones de sala
- 🎤 Intervenciones en sala
- 👥 Participación en comisiones

## 🚀 Despliegue Rápido (GitHub Pages)

### Opción 1: Solo HTML (sin API real)
La forma más simple para tener el sitio funcionando en minutos:

1. **Crear repositorio en GitHub:**
   ```bash
   git init fiscalizacion-aysen
   cd fiscalizacion-aysen
   ```

2. **Copiar el archivo HTML:**
   - Copia `fiscalizacion-aysen.html` y renómbralo a `index.html`

3. **Subir a GitHub:**
   ```bash
   git add index.html
   git commit -m "Sitio inicial de fiscalización legislativa"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/fiscalizacion-aysen.git
   git push -u origin main
   ```

4. **Activar GitHub Pages:**
   - Ve a Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`
   - Save

Tu sitio estará en: `https://TU_USUARIO.github.io/fiscalizacion-aysen/`

### Opción 2: Con datos reales de la API

Para obtener datos reales del Congreso Nacional:

1. **Instalar dependencias Python:**
   ```bash
   pip install requests
   ```

2. **Ejecutar el script de recolección:**
   ```bash
   python3 obtener_datos_congreso.py
   ```

3. **Integrar datos en la web:**
   - El script genera `datos_parlamentarios_aysen.json`
   - Modifica `index.html` para cargar este JSON
   - Configura GitHub Actions para actualización automática

## 🔧 Configuración Avanzada

### Actualización Automática con GitHub Actions

Crea `.github/workflows/actualizar-datos.yml`:

```yaml
name: Actualizar Datos Parlamentarios

on:
  schedule:
    - cron: '0 8 * * *'  # Diariamente a las 8 AM
  workflow_dispatch:  # Permite ejecución manual

jobs:
  actualizar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Instalar dependencias
        run: pip install requests
      
      - name: Obtener datos del Congreso
        run: python obtener_datos_congreso.py
      
      - name: Commit y push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add datos_parlamentarios_aysen.json
          git commit -m "Actualización automática de datos" || exit 0
          git push
```

## 📡 Fuentes de Datos

El sistema utiliza las siguientes fuentes oficiales:

- **API Cámara de Diputados**: https://www.camara.cl/transparencia/datosAbiertos.aspx
- **Datos Abiertos Congreso**: https://opendata.congreso.cl
- **Biblioteca del Congreso Nacional**: https://www.bcn.cl/laborparlamentaria

### Endpoints Principales

#### Cámara de Diputados
```
Base: https://opendata.camara.cl/wscamaradiputados.asmx

- /retornarDiputadosPeriodoActual
- /retornarDetalleDiputado?prmDiputadoId={ID}
- /retornarAsistenciaDiputado?prmDiputadoId={ID}
- /retornarMocionesXAnho?prmAnho={AÑO}
```

#### Senado
```
Base: https://tramitacion.senado.cl/wspublico

- Consultar documentación en senado.cl/datos-abiertos
```

## 🛠️ Personalización

### Modificar Diseño

El CSS está inline en `index.html`. Variables principales:

```css
/* Colores */
--color-primary: #1565c0;
--color-senado: #e3f2fd;
--color-camara: #f3e5f5;

/* Tipografía */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
```

### Agregar Métricas

Para agregar nuevas métricas, edita la sección `.stats` en el HTML y actualiza el script Python para obtener los datos correspondientes.

## 📋 Roadmap

- [x] Prototipo funcional con diseño limpio
- [x] Script Python para APIs del Congreso
- [ ] Integración completa con APIs
- [ ] Gráficos de tendencias temporales
- [ ] Sistema de alertas para nueva actividad
- [ ] Comparación con promedios nacionales
- [ ] Exportación de reportes en PDF
- [ ] API propia para otros desarrolladores

## 🤝 Contribuciones

Este es un proyecto de transparencia ciudadana. Las contribuciones son bienvenidas:

1. Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-metrica`)
3. Commit de cambios (`git commit -m 'Agregar nueva métrica'`)
4. Push a la rama (`git push origin feature/nueva-metrica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de dominio público y está dedicado al bien común. Puedes usarlo, modificarlo y distribuirlo libremente.

## 📧 Contacto

Para sugerencias o reportar errores, abre un issue en el repositorio.

---

**Nota**: Este es un proyecto ciudadano independiente, no afiliado al Congreso Nacional de Chile. Los datos se obtienen de fuentes públicas oficiales.

## 🎓 Recursos Adicionales

### Aprender más sobre el Proceso Legislativo
- [Formación de la Ley en Chile](https://www.bcn.cl/formacionleyes)
- [Funciones del Congreso](https://www.senado.cl/acerca-del-senado)

### Otras Plataformas de Fiscalización
- [Ciudadano Inteligente](https://ciudadanointeligente.org/)
- [Vota Inteligente](https://votainteligente.cl/)

### APIs y Datos Abiertos
- [Portal de Datos Abiertos del Estado](https://datos.gob.cl/)
- [Documentación API Cámara](https://www.camara.cl/transparencia/datosAbiertos.aspx)
