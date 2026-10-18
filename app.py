from datetime import date
import os
import pandas as pd
import streamlit as st

# Configuración de la página optimizada para móvil
st.set_page_config(
    page_title="Control Tensión Arterial", page_icon="🩺", layout="centered"
)

# Estilos CSS avanzados para apariencia móvil
st.markdown(
    """
    <style>
    .stApp {
        background-color: #EBF3F1;
    }
    .block-container {
        max-width: 450px !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #FFFFFF;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #2E8B57;
        color: white;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        padding: 12px;
        border: none;
        box-shadow: 0 4px 10px rgba(46, 139, 87, 0.2);
    }
    .stButton>button:hover {
        background-color: #236B43;
        color: white;
    }
    h1, h2, h3 {
        color: #1F4E5B;
        font-family: sans-serif;
    }
    .card {
        background-color: #F4F9F7;
        padding: 20px;
        border-radius: 14px;
        border-left: 5px solid #2E8B57;
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
      "<h1 style='text-align: center; font-size: 1.8rem;'>🩺 CONTROL TENSIÓN"
      " ARTERIAL</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #666; font-size: 0.95rem;'>Mantén tu"
      " salud bajo control de forma sencilla.</p>",
      unsafe_allow_html=True,
  )

  st.write("---")

  if st.button("🚀 INICIAR", key="btn_inicio_iniciar"):
    cambiar_pantalla("iniciar")
    st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("📊 HISTORIAL", key="btn_inicio_historial"):
    cambiar_pantalla("historial")
    st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("ℹ️ INFO", key="btn_inicio_info"):
    cambiar_pantalla("info")
    st.rerun()

  st.markdown("<br><br>", unsafe_allow_html=True)
  st.info(
      "💡 **Consejo:** Toma 3 medidas consecutivas de tu tensión en reposo e"
      " introduce los valores máximos y mínimos."
  )

# ---------------------------------------------------------
# PANTALLA 2: INICIAR (Formulario de 3 medidas)
# ---------------------------------------------------------
elif st.session_state.pantalla == "iniciar":
  st.subheader("📝 Registro de Nuevas Medidas")
  st.write("Introduce la fecha y los valores de tus **3 tomas**:")

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
  if st.button("🏠 Volver a Inicio", key="btn_form_volver"):
    cambiar_pantalla("inicio")
    st.rerun()

# ---------------------------------------------------------
# PANTALLA 3: RESULTADO Y VALORACIÓN
# ---------------------------------------------------------
elif st.session_state.pantalla == "resultado":
  st.subheader("🔍 Valoración de Medidas")

  if "datos_temp" in st.session_state:
    datos = st.session_state.datos_temp
    sist = datos["sist_media"]
    diast = datos["diast_media"]

    if sist < 90 or diast < 60:
      estado = "Low (Baja)"
      color_alerta = "#007BFF"
    elif sist < 120 and diast < 80:
      estado = "Normal"
      color_alerta = "#28A745"
    elif (120 <= sist <= 139) or (80 <= diast <= 89):
      estado = "Prehypertension (Prehipertensión)"
      color_alerta = "#FFC107"
    elif (140 <= sist <= 159) or (90 <= diast <= 99):
      estado = "Hypertension Stage 1 (Hipertensión Grado 1)"
      color_alerta = "#FD7E14"
    else:
      estado = "Hypertension Stage 2 (Hipertensión Grado 2)"
      color_alerta = "#DC3545"

    st.markdown(
        f"""
        <div class="card">
            <h4>📅 Fecha: {datos['fecha']}</h4>
            <p><b>Promedio Máxima (Sistólica):</b> {sist} mmHg</p>
            <p><b>Promedio Mínima (Diastólica):</b> {diast} mmHg</p>
            <hr>
            <p><b>Estado Actual:</b><br><span style="color:{color_alerta}; font-size:1.1em; font-weight:bold;">{estado}</span></p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("💾 REGISTRAR EN EXCEL", key="btn_registrar_excel"):
      df = pd.read_excel(EXCEL_FILE)
      nuevo_registro = pd.DataFrame([{
          "Fecha": str(datos["fecha"]),
          "Sistólica Media": sist,
          "Diastólica Media": diast,
          "Estado / Valoración": estado,
      }])
      df = pd.concat([df, nuevo_registro], ignore_index=True)
      df.to_excel(EXCEL_FILE, index=False)
      st.success("¡Valores almacenados correctamente!")

  else:
    st.warning("No hay datos recientes calculados.")

  st.write("---")
  col_1, col_2 = st.columns(2)
  with col_1:
    if st.button("📊 Historial", key="btn_res_historial"):
      cambiar_pantalla("historial")
      st.rerun()
  with col_2:
    if st.button("🏠 Inicio", key="btn_res_inicio"):
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

      # Botón de descarga directa con lectura segura de bytes
      with open(EXCEL_FILE, "rb") as f:
        excel_bytes = f.read()

      st.download_button(
          label="📥 Descargar Excel en mi dispositivo",
          data=excel_bytes,
          file_name="historial_tension.xlsx",
          mime=(
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          ),
          key="btn_descargar_excel",
      )

      st.markdown("### Evolución Gráfica")
      if len(df) > 0:
        df_chart = df.set_index("Fecha")[
            ["Sistólica Media", "Diastólica Media"]
        ]
        st.line_chart(df_chart)
    else:
      st.info("Aún no hay registros guardados.")
  else:
    st.info("No se encontró el archivo de Excel todavía.")

  st.write("---")
  if st.button("🏠 Volver a Inicio", key="btn_historial_inicio"):
    cambiar_pantalla("inicio")
    st.rerun()

# ---------------------------------------------------------
# PANTALLA 5: INFO (Guía de Tensión)
# ---------------------------------------------------------
elif st.session_state.pantalla == "info":
  st.subheader("ℹ️ Información y Tabla")
  st.write("Rangos oficiales de presión arterial:")

  if os.path.exists("tabla_tension.jpg"):
    st.image(
        "tabla_tension.jpg",
        caption="Blood Pressure Chart Reference",
        use_container_width=True,
    )
  else:
    st.warning(
        "⚠️ Coloca la imagen de la tabla con el nombre 'tabla_tension.jpg' en"
        " la misma carpeta."
    )

  st.markdown("""
  * 🟢 **Normal:** Sistólica < 120 y Diastólica < 80.
  * 🟡 **Prehipertensión:** Sistólica 120–139 o Diastólica 80–89.
  * 🟠 **Hipertensión Grado 1:** Sistólica 140–159 o Diastólica 90–99.
  * 🔴 **Hipertensión Grado 2:** Sistólica ≥ 160 o Diastólica ≥ 100.
  * 🔵 **Baja (Low):** Sistólica < 90 o Diastólica < 60.
  """)

  st.write("---")
  if st.button("🏠 Volver a Inicio", key="btn_info_inicio"):
    cambiar_pantalla("inicio")
    st.rerun()