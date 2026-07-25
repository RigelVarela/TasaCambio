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


# 2. CARGA AUTOMÁTICA Y CACHÉ
@st.cache_data(ttl=1800)  # Guarda los datos en memoria por 30 minutos
def obtener_tasas_automaticas():
    # BCV USD
    try:
        bcv = float(requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=5).json().get("promedio", 0.0))
    except:
        bcv = 0.0

    # BCV EUR
    try:
        euro = float(requests.get("https://ve.dolarapi.com/v1/euros/oficial", timeout=5).json().get("promedio", 0.0))
    except:
        euro = 0.0

    # Binance USDT
    try:
        p2p_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        data = {
            "asset": "USDT", "fiat": "VES", "merchantCheck": True,
            "page": 1, "payTypes": [], "publisherType": None,
            "rows": 1, "tradeType": "BUY"
        }
        response = requests.post(p2p_url, json=data, timeout=5)
        binance = float(response.json()['data'][0]['adv']['price'])
    except:
        binance = 0.0

    return bcv, euro, binance


# 3. MANEJO DE ESTADO Y AUTO-CARGA
if 'bcv' not in st.session_state: st.session_state.bcv = 0.0
if 'euro' not in st.session_state: st.session_state.euro = 0.0
if 'binance' not in st.session_state: st.session_state.binance = 0.0

# Se ejecuta automáticamente si los valores están en cero
if st.session_state.bcv == 0.0:
    with st.spinner("Conectando con BCV y Binance..."):
        b, e, bin_rate = obtener_tasas_automaticas()
        st.session_state.bcv = b
        st.session_state.euro = e
        st.session_state.binance = bin_rate

# 4. INTERFAZ DE USUARIO
st.title("💱 Monitor y Calculadora Cambiaria")
st.markdown("Consulta las tasas en tiempo real y calcula la brecha del mercado.")

# Botón opcional solo por si el usuario quiere forzar la actualización antes de los 30 min
if st.button("🔄 Forzar Actualización Manual", use_container_width=True):
    obtener_tasas_automaticas.clear()  # Limpia la caché
    with st.spinner("Actualizando tasas..."):
        b, e, bin_rate = obtener_tasas_automaticas()
        st.session_state.bcv = b
        st.session_state.euro = e
        st.session_state.binance = bin_rate
    st.rerun()

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

# 5. CONVERSOR BIDIRECCIONAL
st.subheader("Conversor Rápido")
col_usd, col_bs = st.columns(2)

# Columna Izquierda: De Dólares a Bolívares
with col_usd:
    monto_usd = st.number_input("Tengo Dólares ($)", min_value=0.0, format="%.2f")

    if st.session_state.bcv > 0 and st.session_state.binance > 0 and monto_usd > 0:
        eq_bcv = monto_usd * st.session_state.bcv
        eq_binance = monto_usd * st.session_state.binance
        eq_euro = monto_usd * st.session_state.euro

        st.metric("Valor a Tasa BCV", f"{eq_bcv:.2f} Bs")
        st.metric("Valor a Tasa Binance", f"{eq_binance:.2f} Bs")
        st.metric("Valor a Tasa Euro BCV", f"{eq_euro:.2f} Bs")

        # Botón de WhatsApp integrado al cálculo en USD
        mensaje_wa = (
            f"📊 *Cálculo Cambiario*\n"
            f"Monto: ${monto_usd:.2f}\n\n"
            f"*Tasas del día:*\n"
            f"🇺🇸 BCV: {st.session_state.bcv:.2f} Bs\n"
            f"🇪🇺 BCV EURO: {st.session_state.euro:.2f} Bs\n"
            f"🟡 Binance: {st.session_state.binance:.2f} Bs\n\n"
            f"*Total a pagar/recibir:*\n"
            f"➡️ BCV: {eq_bcv:.2f} Bs\n"
            f"➡️ BCV EURO: {eq_euro:.2f} Bs\n"
            f"➡️ Binance: {eq_binance:.2f} Bs"
        )
        mensaje_codificado = urllib.parse.quote(mensaje_wa)
        st.link_button("📲 Compartir por WhatsApp", f"https://api.whatsapp.com/send?text={mensaje_codificado}",
                       type="primary", use_container_width=True)

# Columna Derecha: De Bolívares a Dólares/Euros
with col_bs:
    monto_bs = st.number_input("Tengo Bolívares (Bs)", min_value=0.0, format="%.2f")

    if st.session_state.bcv > 0 and st.session_state.binance > 0 and monto_bs > 0:
        eq_usd_bcv = monto_bs / st.session_state.bcv
        eq_usd_binance = monto_bs / st.session_state.binance
        eq_eur_bcv = monto_bs / st.session_state.euro if st.session_state.euro > 0 else 0

        st.metric("Equivalente USD (Tasa BCV)", f"${eq_usd_bcv:.2f}")
        st.metric("Equivalente USD (Tasa Binance)", f"${eq_usd_binance:.2f}")
        st.metric("Equivalente EUR (Tasa BCV)", f"€{eq_eur_bcv:.2f}")

st.divider()

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