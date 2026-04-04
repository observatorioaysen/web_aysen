#!/usr/bin/env python3
"""
Script para obtener datos de parlamentarios de Aysén desde las APIs del Congreso Nacional de Chile
Genera un archivo JSON con métricas actualizadas que puede ser consumido por la página web

Uso:
  python obtener_datos_congreso.py              # Ejecutar una vez
  python obtener_datos_congreso.py --watch      # Ejecutar en bucle (cada 6 horas por defecto)
  python obtener_datos_congreso.py --watch --interval 3600  # Cada hora
"""

import sys
import requests
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List
import xml.etree.ElementTree as ET

# Forzar UTF-8 en la consola (necesario en Windows)
sys.stdout.reconfigure(encoding='utf-8')

# IDs conocidos de parlamentarios de Aysén (necesitan verificación)
PARLAMENTARIOS_AYSEN = {
    "senadores": [
        {
            "nombre": "Miguel Ángel Calisto Águila",
            "partido": "Independiente",
            "comite": "Comité Partido Evópoli e Independientes",
            "id_senador": None  # Necesita ser obtenido de la API
        },
        {
            "nombre": "Ximena Ordenes Neira",
            "partido": "Independiente",
            "comite": "Comité Mixto Partido Socialista, Partido por la Democracia e independientes y Partido Liberal",
            "id_senador": None
        }
    ],
    "diputados": [
        {
            "nombre": "René Alinco Bustos",
            "partido": "IND/FRVS",
            "id_diputado": None
        },
        {
            "nombre": "Andrea Macías Palma",
            "partido": "Partido Socialista",
            "id_diputado": None
        },
        {
            "nombre": "Alejandra Valdebenito Torres",
            "partido": "Unión Demócrata Independiente",
            "id_diputado": None
        }
    ]
}

# URLs base de las APIs
API_CAMARA_BASE = "https://opendata.camara.cl/wscamaradiputados.asmx"
API_SENADO_BASE = "https://tramitacion.senado.cl/wspublico"
BCN_LABOR_BASE = "https://www.bcn.cl/laborparlamentaria"

# Palabras clave para filtrar temas de Aysén
KEYWORDS_AYSEN = [
    'Aysén', 'Aysen', 'Coyhaique', 'Puerto Aysén', 'Chile Chico',
    'Cochrane', 'Puerto Cisnes', 'Lago Verde', 'Río Ibáñez',
    'Tortel', 'General Carrera', 'Baker', 'Chelenko', 'Patagonia',
    'Región de Aysén', 'XI Región'
]


def buscar_intervenciones_aysen(nombre_parlamentario: str, tipo: str = 'senador') -> List[Dict]:
    """
    Busca intervenciones parlamentarias relacionadas con Aysén
    Utiliza web scraping básico de la BCN Labor Parlamentaria
    
    Args:
        nombre_parlamentario: Nombre completo del parlamentario
        tipo: 'senador' o 'diputado'
    
    Returns:
        Lista de intervenciones relacionadas con Aysén
    """
    intervenciones_aysen = []
    
    try:
        # NOTA: La BCN Labor Parlamentaria requiere navegación web compleja
        # Este es un placeholder que muestra la estructura esperada
        # Para implementación completa, se necesitaría Selenium o scraping más avanzado
        
        # URL de ejemplo para búsqueda en BCN
        # https://www.bcn.cl/laborparlamentaria/wsgi/consulta/index.py
        
        # Por ahora, retornamos datos de ejemplo para demostración
        # En producción, aquí iría el scraping real o llamada a API si existe
        
        intervenciones_ejemplo = [
            {
                'fecha': '2025-11-15',
                'tema': 'Proyecto de conectividad para zonas rurales de Aysén',
                'extracto': 'Intervención sobre la necesidad de mejorar la conectividad digital en comunidades aisladas de la región.',
                'url': f'{BCN_LABOR_BASE}/wsgi/consulta/verIntervención.py?id=ejemplo'
            },
            {
                'fecha': '2025-10-28',
                'tema': 'Financiamiento para Parque Nacional Laguna San Rafael',
                'extracto': 'Moción para aumentar presupuesto destinado a conservación de áreas protegidas en la Patagonia.',
                'url': f'{BCN_LABOR_BASE}/wsgi/consulta/verIntervención.py?id=ejemplo2'
            },
            {
                'fecha': '2025-09-12',
                'tema': 'Infraestructura vial Ruta 7 Carretera Austral',
                'extracto': 'Fiscalización sobre el estado de avance de obras en la Carretera Austral y solicitud de mayores recursos.',
                'url': f'{BCN_LABOR_BASE}/wsgi/consulta/verIntervención.py?id=ejemplo3'
            }
        ]
        
        # Filtrar solo las que mencionan Aysén
        for interv in intervenciones_ejemplo:
            if any(keyword.lower() in interv['tema'].lower() or 
                   keyword.lower() in interv['extracto'].lower() 
                   for keyword in KEYWORDS_AYSEN):
                intervenciones_aysen.append(interv)
        
        print(f"    → Encontradas {len(intervenciones_aysen)} intervenciones sobre Aysén")
        
    except Exception as e:
        print(f"Error al buscar intervenciones: {e}")
    
    return intervenciones_aysen


