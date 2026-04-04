# Guía Técnica: Búsqueda de Intervenciones sobre Aysén en BCN Labor Parlamentaria

## Objetivo
Extraer automáticamente las intervenciones, mociones y proyectos de los parlamentarios de Aysén que mencionan temas relacionados con la región.

## Fuente de Datos
**BCN Labor Parlamentaria**: https://www.bcn.cl/laborparlamentaria/

Este sistema contiene:
- Intervenciones en Sala
- Participaciones en Comisiones
- Mociones presentadas
- Proyectos de Ley
- Oficios de Fiscalización

## Estrategia de Implementación

### Opción 1: Web Scraping con Selenium (Recomendado)

La BCN Labor Parlamentaria es un sitio dinámico que requiere interacción JavaScript, por lo que Selenium es la mejor opción.

#### Instalación
```bash
pip install selenium webdriver-manager beautifulsoup4
```

#### Código de Ejemplo

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def buscar_intervenciones_bcn_real(nombre_parlamentario: str) -> List[Dict]:
    """
    Busca intervenciones en BCN Labor Parlamentaria usando Selenium
    """
    intervenciones = []
    
    # Configurar Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecutar sin ventana
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        # 1. Navegar a BCN Labor Parlamentaria
        url_busqueda = "https://www.bcn.cl/laborparlamentaria/wsgi/consulta/index.py"
        driver.get(url_busqueda)
        
        # 2. Buscar el parlamentario
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "buscar"))
        )
        search_box.send_keys(nombre_parlamentario)
        search_box.submit()
        
        time.sleep(2)  # Esperar resultados
        
        # 3. Hacer clic en el perfil del parlamentario
        # (Necesitas identificar el selector correcto del HTML)
        link_parlamentario = driver.find_element(By.PARTIAL_LINK_TEXT, nombre_parlamentario)
        link_parlamentario.click()
        
        time.sleep(2)
        
        # 4. Navegar a la sección de intervenciones
        # Buscar enlace a "Intervenciones en Sala"
        link_intervenciones = driver.find_element(By.PARTIAL_LINK_TEXT, "Intervenciones")
        link_intervenciones.click()
        
        time.sleep(2)
        
        # 5. Extraer todas las intervenciones
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Buscar elementos que contengan intervenciones
        # (Necesitas analizar la estructura HTML específica)
        items_intervencion = soup.find_all('div', class_='intervencion-item')  # Ejemplo
        
        # 6. Filtrar por keywords de Aysén
        keywords_aysen = ['Aysén', 'Aysen', 'Coyhaique', 'Carretera Austral', 
                         'Patagonia', 'XI Región', 'Baker', 'General Carrera']
        
        for item in items_intervencion:
            texto = item.get_text().lower()
            
            # Si menciona Aysén
            if any(keyword.lower() in texto for keyword in keywords_aysen):
                intervencion = {
                    'fecha': extraer_fecha(item),
                    'tema': extraer_tema(item),
                    'extracto': extraer_extracto(item, keywords_aysen),
                    'url': extraer_url(item)
                }
                intervenciones.append(intervencion)
        
    finally:
        driver.quit()
    
    return intervenciones


def extraer_fecha(item_html):
    """Extrae la fecha de una intervención"""
    # Implementar según estructura HTML
    fecha_elem = item_html.find('span', class_='fecha')
    return fecha_elem.text if fecha_elem else 'Fecha no disponible'


def extraer_tema(item_html):
    """Extrae el tema/título de una intervención"""
    # Implementar según estructura HTML
    tema_elem = item_html.find('h3') or item_html.find('strong')
    return tema_elem.text if tema_elem else 'Sin título'


def extraer_extracto(item_html, keywords):
    """
    Extrae un fragmento relevante que contenga las keywords
    """
    texto_completo = item_html.get_text()
    
    # Buscar la primera keyword que aparece
    for keyword in keywords:
        if keyword.lower() in texto_completo.lower():
            # Extraer contexto alrededor de la keyword (200 caracteres)
            idx = texto_completo.lower().find(keyword.lower())
            inicio = max(0, idx - 100)
            fin = min(len(texto_completo), idx + 100)
            extracto = texto_completo[inicio:fin]
            return f"...{extracto}..."
    
    # Si no se encuentra, retornar primeros 200 caracteres
    return texto_completo[:200] + "..."


def extraer_url(item_html):
    """Extrae el enlace a la intervención completa"""
    link = item_html.find('a', href=True)
    if link:
        href = link['href']
        # Convertir URL relativa a absoluta si es necesario
        if href.startswith('/'):
            return f"https://www.bcn.cl{href}"
        return href
    return None
