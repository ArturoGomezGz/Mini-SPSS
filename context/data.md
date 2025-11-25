# Análisis del Archivo datos.sav

## Resumen Ejecutivo

Este documento presenta un análisis exhaustivo del archivo `datos.sav`, que contiene datos de una encuesta ciudadana realizada en el Área Metropolitana de Guadalajara (AMG). El análisis fue realizado el 25 de noviembre de 2025.

---

## 1. Estructura General del Archivo

### Dimensiones
- **Total de casos (filas)**: 2,418 encuestados
- **Total de variables (columnas)**: 265 variables
- **Formato**: Archivo SPSS (.sav)

### Información Básica
El archivo contiene una base de datos estructurada con:
- Identificadores únicos de sujetos
- Metadatos temporales (fecha y duración)
- 262 variables de contenido relacionadas con la encuesta
- Variables derivadas de clasificación sociodemográfica

---

## 2. Tipo de Datos

### Naturaleza de la Encuesta
Este archivo contiene datos de una **encuesta de opinión ciudadana** que aborda múltiples dimensiones de la vida urbana y la percepción ciudadana en el AMG.

### Categorías Temáticas Principales

#### A. Calidad de Vida y Satisfacción (Q_1 - Q_11)
- Evaluación de calidad de vida general
- Satisfacción con diversos servicios urbanos
- Percepción sobre la situación actual de la ciudad

#### B. Servicios Públicos (T_Q_12_1 - T_Q_13_6)
Evaluación de servicios como:
- Alumbrado público
- Pavimentación
- Recolección de basura
- Transporte público
- Seguridad pública
- Servicios de agua

#### C. Gobierno y Administración Pública (Q_14 - Q_22)
- Evaluación del desempeño gubernamental
- Percepción de transparencia
- Confianza en autoridades locales
- Conocimiento de programas municipales

#### D. Movilidad y Transporte (Q_23_O1 - Q_32)
- Modos de transporte utilizados
- Frecuencia de uso
- Tiempos de traslado
- Evaluación de infraestructura vial
- Problemas de tráfico

#### E. Infraestructura Urbana (Q_33 - Q_43)
- Espacios públicos (parques, bibliotecas, centros deportivos)
- Accesibilidad
- Satisfacción con infraestructura comunitaria
- Frecuencia de uso de espacios públicos

#### F. Seguridad Vial (Q_44 - Q_48)
- Uso de cinturón de seguridad
- Comportamientos de riesgo al conducir
- Percepción de seguridad vial
- Principales causas de accidentes

#### G. Seguridad Pública y Delincuencia (Q_49 - Q_55)
- Percepción de seguridad en el hogar y la colonia
- Victimización (experiencia con delitos)
- Tipos de delitos experimentados
- Denuncia de delitos
- Razones para no denunciar

#### H. Violencia y Convivencia (Q_56 - Q_66)
- Experiencia con violencia doméstica
- Agresiones en diferentes contextos
- Satisfacción con relaciones interpersonales
- Conflictos vecinales
- Discriminación

#### I. Participación Ciudadana (Q_67_O1 - Q_68_4)
- Formas de participación política
- Activismo ciudadano
- Uso de redes sociales para participación
- Actitudes hacia la participación comunitaria

#### J. Medios de Comunicación y Democracia (Q_69 - Q_73)
- Fuentes de información
- Consumo de medios
- Actitudes hacia la democracia
- Confianza en instituciones (gobierno, policía, medios, etc.)
- Percepción sobre derechos y libertades

#### K. Datos Sociodemográficos (Q_74 - Q_94)
Variables de caracterización del encuestado:

**Personales:**
- Género (Q_74)
- Edad (Q_75)
- Nivel educativo (Q_76)
- Estado civil (Q_77)
- Ocupación (Q_79)

**Socioeconómicas:**
- Clase social autopercibida (Q_78)
- Nivel socioeconómico (NSE2024)
- Características del hogar (número de focos, baños, personas)
- Tenencia de la vivienda (Q_90)
- Posesión de bienes (T_Q_80_1 - T_Q_83_2)

**Geográficas:**
- Municipio de residencia (Q_94)

