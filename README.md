# Sistema de Comisiones de Vendedores

Sistema completo para calcular comisiones de vendedores por rango de fechas, desarrollado con **Flask** (backend) y **React** (frontend).

## 📋 Descripción del Proyecto

Basado en el video explicativo de [feli203040](https://github.com/feli203040/Video-Explicativo-C-.NET), este sistema implementa:

- **3 tablas principales**: Vendedores, Ventas (fecha y monto), y Reglas de Comisiones
- **Cálculo automático** de comisiones por rango de fechas
- **Interfaz moderna** para gestionar y visualizar datos
- **Datos quemados** (hardcoded) como se especificó en los requisitos

## 🚀 Características

### Backend (Flask)
- ✅ API RESTful completa
- ✅ Cálculo de comisiones por rango de fechas
- ✅ Gestión de vendedores, ventas y reglas
- ✅ CORS habilitado para comunicación con frontend
- ✅ Datos de ejemplo incluidos

### Frontend (React)
- ✅ Interfaz moderna y responsive
- ✅ Formularios para calcular comisiones
- ✅ Tablas para visualizar datos
- ✅ Formulario para agregar nuevas ventas
- ✅ Diseño con gradientes y efectos visuales

## 📊 Ejemplo de Funcionamiento

**Rango de fechas**: 2 de junio a 26 de junio

**Vendedor Perico**:
- 2 ventas en el rango: $40 + $40 = $80 total
- Regla: 10% de comisión
- **Comisión calculada**: $8.00

**Vendedor Sola**:
- 1 venta en el rango: $60 total
- Regla: 8% de comisión  
- **Comisión calculada**: $4.80

## 🛠️ Instalación y Uso

### Prerrequisitos
- Python 3.7+
- Node.js 14+
- npm o yarn

### Backend (Flask)

1. **Navegar al directorio backend**:
   ```bash
   cd backend
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el servidor**:
   ```bash
   python app.py
   ```

El backend estará disponible en: `http://localhost:5000`

### Frontend (React)

1. **Navegar al directorio frontend**:
   ```bash
   cd frontend
   ```

2. **Instalar dependencias**:
   ```bash
   npm install
   ```

3. **Ejecutar la aplicación**:
   ```bash
   npm start
   ```

El frontend estará disponible en: `http://localhost:3000`

## 📁 Estructura del Proyecto

```
Video/
├── backend/
│   ├── app.py              # API principal de Flask
│   └── requirements.txt    # Dependencias de Python
├── frontend/
│   ├── public/             # Archivos públicos
│   ├── src/
│   │   ├── App.js          # Componente principal
│   │   ├── App.css         # Estilos
│   │   └── index.js        # Punto de entrada
│   ├── package.json        # Dependencias de Node.js
│   └── README.md           # Documentación de React
└── README.md               # Este archivo
```

## 🔌 Endpoints de la API

### GET `/api/vendedores`
Obtiene la lista de todos los vendedores.

### GET `/api/ventas`
Obtiene la lista de todas las ventas.

### GET `/api/reglas`
Obtiene las reglas de comisión para cada vendedor.

### POST `/api/calcular-comisiones`
Calcula comisiones para un rango de fechas.

**Body**:
```json
{
  "fecha_inicio": "2024-06-02",
  "fecha_fin": "2024-06-26"
}
```

### POST `/api/agregar-venta`
Agrega una nueva venta al sistema.

**Body**:
```json
{
  "vendedor_id": 1,
  "fecha": "2024-06-15",
  "monto": 50.00
}
```

## 💾 Datos de Ejemplo

### Vendedores
- **Perico** (ID: 1) - 10% de comisión
- **Sola** (ID: 2) - 8% de comisión  
- **Carlos** (ID: 3) - 12% de comisión
- **María** (ID: 4) - 9% de comisión

### Ventas de Ejemplo
- Perico: 2 ventas en junio ($40 + $40 = $80)
- Sola: 1 venta en junio ($60)
- Carlos: 1 venta en junio ($90)
- María: 1 venta en junio ($75)

## 🎨 Características de la UI

- **Diseño moderno** con gradientes y efectos glassmorphism
- **Responsive** para dispositivos móviles y desktop
- **Animaciones suaves** y transiciones
- **Tablas interactivas** con hover effects
- **Formularios intuitivos** con validación
- **Resultados visuales** claros y organizados

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask**: Framework web de Python
- **Flask-CORS**: Para manejo de CORS
- **datetime**: Para manejo de fechas

### Frontend
- **React 18**: Biblioteca de UI
- **Axios**: Cliente HTTP
- **CSS3**: Estilos modernos con gradientes y efectos
- **HTML5**: Estructura semántica

## 📝 Notas de Desarrollo

- Los datos están **quemados** (hardcoded) como se especificó en los requisitos
- No se requiere base de datos ni sistema de autenticación
- El sistema está diseñado para ser fácilmente extensible
- La interfaz es intuitiva y no requiere documentación adicional

## 🤝 Contribución

Este proyecto fue desarrollado como respuesta a los requisitos especificados en el video explicativo. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Desarrollado con ❤️ usando Flask y React** 