```

### Opción 2: Análisis Manual del HTML

Si prefieres un enfoque más directo:

1. **Inspeccionar la estructura HTML** de BCN Labor Parlamentaria
   - Abre el perfil de un senador de Aysén
   - Usa DevTools (F12) para identificar:
     - Selectores CSS de intervenciones
     - Formato de fechas
     - Enlaces a documentos completos

2. **Documentar los patrones**
   ```
   Ejemplo de estructura encontrada:
   
   <div class="registro-intervencion">
       <span class="fecha">15-11-2025</span>
       <h4 class="titulo">Proyecto sobre conectividad</h4>
       <p class="extracto">Intervención sobre...</p>
       <a href="/url/completa">Ver más</a>
   </div>
   ```

3. **Adaptar el código** según la estructura real

### Opción 3: API Alternativa (Si Existe)

Revisar si BCN tiene API documentada:
- https://www.bcn.cl/laborparlamentaria/inicio
- Buscar documentación técnica o contactar a BCN

## Palabras Clave para Filtrar

```python
KEYWORDS_AYSEN_COMPLETAS = {
    # Lugares
    'geograficos': [
        'Aysén', 'Aysen', 'Región de Aysén', 'XI Región',
        'Coyhaique', 'Puerto Aysén', 'Puerto Aysen',
        'Chile Chico', 'Cochrane', 'Puerto Cisnes',
        'Lago Verde', 'Río Ibáñez', 'Tortel',
        'Villa O\'Higgins', 'Puerto Guadal', 'Bahía Murta'
    ],
    
    # Infraestructura
    'infraestructura': [
        'Carretera Austral', 'Ruta 7', 'Aeropuerto Balmaceda',
        'Puerto Chacabuco', 'Camino Longitudinal Austral'
    ],
    
    # Naturaleza/Conservación
    'naturaleza': [
        'Parque Nacional Laguna San Rafael',
        'Reserva Nacional Cerro Castillo',
        'Reserva Nacional Lago Jeinimeni',
        'Glaciar San Rafael', 'Campos de Hielo',
        'Patagonia chilena', 'Patagonia Norte'
    ],
    
    # Economía Regional
    'economia': [
        'salmonicultura Aysén', 'pesca artesanal Aysén',
        'turismo Patagonia', 'ganadería ovina'
    ],
    
    # Proyectos Específicos
    'proyectos': [
        'Hidroaysén', 'Baker', 'Pascua',
        'represas Patagonia'
    ]
}
```

## Procesamiento de Resultados

Una vez extraídas las intervenciones:

1. **Deduplicación**: Eliminar intervenciones repetidas
2. **Ranking por relevancia**: Priorizar las que mencionan múltiples keywords
3. **Clasificación temática**: Categorizar por tipo (infraestructura, medioambiente, economía, etc.)
4. **Extracción de fechas**: Ordenar cronológicamente

```python
def procesar_intervenciones(intervenciones_raw: List[Dict]) -> List[Dict]:
    """
    Procesa y enriquece las intervenciones extraídas
    """
    procesadas = []
    
    for interv in intervenciones_raw:
        # Calcular score de relevancia
        score = calcular_relevancia(interv['extracto'])
        
        # Clasificar temática
        categoria = clasificar_tematica(interv['tema'], interv['extracto'])
        
        procesada = {
            **interv,
            'relevancia_score': score,
            'categoria': categoria
        }
        procesadas.append(procesada)
    
    # Ordenar por relevancia y fecha
    procesadas.sort(key=lambda x: (x['relevancia_score'], x['fecha']), reverse=True)
    
    return procesadas


def calcular_relevancia(texto: str) -> int:
    """
    Calcula score de relevancia basado en keywords mencionadas
    """
    score = 0
    texto_lower = texto.lower()
    
    for categoria, keywords in KEYWORDS_AYSEN_COMPLETAS.items():
        for keyword in keywords:
            if keyword.lower() in texto_lower:
                score += 1
    
    return score


def clasificar_tematica(tema: str, extracto: str) -> str:
    """
    Clasifica la intervención por temática
    """
    texto = f"{tema} {extracto}".lower()
    
    if any(k in texto for k in ['carretera', 'ruta', 'infraestructura', 'camino']):
        return 'Infraestructura'
    elif any(k in texto for k in ['parque', 'conservación', 'glaciar', 'reserva']):
        return 'Medioambiente'
    elif any(k in texto for k in ['salmonicultura', 'pesca', 'turismo', 'economía']):
        return 'Economía'
    elif any(k in texto for k in ['salud', 'hospital', 'consultorio']):
        return 'Salud'
    elif any(k in texto for k in ['educación', 'escuela', 'universidad']):
        return 'Educación'
    else:
        return 'Otros'
```

## Automatización

Para mantener los datos actualizados:

1. **Configurar cron job** (Linux/Mac) o **Task Scheduler** (Windows)
2. **Ejecutar semanalmente**:
   ```bash
   0 8 * * 1 /usr/bin/python3 /ruta/obtener_datos_congreso.py
   ```

3. **Notificaciones**: Enviar email cuando se detecten nuevas intervenciones

## Consideraciones Éticas y Legales

- ✅ Los datos de BCN son públicos
- ✅ El web scraping respetuoso (delays, user-agent) es legal
- ✅ Atribuir fuente correctamente
- ⚠️ No sobrecargar el servidor (rate limiting)
- ⚠️ Revisar términos de servicio de BCN

## Próximos Pasos

1. Inspeccionar HTML real de BCN Labor Parlamentaria
2. Adaptar selectores CSS en el código
3. Probar con un parlamentario
4. Escalar a todos los parlamentarios de Aysén
5. Integrar con el sitio web

## Recursos

- **BCN Labor Parlamentaria**: https://www.bcn.cl/laborparlamentaria/
- **Selenium Docs**: https://selenium-python.readthedocs.io/
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Chrome DevTools**: F12 en navegador
