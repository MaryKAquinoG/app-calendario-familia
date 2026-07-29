import streamlit as st

# ==========================================
# MAGIA: DETECTAR ENLACE DE ACCESO DIRECTO
# ==========================================
# Lee la URL para ver si alguien entró con un enlace personalizado
parametros = st.query_params

# Si el enlace tiene la palabra "correo", lo guardamos automáticamente
if "correo" in parametros:
    st.session_state.correo_jugador = parametros["correo"].lower()

# ==========================================
# PANTALLA 0: INICIO DE SESIÓN MANUAL
# ==========================================
# Esta pantalla SOLO se muestra si no entraron con un enlace directo
if 'correo_jugador' not in st.session_state:
    st.markdown('<h1 class="titulo-texto">¡Bienvenido! Inicia tu Aventura</h1>', unsafe_allow_html=True)
    st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
    
    st.write("🌟 **Acceso Libre:** Ingresa tu correo o pide a tus padres tu enlace mágico.")
    correo_input = st.text_input("📧 Ingresa tu correo electrónico:")
    
    if st.button("🔑 Entrar al Juego"):
        if "@" in correo_input and "." in correo_input:
            st.session_state.correo_jugador = correo_input.lower()
            st.rerun() 
        else:
            st.error("🛑 Ingresa un correo válido.")
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
import streamlit as st
import random
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN VISUAL INICIAL
# ==========================================
st.set_page_config(page_title="¡Planificador Divertido!", page_icon="🎮", layout="centered")

# ==========================================
# 2. INICIALIZAR MEMORIA Y ARMARIO (NUEVAS PIEZAS)
# ==========================================
if 'perfil_creado' not in st.session_state:
    st.session_state.perfil_creado = False
    st.session_state.puntos = 0
    st.session_state.copas = 15
    st.session_state.nombre = ""
    st.session_state.papa = "Papá"
    st.session_state.mama = "Mamá"
    st.session_state.fondo = "🌟 Blanco Mágico"
    
    # --- ARMARIO ACTUALIZADO: Ropa real y variada ---
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