**Variables de Hogar:**
- Responsable de las labores del hogar (Q_81)
- Escolaridad del responsable del hogar (Q_82)
- Número de habitaciones (Q_85)
- Número de baños (Q_87)
- Número de personas en el hogar (Q_89)
- Ingreso del hogar (Q_91)

#### L. Variables Derivadas y de Clasificación
- **SEXO**: Género categorizado
- **CALIDAD_VIDA**: Índice de calidad de vida categorizado
- **EDAD**: Grupos de edad (18-29, 30-44, 45-59, 60+)
- **ESC**: Nivel educativo categorizado
- **NSE2024**: Nivel socioeconómico detallado (E, D, D+, C-, C, C+, A/B)
- **NSE2024_C**: Nivel socioeconómico consolidado
- **FACTOR**: Factor de ponderación para análisis estadístico

---

## 3. Características de las Variables

### Sistema de Codificación

La mayoría de las variables utilizan un sistema de codificación numérica donde:
- **Valores positivos (1-18)**: Respuestas específicas de la encuesta
- **-1**: "No aplica (en blanco por filtro)" - pregunta filtrada que no corresponde al encuestado
- **-2**: "No sabe / No contestó" - respuesta faltante o desconocida

### Tipos de Variables

#### Variables Numéricas Continuas
- `SbjNum`: Número de identificación del sujeto
- `Date`: Fecha de la encuesta (formato timestamp)
- `Duration`: Duración de la encuesta
- `Q_75`: Edad en años
- `Q_85`: Número de habitaciones
- `Q_87`: Número de baños
- `Q_89`: Número de personas en el hogar
- `FACTOR`: Factor de expansión

#### Variables Categóricas Ordinales
La mayoría de las preguntas de la encuesta usan escalas ordinales:

**Escala de Satisfacción (1-6):**
1. Nada satisfecha(o)
2. Poco satisfecha(o)
3. Ni satisfecha(o), ni insatisfecha(o)
4. Algo satisfecha(o)
5. Muy satisfecha(o)
6. No sabe/No contestó

**Escala de Frecuencia (1-6):**
1. Nunca
2. Pocas veces
3. A veces sí y a veces no
4. La mayoría de las veces
5. Siempre
6. No sabe/No contestó

**Escala de Acuerdo (1-6):**
1. Muy en desacuerdo
2. En desacuerdo
3. Ni de acuerdo, ni en desacuerdo
4. De acuerdo
5. Muy de acuerdo
6. No sabe/No contestó

**Escala de Confianza (1-7):**
1. Nada
2. Poco
3. Ni confío ni desconfío
4. Algo
5. Mucha
6. No contestó
7. No sabría opinar

#### Variables Categóricas Nominales
Variables sin orden jerárquico:
- Municipio de residencia (6 opciones)
- Tipo de transporte utilizado
- Tipos de delitos
- Formas de participación ciudadana
- Fuentes de información

---

## 4. Cobertura Geográfica

### Municipios Incluidos
La encuesta cubre los 6 municipios del Área Metropolitana de Guadalajara:

1. **El Salto**
2. **Guadalajara** (municipio central)
3. **San Pedro Tlaquepaque**
4. **Tlajomulco de Zúñiga**
5. **Tonalá**
6. **Zapopan**

---

## 5. Valores Faltantes

### Variables con Datos Faltantes Significativos

El análisis identificó **75 variables con valores faltantes**, siendo las más relevantes:

| Variable | Valores Faltantes | % del Total |
|----------|-------------------|-------------|
| Q_74_S | 2,418 | 100% |
| Q_4_S | 2,330 | 96.4% |
| Q_23_O5 | 2,417 | 99.9% |
| Q_23_O4 | 2,417 | 99.9% |
| Q_23_O3 | 2,407 | 99.5% |
| Q_23_O2 | 2,317 | 95.8% |
| Q_81 | 1,148 | 47.5% |
| Q_91 | 1,102 | 45.6% |
| Q_82 | 1,058 | 43.8% |
| IND_SE2024 | 59 | 2.4% |