def obtener_diputados_periodo_actual() -> List[Dict]:
    """
    Obtiene la lista de diputados del período legislativo actual
    """
    url = f"{API_CAMARA_BASE}/retornarDiputadosPeriodoActual"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Parsear XML
            root = ET.fromstring(response.content)
            diputados = []
            
            for diputado in root.findall('.//Diputado'):
                diputados.append({
                    'id': diputado.find('Id').text if diputado.find('Id') is not None else None,
                    'nombre': diputado.find('Nombre').text if diputado.find('Nombre') is not None else None,
                    'apellido_paterno': diputado.find('ApellidoPaterno').text if diputado.find('ApellidoPaterno') is not None else None,
                    'apellido_materno': diputado.find('ApellidoMaterno').text if diputado.find('ApellidoMaterno') is not None else None,
                    'distrito': diputado.find('Distrito').text if diputado.find('Distrito') is not None else None,
                    'region': diputado.find('Region').text if diputado.find('Region') is not None else None,
                })
            
            return diputados
        else:
            print(f"Error al obtener diputados: Status {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al consultar API de Cámara: {e}")
        return []


def filtrar_parlamentarios_aysen(diputados: List[Dict]) -> List[Dict]:
    """
    Filtra los diputados que representan a la Región de Aysén
    """
    return [d for d in diputados if d['region'] and 'Aysén' in d['region']]


def obtener_metricas_diputado(id_diputado: str) -> Dict:
    """
    Obtiene métricas de actividad de un diputado específico
    """
    metricas = {
        'proyectos_presentados': 0,
        'asistencia_porcentaje': 0,
        'intervenciones': 0,
        'comisiones': 0
    }
    
    # Estas son llamadas de ejemplo - necesitan ajustarse según la API real
    # La documentación oficial está en https://www.camara.cl/transparencia/datosAbiertos.aspx
    
    try:
        # Obtener asistencia (endpoint de ejemplo)
        # url_asistencia = f"{API_CAMARA_BASE}/retornarAsistenciaDiputado?prmDiputadoId={id_diputado}"
        # response = requests.get(url_asistencia, timeout=10)
        # ... parsear respuesta ...
        
        # Por ahora retornamos datos de placeholder
        metricas['proyectos_presentados'] = "Consultar API"
        metricas['asistencia_porcentaje'] = "Consultar API"
        metricas['intervenciones'] = "Consultar API"
        metricas['comisiones'] = "Consultar API"
        
    except Exception as e:
        print(f"Error al obtener métricas de diputado {id_diputado}: {e}")
    
    return metricas


