import os
from datetime import date
import pandas as pd
import streamlit as st

# Configuración de la página para dispositivos móviles
st.set_page_config(
    page_title="Control Tensión Arterial", page_icon="🩺", layout="centered"
)

# Estilos CSS personalizados (Tonos verdes y azulados, diseño limpio y agradable)
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f7f4;
    }
    .stButton>button {
        background-color: #2E8B57;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        padding: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #205c3b;
        color: white;
    }
    h1, h2, h3 {
        color: #1F4E5B;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

EXCEL_FILE = "historial_tension.xlsx"


# Inicializar archivo Excel si no existe
def inicializar_excel():
  if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(
        columns=[
            "Fecha",
            "Sistólica Media",
            "Diastólica Media",
            "Estado / Valoración",
        ]
    )
    df.to_excel(EXCEL_FILE, index=False)


inicializar_excel()

# Control de navegación entre las 5 pantallas
if "pantalla" not in st.session_state:
  st.session_state.pantalla = "inicio"


def cambiar_pantalla(nombre):
  st.session_state.pantalla = nombre


# ---------------------------------------------------------
# PANTALLA 1: INICIO
# ---------------------------------------------------------
if st.session_state.pantalla == "inicio":
  st.markdown(
      "<h1 style='text-align: center;'>🩺 Control Tensión Arterial</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #555;'>Mantén tu salud bajo"
      " control de forma sencilla.</p>",
      unsafe_allow_html=True,
  )

  st.write("---")

  col1, col2, col3 = st.columns(3)
  with col1:
    if st.button("🚀 Iniciar"):
      cambiar_pantalla("iniciar")
  with col2:
    if st.button("📊 Historial"):
      cambiar_pantalla("historial")
  with col3:
    if st.button("ℹ️ Info"):
      cambiar_pantalla("info")

  st.markdown("<br><br>", unsafe_allow_html=True)
  st.info(
      "💡 **Consejo:** Toma 3 medidas consecutivas de tu tensión en reposo e"
      " introduce los valores máximos (sistólica) y mínimos (diastólica)."
  )

# ---------------------------------------------------------
# PANTALLA 2: INICIAR (Formulario de 3 medidas)
# ---------------------------------------------------------
elif st.session_state.pantalla == "iniciar":
  st.subheader("📝 Registro de Nuevas Medidas")
  st.write(
      "Introduce la fecha y los valores máximos y mínimos de tus **3"
      " tomas**[cite: 2]:"
  )

  with st.form("form_tensions"):
    fecha_medida = st.date_input("Fecha de la medición", value=date.today())

    st.markdown("---")
    st.markdown("### 📌 Medida 1")
    sistolica_1 = st.number_input(
        "Máxima (Sistólica) 1", min_value=50, max_value=250, value=120, step=1
    )
    diastolica_1 = st.number_input(
        "Mínima (Diastólica) 1", min_value=30, max_value=150, value=80, step=1
    )

    st.markdown("---")
    st.markdown("### 📌 Medida 2")
    sistolica_2 = st.number_input(
        "Máxima (Sistólica) 2", min_value=50, max_value=250, value=120, step=1
    )
    diastolica_2 = st.number_input(
        "Mínima (Diastólica) 2", min_value=30, max_value=150, value=80, step=1
    )

    st.markdown("---")
    st.markdown("### 📌 Medida 3")
    sistolica_3 = st.number_input(
        "Máxima (Sistólica) 3", min_value=50, max_value=250, value=120, step=1
    )
    diastolica_3 = st.number_input(
        "Mínima (Diastólica) 3", min_value=30, max_value=150, value=80, step=1
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Siguiente ➡️")

    if submitted:
      # Guardar datos en el estado de sesión para calcular medias en la siguiente pantalla
      st.session_state.datos_temp = {
          "fecha": fecha_medida,
          "sist_media": round((sistolica_1 + sistolica_2 + sistolica_3) / 3, 1),
          "diast_media": round(
              (diastolica_1 + diastolica_2 + diastolica_3) / 3, 1
          ),
      }
      cambiar_pantalla("resultado")
      st.rerun()

  st.write("---")
  if st.button("🏠 Volver a Inicio"):
    cambiar_pantalla("inicio")
    st.rerun()

# ---------------------------------------------------------
# PANTALLA 3: RESULTADO Y VALORACIÓN
# ---------------------------------------------------------
elif st.session_state.pantalla == "resultado":
  st.subheader("🔍 Valoración de las Últimas Medidas")

  if "datos_temp" in st.session_state:
    datos = st.session_state.datos_temp
    sist = datos["sist_media"]
    diast = datos["diast_media"]

    # Determinación del estado según la tabla oficial del gráfico aportado
    if sist < 90 or diast < 60:
      estado = "Low (Baja)"
      color_alerta = "blue"
    elif sist < 120 and diast < 80:
      estado = "Normal"
      color_alerta = "green"
    elif (120 <= sist <= 139) or (80 <= diast <= 89):
      estado = "Prehypertension (Prehipertensión)"
      color_alerta = "orange"
    elif (140 <= sist <= 159) or (90 <= diast <= 99):
      estado = "Hypertension Stage 1 (Hipertensión Grado 1)"
      color_alerta = "red"
    else:
      estado = "Hypertension Stage 2 (Hipertensión Grado 2)"
      color_alerta = "darkred"

    st.markdown(
        f"""
        <div class="card">
            <h4>📅 Fecha: {datos['fecha']}</h4>
            <p><b>Promedio Máxima (Sistólica):</b> {sist} mmHg</p>
            <p><b>Promedio Mínima (Diastólica):</b> {diast} mmHg</p>
            <hr>
            <p><b>Estado Actual:</b> <span style="color:{color_alerta}; font-size:1.2em; font-weight:bold;">{estado}</span></p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("💾 Registrar en Excel"):
      # Cargar Excel existente, añadir registro y guardar
      df = pd.read_excel(EXCEL_FILE)
      nuevo_registro = pd.DataFrame([{
          "Fecha": str(datos["fecha"]),
          "Sistólica Media": sist,
          "Diastólica Media": diast,
          "Estado / Valoración": estado,
      }])
      df = pd.concat([df, nuevo_registro], ignore_index=True)
      df.to_excel(EXCEL_FILE, index=False)
      st.success("¡Valores almacenados correctamente en el archivo Excel!")

  else:
    st.warning("No hay datos recientes calculados. Por favor, introduce medidas.")

  st.write("---")
  col_1, col_2 = st.columns(2)
  with col_1:
    if st.button("📊 Ver Historial"):
      cambiar_pantalla("historial")
      st.rerun()
  with col_2:
    if st.button("🏠 Volver a Inicio"):
      cambiar_pantalla("inicio")
      st.rerun()

# ---------------------------------------------------------
# PANTALLA 4: HISTORIAL Y GRÁFICO
# ---------------------------------------------------------
elif st.session_state.pantalla == "historial":
  st.subheader("📊 Historial de Registros")

  if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
    if not df.empty:
      st.dataframe(df, use_container_width=True)

      st.markdown("### Evolución Gráfica")
      # Gráfico de líneas integrado para visualizar la evolución temporal
      if len(df) > 0:
        df_chart = df.set_index("Fecha")[
            ["Sistólica Media", "Diastólica Media"]
        ]
        st.line_chart(df_chart)
    else:
      st.info(
          "Aún no hay registros guardados. Realiza una medición y regístrala."
      )
  else:
    st.info("No se encontró el archivo de Excel todavía.")

  st.write("---")
  if st.button("🏠 Volver a Inicio"):
    cambiar_pantalla("inicio")
    st.rerun()

# ---------------------------------------------------------
# PANTALLA 5: INFO (Guía de Tensión)
# ---------------------------------------------------------
elif st.session_state.pantalla == "info":
  st.subheader("ℹ️ Información y Tabla de Referencia")
  st.write(
      "Esta tabla te muestra los rangos oficiales de presión arterial para"
      " interpretar tus resultados:"
  )

  # Carga de la imagen local situada en la misma carpeta (asegúrate de llamarla tabla_tension.jpg)
  if os.path.exists("tabla_tension.jpg"):
    st.image(
        "tabla_tension.jpg",
        caption="Blood Pressure Chart Reference",
        use_container_width=True,
    )
  else:
    st.warning(
        "⚠️ Coloca la imagen de la tabla con el nombre 'tabla_tension.jpg' en"
        " la misma carpeta para visualizarla aquí."
    )

  st.markdown("""
  * 🟢 **Normal:** Sistólica por debajo de 120 y Diastólica por debajo de 80[cite: 2].
  * 🟡 **Prehipertensión:** Sistólica de 120 a 139 o Diastólica de 80 a 89[cite: 2].
  * 🟠 **Hipertensión Grado 1:** Sistólica de 140 a 159 o Diastólica de 90 a 99[cite: 2].
  * 🔴 **Hipertensión Grado 2:** Sistólica de 160 o más, o Diastólica de 100 o más[cite: 2].
  * 🔵 **Baja (Low):** Sistólica menor de 90 o Diastólica menor de 60[cite: 2].
  """)

  st.write("---")
  if st.button("🏠 Volver a Inicio"):
    cambiar_pantalla("inicio")
    st.rerun()