# --- CSS MEJORADO PARA EL "TÓTEM" DE ROPA ---
st.markdown(f"""
    <style>
    .stApp {{ background: {fondo_actual}; background-attachment: fixed; transition: all 0.5s ease; }}
    
    /* AVATAR TÓTEM (Apilado de arriba a abajo) */
    .avatar-totem {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: rgba(255,255,255,0.8);
        border: 4px dashed #6495ED;
        border-radius: 40px;
        padding: 20px 10px;
        margin: 10px auto 30px auto;
        width: 250px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        animation: flotar 3s infinite ease-in-out;
    }}
    
    @keyframes flotar {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    /* MÁRGENES NEGATIVOS PARA PEGAR LAS PIEZAS */
    .p-cabeza {{ font-size: 55px; z-index: 5; margin-bottom: -15px; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2)); }}
    .p-cara {{ font-size: 90px; z-index: 4; }}
    .p-camisa {{ font-size: 75px; z-index: 3; margin-top: -20px; filter: drop-shadow(0px 3px 2px rgba(0,0,0,0.2)); }}
    .p-piernas {{ font-size: 65px; z-index: 2; margin-top: -15px; }}
    .p-medias {{ font-size: 35px; z-index: 1; margin-top: -10px; letter-spacing: -5px; }}
    .p-zapatos {{ font-size: 50px; z-index: 2; margin-top: -5px; letter-spacing: -5px; }}
    
    .titulo-texto {{ color: #FF5733; font-family: 'Comic Sans MS', cursive; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(255,255,255,0.7); text-align: center; }}
    .caja-translucida {{ background-color: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 25px; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); }}
    .oracion-didactica {{ font-size: 20px; color: #2E8B57; font-weight: bold; text-align: center; margin-top: 15px; background: #e8f5e9; padding: 10px; border-radius: 15px; border: 2px solid #a5d6a7; }}
    
    .stButton>button {{ background-color: #FFC300; color: #900C3F; font-weight: bold; border-radius: 20px; width: 100%; font-size: 18px; border: 4px solid #ff9900; transition: all 0.3s ease; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNCIONES MAGICAS DEL AVATAR (MÉTODO TÓTEM)
# ==========================================
def renderizar_avatar_html():
    cabeza = st.session_state.avatar_equipado["Cabeza"].split()[0] if st.session_state.avatar_equipado["Cabeza"] != "(Nada)" else ""
    cara = st.session_state.avatar_equipado["Cara"].split()[0]
    camisa = st.session_state.avatar_equipado["Camisa"].split()[0] if st.session_state.avatar_equipado["Camisa"] != "(Nada)" else ""
    piernas = st.session_state.avatar_equipado["Piernas"].split()[0] if st.session_state.avatar_equipado["Piernas"] != "(Nada)" else ""
    
    # Multiplicamos por 2 para que salgan dos zapatos y dos medias
    medias = (st.session_state.avatar_equipado["Medias"].split()[0] * 2) if st.session_state.avatar_equipado["Medias"] != "(Nada)" else ""
    zapatos = (st.session_state.avatar_equipado["Zapatos"].split()[0] * 2) if st.session_state.avatar_equipado["Zapatos"] != "(Nada)" else ""
    
    html = f'''
    <div class="avatar-totem">
        <div class="p-cabeza">{cabeza}</div>
        <div class="p-cara">{cara}</div>
        <div class="p-camisa">{camisa}</div>
        <div class="p-piernas">{piernas}</div>
        <div class="p-medias">{medias}</div>
        <div class="p-zapatos">{zapatos}</div>
    </div>
    '''
    return html

def actualizar_avatar():
    st.session_state.avatar_equipado["Cara"] = st.session_state.sel_cara
    st.session_state.avatar_equipado["Cabeza"] = st.session_state.sel_cabeza
    st.session_state.avatar_equipado["Camisa"] = st.session_state.sel_camisa
    st.session_state.avatar_equipado["Piernas"] = st.session_state.sel_piernas
    st.session_state.avatar_equipado["Medias"] = st.session_state.sel_medias
    st.session_state.avatar_equipado["Zapatos"] = st.session_state.sel_zapatos

# ==========================================
# PANTALLA 1: CREACIÓN DE PERFIL INICIAL
# ==========================================
if not st.session_state.perfil_creado:
    st.markdown('<h1 class="titulo-texto">¡Crea tu Cuenta de Jugador!</h1>', unsafe_allow_html=True)
    st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
    
    st.session_state.nombre = st.text_input("📝 ¿Cómo te llamas?")
    colP, colM = st.columns(2)
    st.session_state.papa = colP.text_input("👨 Nombre de Papá (Opcional):", "Papá")
    st.session_state.mama = colM.text_input("👩 Nombre de Mamá (Opcional):", "Mamá")
    st.session_state.fondo = st.selectbox("🎨 Escoge el fondo de tu app", list(colores_fondos.keys()))
    
    if st.button("🚀 ¡ENTRAR AL JUEGO!"):
        if st.session_state.nombre != "":
            st.session_state.perfil_creado = True
            st.rerun() 
        else:
            st.error("🛑 Debes poner tu nombre para iniciar.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PANTALLA 2: EL JUEGO PRINCIPAL
# ==========================================
else:
    # EL AVATAR TÓTEM SIEMPRE VISIBLE ARRIBA
    st.markdown(renderizar_avatar_html(), unsafe_allow_html=True)
    
    st.markdown(f'''
        <div style="text-align:center; margin-bottom:20px;">
            <h2 class="titulo-texto">¡A jugar, {st.session_state.nombre}!</h2>
            <div style="font-size:22px; color:#E67E22; font-weight:bold;">Tus Monedas: {st.session_state.copas} 🏆</div>
        </div>
    ''', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎮 Misiones", "👕 Vestidor", "🛍️ Tienda", "📅 Agenda"])

    # ------------------------------------------
    # PESTAÑA 1: MISIONES (Sin cambios)
    # ------------------------------------------
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

    # ------------------------------------------
    # PESTAÑA 2: EL NUEVO VESTIDOR DIDÁCTICO
    # ------------------------------------------
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
        
        # Oración didáctica generada automáticamente
        cara_texto = st.session_state.avatar_equipado["Cara"][2:]
        camisa_texto = st.session_state.avatar_equipado["Camisa"][2:]
        zapatos_texto = st.session_state.avatar_equipado["Zapatos"][2:] if st.session_state.avatar_equipado["Zapatos"] != "(Nada)" else "descalzo"
        
        oracion = f"Soy un **{cara_texto}**. Llevo puesto un(a) **{camisa_texto}** y en mis pies tengo **{zapatos_texto}**."
        st.markdown(f'<div class="oracion-didactica">📖 {oracion}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------
    # PESTAÑA 3 Y 4: TIENDA Y AGENDA
    # ------------------------------------------
    with tab3:
        st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
        st.header("🛍️ Boutique de Avatares (Muestra)")
        st.info("Aquí podrás comprar más faldas, zapatos y sombreros con las copas que ganes haciendo tus misiones.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="caja-translucida">', unsafe_allow_html=True)
        st.header("📅 Mi Planificador Divertido")
        fecha = st.date_input("Día de la misión", datetime.now())
        fecha_str = fecha.strftime("%Y-%m-%d")
        evento = st.text_input("¿Qué pasará este día?")
        if st.button("📌 Guardar Evento"):
            if fecha_str not in st.session_state.agenda:
                st.session_state.agenda[fecha_str] = []
            st.session_state.agenda[fecha_str].append(evento)
            st.success("¡Agendado!")
        if fecha_str in st.session_state.agenda:
            for e in st.session_state.agenda[fecha_str]:
                st.write(f"🔹 **{e}**")
        st.markdown('</div>', unsafe_allow_html=True)
        # ==========================================
# 🔐 ZONA DE PADRES: GENERADOR DE ENLACES
# ==========================================
# Creamos una línea separadora en el menú lateral
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔐 Zona de Padres")

# Pedimos el PIN (se mostrará con puntitos por privacidad)
pin_ingresado = st.sidebar.text_input("PIN de acceso:", type="password", key="pin_padres")

# Verificamos si el PIN es correcto
if pin_ingresado == "1234":
    st.sidebar.success("¡Acceso concedido!")
    st.sidebar.markdown("#### 🔗 Creador de Enlaces Mágicos")
    
    # 1. Pedimos la URL real de tu juego en Streamlit
    url_base = st.sidebar.text_input(
        "URL de tu juego en la nube:", 
        value="https://tu-enlace-real.streamlit.app"
    )
    
    # 2. Pedimos el correo del niño
    nuevo_correo = st.sidebar.text_input("Correo del jugador (ej. juan@email.com):")
    
    # 3. Si escribiste un correo, generamos el enlace
    if nuevo_correo:
        # Limpiamos el correo (quitamos espacios extra y lo ponemos en minúsculas)
        correo_limpio = nuevo_correo.strip().lower()
        
        # Unimos la URL con el parámetro del correo
        enlace_final = f"{url_base}/?correo={correo_limpio}"
        
        st.sidebar.markdown("**Copia este enlace y envíalo por WhatsApp:**")
        # st.code crea un cuadro muy bonito con un botón de "Copiar" automático
        st.sidebar.code(enlace_final, language="text")

elif pin_ingresado != "":
    # Si escriben algo pero no es 1234, mostramos error
    st.sidebar.error("PIN incorrecto.")