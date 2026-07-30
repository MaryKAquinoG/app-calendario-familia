import streamlit as st
import random
from datetime import datetime

# ------------------------------------------
# Manejo de parámetros de URL (enlaces mágicos)
# ------------------------------------------
parametros = st.experimental_get_query_params()
if "correo" in parametros and parametros["correo"]:
    # st.experimental_get_query_params devuelve listas de valores
    st.session_state["correo_jugador"] = parametros["correo"][0].lower()

# ------------------------------------------
# Si no hay correo en sesión, mostramos la pantalla de login
# ------------------------------------------
if "correo_jugador" not in st.session_state:
    st.set_page_config(page_title="¡Planificador Divertido!", page_icon="🎮", layout="centered")
    st.markdown('<h1 class="titulo-texto">¡Bienvenido! Inicia tu Aventura</h1>', unsafe_allow_html=True)
    st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
    st.write("🌟 **Acceso Libre:** Ingresa tu correo o pide a tus padres tu enlace mágico.")
    correo_input = st.text_input("📧 Ingresa tu correo electrónico:")
    if st.button("🔑 Entrar al Juego"):
        if "@" in correo_input and "." in correo_input:
            st.session_state["correo_jugador"] = correo_input.lower()
            st.experimental_rerun()
        else:
            st.error("🛑 Ingresa un correo válido.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ------------------------------------------
# Importante: desde aquí el jugador está identificado
# ------------------------------------------
st.set_page_config(page_title="¡Planificador Divertido!", page_icon="🎮", layout="centered")

# ------------------------------------------
# Inicializar estado si falta
# ------------------------------------------
if 'perfil_creado' not in st.session_state:
    st.session_state.perfil_creado = False
    st.session_state.puntos = 0
    st.session_state.copas = 15
    st.session_state.nombre = ""
    st.session_state.papa = "Papá"
    st.session_state.mama = "Mamá"
    st.session_state.fondo = "🌟 Blanco Mágico"
    st.session_state.mi_armario = {
        "Cara": ["👦 Niño", "👧 Niña", "🤖 Robot", "🐶 Perrito", "👽 Alien"],
        "Cabeza": ["(Nada)", "🧢 Gorra", "👑 Corona", "🎀 Lazo", "🎩 Sombrero"],
        "Camisa": ["👕 Camiseta", "👚 Blusa", "🧥 Abrigo", "🦺 Chaleco", "👗 Vestido Entero"],
        "Piernas": ["(Nada)", "👖 Jeans", "🩳 Shorts", "👗 Falda"],
        "Medias": ["(Nada)", "🧦 Medias Blancas", "🧧 Medias Rojas"],
        "Zapatos": ["👟 Deportivos", "👞 Zapatos Cuero", "🥾 Botas"]
    }
    st.session_state.avatar_equipado = {
        "Cara": "👦 Niño",
        "Cabeza": "(Nada)",
        "Camisa": "👕 Camiseta",
        "Piernas": "👖 Jeans",
        "Medias": "(Nada)",
        "Zapatos": "👟 Deportivos"
    }
    st.session_state.reto_resuelto = False
    st.session_state.agenda = {}
    st.session_state.num1 = random.randint(2, 9)
    st.session_state.num2 = random.randint(2, 9)

colores_fondos = {
    "🌟 Blanco Mágico": "#E8F8F5",
    "🦄 Galaxia Pastel": "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)",
    "🦖 Bosque Jurásico": "linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)",
    "🌋 Volcán de Lava": "linear-gradient(135deg, #ff9a44 0%, #fc6076 100%)"
}

fondo_actual = colores_fondos.get(st.session_state.fondo, "#E8F8F5")

# ------------------------------------------
# CSS
# ------------------------------------------
st.markdown(f"""
    <style>
    .stApp {{ background: {fondo_actual}; background-attachment: fixed; transition: all 0.5s ease; }}
    .avatar-totem {{ display:flex; flex-direction:column; align-items:center; justify-content:center; background-color: rgba(255,255,255,0.85); border: 4px dashed #6495ED; border-radius: 20px; padding: 12px; width: 220px; margin: 6px auto 18px auto; }}
    .p-cabeza {{ font-size: 44px; margin-bottom: -8px; }}
    .p-cara {{ font-size: 70px; }}
    .p-camisa {{ font-size: 48px; margin-top: -12px; }}
    .p-piernas {{ font-size: 40px; margin-top: -8px; }}
    .titulo-texto {{ color: #FF5733; font-family: 'Comic Sans MS', cursive; font-size: 2.0rem; text-align: center; }}
    .caja-translucida {{ background-color: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 14px; margin-bottom: 14px; box-shadow: 0 8px 16px rgba(0,0,0,0.06); }}
    .oracion-didactica {{ font-size: 16px; color: #2E8B57; font-weight: bold; text-align: center; margin-top: 10px; background: #e8f5e9; padding: 8px; border-radius: 10px; border: 1px solid #a5d6a7; }}
    .stButton>button {{ background-color: #FFC300; color: #900C3F; font-weight: bold; border-radius: 12px; width: 100%; font-size: 16px; border: 2px solid #ff9900; }}
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------
# Helper: render avatar
# ------------------------------------------

def renderizar_avatar_html():
    cabeza = st.session_state.avatar_equipado.get("Cabeza", "").split()[0] if st.session_state.avatar_equipado.get("Cabeza", "") != "(Nada)" else ""
    cara = st.session_state.avatar_equipado.get("Cara", "").split()[0] if st.session_state.avatar_equipado.get("Cara", "") else ""
    camisa = st.session_state.avatar_equipado.get("Camisa", "").split()[0] if st.session_state.avatar_equipado.get("Camisa", "") != "(Nada)" else ""
    piernas = st.session_state.avatar_equipado.get("Piernas", "").split()[0] if st.session_state.avatar_equipado.get("Piernas", "") != "(Nada)" else ""
    medias = (st.session_state.avatar_equipado.get("Medias", "").split()[0] * 2) if st.session_state.avatar_equipado.get("Medias", "") != "(Nada)" else ""
    zapatos = (st.session_state.avatar_equipado.get("Zapatos", "").split()[0] * 2) if st.session_state.avatar_equipado.get("Zapatos", "") != "(Nada)" else ""
    html = f"""
    <div class="avatar-totem">
        <div class="p-cabeza">{cabeza}</div>
        <div class="p-cara">{cara}</div>
        <div class="p-camisa">{camisa}</div>
        <div class="p-piernas">{piernas}</div>
        <div class="p-medias">{medias}</div>
        <div class="p-zapatos">{zapatos}</div>
    </div>
    """
    return html

# ------------------------------------------
# actualizar avatar desde selectboxes
# ------------------------------------------

def actualizar_avatar():
    # Las claves sel_* existen si el usuario interactuó; usamos .get para evitar KeyError
    if st.session_state.get("sel_cara"):
        st.session_state.avatar_equipado["Cara"] = st.session_state.get("sel_cara")
    if st.session_state.get("sel_cabeza"):
        st.session_state.avatar_equipado["Cabeza"] = st.session_state.get("sel_cabeza")
    if st.session_state.get("sel_camisa"):
        st.session_state.avatar_equipado["Camisa"] = st.session_state.get("sel_camisa")
    if st.session_state.get("sel_piernas"):
        st.session_state.avatar_equipado["Piernas"] = st.session_state.get("sel_piernas")
    if st.session_state.get("sel_medias"):
        st.session_state.avatar_equipado["Medias"] = st.session_state.get("sel_medias")
    if st.session_state.get("sel_zapatos"):
        st.session_state.avatar_equipado["Zapatos"] = st.session_state.get("sel_zapatos")

# ------------------------------------------
# PANTALLA PRINCIPAL
# ------------------------------------------
if not st.session_state.perfil_creado:
    st.markdown('<h1 class="titulo-texto">¡Crea tu Cuenta de Jugador!</h1>', unsafe_allow_html=True)
    st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
    st.session_state.nombre = st.text_input("📝 ¿Cómo te llamas?")
    colP, colM = st.columns(2)
    st.session_state.papa = colP.text_input("👨 Nombre de Papá (Opcional):", "Papá")
    st.session_state.mama = colM.text_input("👩 Nombre de Mamá (Opcional):", "Mamá")
    st.session_state.fondo = st.selectbox("🎨 Escoge el fondo de tu app", list(colores_fondos.keys()))
    if st.button("🚀 ¡ENTRAR AL JUEGO!"):
        if st.session_state.nombre.strip() != "":
            st.session_state.perfil_creado = True
            st.experimental_rerun()
        else:
            st.error("🛑 Debes poner tu nombre para iniciar.")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Cabecera con avatar y estado
    st.markdown(renderizar_avatar_html(), unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align:center; margin-bottom:10px;">
            <h2 class="titulo-texto">¡A jugar, {st.session_state.nombre}!</h2>
            <div style="font-size:18px; color:#E67E22; font-weight:bold;">Tus Monedas: {st.session_state.copas} 🏆</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎮 Misiones", "👕 Vestidor", "🛍️ Tienda", "📅 Agenda"])

    # Misiones
    with tab1:
        st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
        tareas_completadas = 0
        if st.checkbox("🛏️ Tendí mi cama y ordené"): tareas_completadas += 1
        if st.checkbox("📚 Hice mis tareas de la escuela"): tareas_completadas += 1
        if st.checkbox(f"🤝 Ayudé a {st.session_state.papa} o a {st.session_state.mama}"): tareas_completadas += 1
        st.write("---")
        st.info("🧠 **Mini-Juego: Escudo Mental (+20 pts)**")
        resp = st.number_input(f"¿Cuánto es {st.session_state.num1} x {st.session_state.num2}?", step=1, value=0)
        if resp == (st.session_state.num1 * st.session_state.num2):
            st.session_state.reto_resuelto = True
            tareas_completadas += 1
            st.success("¡Correcto!")
        st.write("---")
        if st.button("🏁 ¡GUARDAR PUNTOS!"):
            if tareas_completadas > 0:
                st.session_state.puntos += (tareas_completadas * 20)
                st.balloons()
                if st.session_state.puntos >= 100:
                    st.session_state.copas += 1
                    st.session_state.puntos -= 100
                    st.session_state.reto_resuelto = False
                    st.session_state.num1 = random.randint(2, 9)
                    st.session_state.num2 = random.randint(2, 9)
        st.markdown('</div>', unsafe_allow_html=True)

    # Vestidor
    with tab2:
        st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
        st.subheader("👕 Arma tu personaje paso a paso")
        c1, c2 = st.columns(2)
        c1.selectbox("1. Sombrero/Cabeza", st.session_state.mi_armario["Cabeza"], index=st.session_state.mi_armario["Cabeza"].index(st.session_state.avatar_equipado["Cabeza"]), key="sel_cabeza", on_change=actualizar_avatar)
        c2.selectbox("2. Cara/Personaje", st.session_state.mi_armario["Cara"], index=st.session_state.mi_armario["Cara"].index(st.session_state.avatar_equipado["Cara"]), key="sel_cara", on_change=actualizar_avatar)
        c3, c4 = st.columns(2)
        c3.selectbox("3. Ropa de arriba", st.session_state.mi_armario["Camisa"], index=st.session_state.mi_armario["Camisa"].index(st.session_state.avatar_equipado["Camisa"]), key="sel_camisa", on_change=actualizar_avatar)
        c4.selectbox("4. Falda o Pantalón", st.session_state.mi_armario["Piernas"], index=st.session_state.mi_armario["Piernas"].index(st.session_state.avatar_equipado["Piernas"]), key="sel_piernas", on_change=actualizar_avatar)
        c5, c6 = st.columns(2)
        c5.selectbox("5. Medias", st.session_state.mi_armario["Medias"], index=st.session_state.mi_armario["Medias"].index(st.session_state.avatar_equipado["Medias"]), key="sel_medias", on_change=actualizar_avatar)
        c6.selectbox("6. Zapatos", st.session_state.mi_armario["Zapatos"], index=st.session_state.mi_armario["Zapatos"].index(st.session_state.avatar_equipado["Zapatos"]), key="sel_zapatos", on_change=actualizar_avatar)
        # Oración didáctica
        cara_texto = st.session_state.avatar_equipado["Cara"][2:] if len(st.session_state.avatar_equipado["Cara"])>2 else st.session_state.avatar_equipado["Cara"]
        camisa_texto = st.session_state.avatar_equipado["Camisa"][2:] if len(st.session_state.avatar_equipado["Camisa"])>2 else st.session_state.avatar_equipado["Camisa"]
        zapatos_texto = st.session_state.avatar_equipado["Zapatos"][2:] if st.session_state.avatar_equipado["Zapatos"] != "(Nada)" else "descalzo"
        oracion = f"Soy un **{cara_texto}**. Llevo puesto un(a) **{camisa_texto}** y en mis pies tengo **{zapatos_texto}**."
        st.markdown(f'<div class="oracion-didactica">📖 {oracion}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Tienda
    with tab3:
        st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
        st.header("🛍️ Boutique de Avatares (Muestra)")
        st.info("Aquí podrás comprar más faldas, zapatos y sombreros con las copas que ganes haciendo tus misiones.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Agenda
    with tab4:
        st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
        st.header("📅 Mi Planificador Divertido")
        fecha = st.date_input("Día de la misión", datetime.now())
        fecha_str = fecha.strftime("%Y-%m-%d")
        evento = st.text_input("¿Qué pasará este día?")
        if st.button("📌 Guardar Evento"):
            if evento.strip():
                if fecha_str not in st.session_state.agenda:
                    st.session_state.agenda[fecha_str] = []
                st.session_state.agenda[fecha_str].append(evento.strip())
                st.success("¡Agendado!")
            else:
                st.error("Escribe el evento antes de guardar.")
        if fecha_str in st.session_state.agenda:
            for e in st.session_state.agenda[fecha_str]:
                st.write(f"🔹 **{e}**")
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# Zona de padres en la barra lateral
# ------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔐 Zona de Padres")
pin_ingresado = st.sidebar.text_input("PIN de acceso:", type="password", key="pin_padres")
if pin_ingresado == "1234":
    st.sidebar.success("¡Acceso concedido!")
    st.sidebar.markdown("#### 🔗 Creador de Enlaces Mágicos")
    url_base = st.sidebar.text_input("URL de tu juego en la nube:", value="https://tu-enlace-real.streamlit.app")
    nuevo_correo = st.sidebar.text_input("Correo del jugador (ej. juan@email.com):")
    if nuevo_correo:
        correo_limpio = nuevo_correo.strip().lower()
        enlace_final = f"{url_base}/?correo={correo_limpio}"
        st.sidebar.markdown("**Copia este enlace y envíalo por WhatsApp:**")
        st.sidebar.code(enlace_final, language="text")
elif pin_ingresado != "":
    st.sidebar.error("PIN incorrecto.")