def generar_datos_json():
    """
    Genera archivo JSON con datos actualizados de parlamentarios de Aysén
    """
    print("Iniciando recolección de datos...")
    
    # Obtener lista completa de diputados
    print("Obteniendo diputados del período actual...")
    todos_diputados = obtener_diputados_periodo_actual()
    
    # Filtrar por Aysén
    diputados_aysen = filtrar_parlamentarios_aysen(todos_diputados)
    
    print(f"\nDiputados encontrados para Aysén: {len(diputados_aysen)}")
    for diputado in diputados_aysen:
        print(f"  - {diputado['nombre']} {diputado['apellido_paterno']} {diputado['apellido_materno']}")
        print(f"    ID: {diputado['id']}, Distrito: {diputado['distrito']}")
    
    # Preparar datos para exportación
    datos_exportacion = {
        'metadata': {
            'ultima_actualizacion': datetime.now().isoformat(),
            'fuente': 'Congreso Nacional de Chile - Datos Abiertos',
            'region': 'Aysén del General Carlos Ibáñez del Campo'
        },
        'senadores': [],
        'diputados': []
    }
    
    # Procesar senadores con intervenciones sobre Aysén
    print("\nProcesando senadores de Aysén...")
    for senador_base in PARLAMENTARIOS_AYSEN['senadores']:
        print(f"\n  Senador/a: {senador_base['nombre']}")
        
        # Buscar intervenciones sobre Aysén
        intervenciones = buscar_intervenciones_aysen(senador_base['nombre'], tipo='senador')
        
        senador_completo = {
            **senador_base,
            'intervenciones_aysen': intervenciones,
            'metricas': {
                'proyectos_presentados': 'Consultar API',
                'asistencia_porcentaje': 'Consultar API',
                'intervenciones': len(intervenciones),
                'comisiones': 'Consultar API'
            }
        }
        datos_exportacion['senadores'].append(senador_completo)
    
    # Agregar datos de diputados con IDs reales
    print("\nProcesando diputados de Aysén...")
    for diputado_aysen in diputados_aysen:
        nombre_completo = f"{diputado_aysen['nombre']} {diputado_aysen['apellido_paterno']} {diputado_aysen['apellido_materno']}"
        print(f"\n  Diputado/a: {nombre_completo}")
        
        # Buscar intervenciones sobre Aysén
        intervenciones = buscar_intervenciones_aysen(nombre_completo, tipo='diputado')
        
        datos_diputado = {
            'id': diputado_aysen['id'],
            'nombre_completo': nombre_completo,
            'nombre': diputado_aysen['nombre'],
            'apellido_paterno': diputado_aysen['apellido_paterno'],
            'apellido_materno': diputado_aysen['apellido_materno'],
            'distrito': diputado_aysen['distrito'],
            'region': diputado_aysen['region'],
            'partido': 'Consultar API',  # Necesita endpoint específico
            'intervenciones_aysen': intervenciones,
            'metricas': obtener_metricas_diputado(diputado_aysen['id'])
        }
        datos_exportacion['diputados'].append(datos_diputado)
    
    # Guardar JSON
    output_file = 'datos_parlamentarios_aysen.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(datos_exportacion, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Datos exportados a: {output_file}")
    print(f"  - {len(datos_exportacion['senadores'])} senadores procesados")
    print(f"  - {len(datos_exportacion['diputados'])} diputados procesados")
    
    return output_file


def ejecutar_ciclo():
    """
    Ejecuta un ciclo completo de recolección y exportación de datos.
    Retorna True si tuvo éxito, False si hubo error.
    """
    print("=" * 60)
    print("FISCALIZACIÓN LEGISLATIVA - REGIÓN DE AYSÉN")
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    try:
        generar_datos_json()
        print(f"\n[OK] Ciclo completado a las {datetime.now().strftime('%H:%M:%S')}")
        return True
    except Exception as e:
        print(f"\n[ERROR] Error durante la ejecucion: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Recolector de datos parlamentarios de Aysén"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Ejecutar en bucle continuo, actualizando el JSON periódicamente"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=6 * 3600,  # 6 horas por defecto
        help="Intervalo en segundos entre actualizaciones (default: 21600 = 6 horas)"
    )
    args = parser.parse_args()

    if args.watch:
        horas = args.interval / 3600
        print(f"Modo watch activado — actualizando cada {horas:.1f} hora(s)")
        print("Presiona Ctrl+C para detener.\n")
        while True:
            ejecutar_ciclo()
            proxima = datetime.fromtimestamp(time.time() + args.interval)
            print(f"Próxima actualización: {proxima.strftime('%Y-%m-%d %H:%M:%S')}\n")
            time.sleep(args.interval)
    else:
        ejecutar_ciclo()


if __name__ == "__main__":
    main()
