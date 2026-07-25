import streamlit as st
import pandas as pd
import requests
import urllib.parse

# 1. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Calculadora Cambiaria", page_icon="💱", layout="centered")

# CSS personalizado para hacer la interfaz más atractiva
st.markdown("""
    <style>
    .tarjeta-metrica {
        background-color: #1E1E2E;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
        text-align: center;
        border-top: 4px solid #00E676;
        margin-bottom: 20px;
    }
    .tarjeta-titulo {
        color: #A6ACCD;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .tarjeta-valor {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: bold;
        margin-top: 8px;
    }
    .alerta-brecha {
        color: #FF5252;
    }
    </style>
""", unsafe_allow_html=True)


# 2. FUNCIONES DE API
def obtener_datos_bcv():
    try:
        res = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=5).json()
        return float(res.get("promedio", 0.0))
    except Exception:
        return 0.0


def obtener_datos_euro():
    try:
        res = requests.get("https://ve.dolarapi.com/v1/euros/oficial", timeout=5).json()
        return float(res.get("promedio", 0.0))
    except Exception:
        return 0.0


def obtener_tasa_binance():
    p2p_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    data = {
        "asset": "USDT", "fiat": "VES", "merchantCheck": True,
        "page": 1, "payTypes": [], "publisherType": None,
        "rows": 1, "tradeType": "BUY"
    }
    try:
        response = requests.post(p2p_url, json=data, timeout=5)
        precio = response.json()['data'][0]['adv']['price']
        return float(precio)
    except Exception:
        return 0.0


# 3. MANEJO DE ESTADO
if 'bcv' not in st.session_state: st.session_state.bcv = 0.0
if 'euro' not in st.session_state: st.session_state.euro = 0.0
if 'binance' not in st.session_state: st.session_state.binance = 0.0


def actualizar_tasas():
    with st.spinner("Conectando con BCV y Binance..."):
        st.session_state.bcv = obtener_datos_bcv()
        st.session_state.euro = obtener_datos_euro()
        st.session_state.binance = obtener_tasa_binance()
    st.toast('¡Tasas actualizadas exitosamente!', icon='✅')


# 4. INTERFAZ DE USUARIO
st.title("💱 Monitor y Calculadora Cambiaria")
st.markdown("Consulta las tasas en tiempo real y calcula la brecha del mercado.")

# Botón de actualización
st.button("🔄 Actualizar Tasas Ahora", on_click=actualizar_tasas, use_container_width=True)

# Tarjetas visuales de las tasas
st.subheader("Tasas Actuales")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="tarjeta-metrica">
        <div class="tarjeta-titulo">🇺🇸 BCV (USD)</div>
        <div class="tarjeta-valor">{st.session_state.bcv:.2f} Bs</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="tarjeta-metrica">
        <div class="tarjeta-titulo">🇪🇺 BCV (EUR)</div>
        <div class="tarjeta-valor">{st.session_state.euro:.2f} Bs</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="tarjeta-metrica" style="border-top-color: #F3BA2F;">
        <div class="tarjeta-titulo">🟡 Binance (USDT)</div>
        <div class="tarjeta-valor">{st.session_state.binance:.2f} Bs</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 5. CONVERSOR Y ANÁLISIS
st.subheader("Conversor Rápido")
monto_usd = st.number_input("Ingresa monto en Dólares ($)", min_value=0.0, format="%.2f")

if st.session_state.bcv > 0 and st.session_state.binance > 0 and monto_usd > 0:
    # Cálculos
    eq_bcv = monto_usd * st.session_state.bcv
    eq_binance = monto_usd * st.session_state.binance
    eq_euro = monto_usd * st.session_state.euro

    # Mostrar métricas en pantalla
    c1, c2, c3 = st.columns(3)
    c1.metric("Valor a Tasa BCV", f"{eq_bcv:.2f} Bs")
    c2.metric("Valor a Tasa Binance", f"{eq_binance:.2f} Bs")
    c3.metric("Valor a Tasa Euro BCV", f"{eq_euro:.2f} Bs")

    st.write("")  # Un pequeño espacio visual

    # --- LÓGICA DEL BOTÓN DE WHATSAPP ---
    # Armamos el mensaje con formato para WhatsApp (*negritas* y saltos de línea)
    mensaje_wa = (
        f"📊 *Cálculo Cambiario*\n"
        f"Monto: ${monto_usd:.2f}\n\n"
        f"*Tasas del día:*\n"
        f"🇺🇸 BCV: {st.session_state.bcv:.2f} Bs\n"
        f"🇪🇺 BCV EURO: {st.session_state.euro:.2f} Bs\n"
        f"🟡 Binance: {st.session_state.binance:.2f} Bs\n\n"
        f"*Total a pagar/recibir:*\n"
        f"➡️ BCV: {eq_bcv:.2f} Bs\n"
        f"➡️ BCV: {eq_euro:.2f} Bs\n"
        f"➡️ Binance: {eq_binance:.2f} Bs"
    )

    # Codificamos el mensaje para que sea una URL válida
    mensaje_codificado = urllib.parse.quote(mensaje_wa)

    # Creamos el enlace final
    url_wa = f"https://api.whatsapp.com/send?text={mensaje_codificado}"

    # Mostramos el botón
    st.link_button("📲 Compartir por WhatsApp", url_wa, type="primary", use_container_width=True)

# 6. ANÁLISIS DE BRECHA Y ESCENARIOS
if st.session_state.bcv > 0 and st.session_state.binance > 0:
    st.subheader("Análisis de Brecha Cambiaria")

    diferencial_pct = ((st.session_state.binance / st.session_state.bcv) - 1) * 100
    brecha_bs = st.session_state.binance - st.session_state.bcv
    impacto_usd = brecha_bs / st.session_state.bcv

    ca, cb, cc = st.columns(3)
    ca.metric("Diferencial", f"{diferencial_pct:.2f}%")
    cb.metric("Brecha por $", f"{brecha_bs:.2f} Bs")
    cc.metric("Impacto en Valor", f"${impacto_usd:.2f}")

    # Tabla de pérdida de poder adquisitivo
    st.markdown("### Escenarios de Poder Adquisitivo")
    escenarios = [10, 50, 100]
    data = []

    for monto in escenarios:
        bs_bcv = monto * st.session_state.bcv
        bs_binance = monto * st.session_state.binance
        data.append({
            "Escenario": f"${monto}",
            "Costo BCV (Bs)": round(bs_bcv, 2),
            "Costo Binance (Bs)": round(bs_binance, 2),
            "Diferencia (Bs)": round(bs_binance - bs_bcv, 2),
            "Pérdida Real (USD)": round((bs_binance - bs_bcv) / st.session_state.bcv, 2)
        })

    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)