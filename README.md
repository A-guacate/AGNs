# AGNs: Análisis Nebular de Cuásares

![Universe banner](https://i.pinimg.com/1200x/53/a6/a2/53a6a21ed1265bc8e5de932c3102031e.jpg)
> Rocket Man | Elton John [▶](https://www.youtube.com/watch?v=DtVBCG6ThDk&list=RDDtVBCG6ThDk&start_radio=1)

## Descripción

Este proyecto implementa un análisis de diagnóstico nebular basado en tres ecuaciones de ratios de líneas de emisión prohibidas (OII, OIII, SII) que dependen de $T_e$ y $N_e$. Al contar con más ecuaciones que incógnitas, se minimiza el residuo $\chi^2$ para encontrar los valores óptimos de estos parámetros.


## 📁 Estructura del Proyecto

```
AGNs/
├── README.md                   
├── pyproject.toml              # Configuración del proyecto y dependencias (pixi)
├── QSO.ipynb                   # Notebook principal 
├── data_sdss.csv               # Datos de entrada (SDSS)
├── diagnostico_nebular.md      # Documentación de la física del proyecto
└── src/
    └── agns/
        ├── __init__.py         # Inicializador del módulo
        └── qso_table.py        # Funciones para generar tablas LaTeX
```