**Nota:** Muchas de estas variables son preguntas abiertas de seguimiento (sufijo "_S") o preguntas múltiples de opciones (sufijo "_O2", "_O3", etc.) que solo se aplican cuando el encuestado selecciona múltiples opciones.

---

## 6. Estadísticas Descriptivas Clave

### Variables Sociodemográficas

#### Distribución por Género (SEXO)
- **Hombre**: codificado como 1
- **Mujer**: codificado como 2
- **No se puede determinar**: -1

#### Distribución por Edad (EDAD)
Grupos de edad:
- **18-29 años**: 1
- **30-44 años**: 2
- **45-59 años**: 3
- **60+ años**: 4

#### Nivel Educativo (ESC)
- **Sec<**: Secundaria o menos (1)
- **Prep**: Preparatoria (2)
- **Univ+**: Universidad o más (3)

#### Nivel Socioeconómico (NSE2024_C)
Consolidado en 4 categorías:
- **D+/D/E**: Nivel bajo (1)
- **C/C-**: Nivel medio-bajo (2)
- **A/B/C+**: Nivel medio-alto y alto (3)
- **SIN DATOS SUFICIENTES**: (4)

**Estadísticas del NSE2024_C:**
- Media: 2.09 (cercano a nivel medio-bajo)
- Desviación estándar: 0.83
- Mínimo: 1
- Máximo: 4

### Factor de Expansión
- **Media**: 1,475.41
- **Desviación estándar**: 904.81
- **Mínimo**: 264.03
- **Máximo**: 4,272.25

Este factor permite expandir los resultados de la muestra a la población total del AMG.

---

## 7. Calidad de los Datos

### Fortalezas
1. **Muestra robusta**: 2,418 casos proporcionan representatividad estadística
2. **Cobertura completa**: Incluye todos los municipios del AMG
3. **Diseño integral**: Abarca múltiples dimensiones de la vida urbana
4. **Metadatos ricos**: Incluye etiquetas detalladas para todas las variables categóricas
5. **Factor de expansión**: Permite extrapolación a la población total
6. **Variables derivadas**: Facilitan el análisis al tener categorizaciones pre-calculadas

### Consideraciones
1. **Valores faltantes**: 75 variables tienen datos faltantes, principalmente en:
   - Preguntas abiertas (especificaciones)
   - Opciones múltiples de respuesta (O2, O3, O4, etc.)
   - Preguntas filtradas que no aplican a todos
2. **Codificación especial**: Los valores -1 y -2 requieren manejo especial en el análisis
3. **Variables categóricas**: Requieren interpretación cuidadosa de las etiquetas

---

## 8. Estructura de Nomenclatura de Variables

### Prefijos y Patrones

#### Prefijo "Q_"
Preguntas directas individuales (ej: `Q_1`, `Q_74`)

#### Prefijo "T_Q_"
Preguntas en formato tabla o batería (múltiples ítems con la misma escala)
- Ejemplo: `T_Q_12_1` a `T_Q_12_5` (evaluación de diferentes servicios)

#### Sufijo "_O1", "_O2", "_O3"
Opciones múltiples de respuesta ordenadas
- Ejemplo: `Q_23_O1`, `Q_23_O2` (primera, segunda opción de modo de transporte)

#### Sufijo "_S"
Especificación abierta para la opción "Otro"
- Ejemplo: `Q_4_S` (especificación de "otro" para Q_4)

#### Variables sin prefijo
Variables derivadas o de clasificación:
- `SbjNum`, `Date`, `Duration`
- `SEXO`, `EDAD`, `ESC`, `NSE2024`, `CALIDAD_VIDA`
- `FACTOR`

---

## 9. Aplicaciones y Usos Potenciales

### Análisis Descriptivos
- Perfiles sociodemográficos de la población del AMG
- Distribución de opiniones sobre servicios públicos
- Niveles de satisfacción ciudadana por municipio
- Patrones de movilidad urbana

### Análisis Inferenciales
- Comparaciones entre municipios
- Análisis por grupos de edad, género, NSE
- Correlaciones entre satisfacción y variables sociodemográficas
- Identificación de predictores de calidad de vida

