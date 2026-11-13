# Apuntes de Matemáticas · curso 2026-27

Web con todos los apuntes: **Matemáticas (1º ESO)**, **Matemáticas B (4º ESO)**, **Matemáticas II** y **Matemáticas Aplicadas a las CCSS II (2º Bachillerato)**.
Teoría, ejemplos y ejercicios resueltos, en web y en PDF (con y sin soluciones).

La portada es `index.html`. Todos los archivos están en la raíz, sin carpetas; el nombre empieza por la asignatura:

- `1eso-matematicas-…` — curso completo, UP1 a UP4, colección de ejercicios y cuadernillos UP1 a UP4
- `4eso-matematicas-b-…` — curso completo, evaluaciones, colección de ejercicios y cuadernillo UP1
- `2bach-matematicas-ii-…` — curso completo, UP1 a UP4 y ejercicios del libro por UP (`…-libro-upN`)
- `2bach-matematicas-ccss-ii-…` — curso completo y las tres evaluaciones


## Actualizar

Las páginas se generan a partir de la carpeta `Apuntes/` con:

```
python3 construir_web.py
```

Después, sube los cambios al repositorio (GitHub Pages publica la rama `main`, carpeta raíz).