### Segmentación
- Perfiles de ciudadanos por nivel de satisfacción
- Grupos de riesgo en seguridad
- Clusters de participación ciudadana
- Tipologías de usuarios de transporte

### Análisis Temporal
- Si se cuenta con datos de años anteriores, permite análisis de tendencias
- Evaluación de políticas públicas a lo largo del tiempo

### Ponderación
- Uso del factor de expansión para generar estimaciones poblacionales
- Proyecciones a nivel metropolitano

---

## 10. Recomendaciones para el Análisis

### Preparación de Datos
1. **Manejo de valores especiales**: Convertir -1 y -2 a NA/null según corresponda
2. **Validación de rangos**: Verificar que las respuestas estén dentro de los valores esperados
3. **Aplicación de etiquetas**: Usar las etiquetas de valor para interpretación
4. **Factor de expansión**: Considerar su uso para resultados representativos

### Análisis Exploratorio
1. **Distribuciones univariadas**: Frecuencias para cada variable categórica
2. **Cruces básicos**: Tablas de contingencia con variables sociodemográficas
3. **Visualizaciones**: Gráficos de barras, mapas por municipio, distribuciones por NSE
4. **Identificación de patrones**: Buscar relaciones entre satisfacción y otros factores

### Análisis Avanzados
1. **Modelos de regresión**: Para identificar predictores de satisfacción
2. **Análisis factorial**: Para reducir dimensionalidad en baterías de preguntas
3. **Análisis de correspondencia**: Para explorar relaciones entre variables categóricas
4. **Modelos multinivel**: Considerando la estructura jerárquica (individuos en municipios)

### Reportes
1. **Por municipio**: Comparaciones entre los 6 municipios
2. **Por NSE**: Brechas entre niveles socioeconómicos
3. **Por edad**: Diferencias generacionales
4. **Temáticos**: Reportes específicos sobre movilidad, seguridad, servicios, etc.

---

## 11. Metadatos Técnicos

### Información del Archivo
- **Nombre del archivo**: datos.sav
- **Formato**: SPSS Statistics (.sav)
- **Número de variables**: 265
- **Número de casos**: 2,418
- **Fecha de análisis**: 2025-11-25
- **Archivo de metadatos**: data_info.json

### Software Recomendado
- **Python**: pandas, pyreadstat, matplotlib, seaborn
- **R**: haven, dplyr, ggplot2
- **SPSS**: Compatible nativamente
- **Stata**: Compatible con conversión

### Codificación
- **Etiquetas de variables**: Todas las variables tienen etiquetas descriptivas
- **Etiquetas de valores**: Variables categóricas tienen diccionarios de valores
- **Encoding**: UTF-8 para texto en español

---

## 12. Conclusiones

El archivo `datos.sav` contiene una **base de datos rica y multidimensional** de una encuesta de opinión ciudadana en el Área Metropolitana de Guadalajara. Con **2,418 casos** y **265 variables**, ofrece una visión integral de:

- Percepción de calidad de vida
- Evaluación de servicios públicos
- Movilidad y transporte
- Seguridad pública y vial
- Participación ciudadana
- Confianza en instituciones
- Características sociodemográficas

### Valor Analítico
Los datos permiten:
- **Diagnósticos urbanos** detallados por municipio
- **Identificación de problemáticas** prioritarias
- **Evaluación de políticas públicas**
- **Segmentación de la población** para intervenciones focalizadas
- **Análisis comparativos** entre territorios y grupos sociales

### Calidad General
La base de datos muestra:
- ✅ Diseño metodológico sólido
- ✅ Muestra representativa
- ✅ Cobertura territorial completa
- ✅ Documentación adecuada (metadatos)
- ⚠️ Valores faltantes en variables específicas (principalmente filtradas)

---

## 13. Contacto y Documentación Adicional

Para análisis específicos o preguntas sobre la interpretación de variables particulares, consulte:
- El archivo de metadatos completo: `data_info.json`
- La documentación del cuestionario original (si está disponible)
- Las etiquetas de valores incluidas en el archivo SPSS

---

**Documento generado automáticamente**  
Fecha: 25 de noviembre de 2025  
Fuente: Análisis de datos.sav mediante Python (pyreadstat + pandas)
