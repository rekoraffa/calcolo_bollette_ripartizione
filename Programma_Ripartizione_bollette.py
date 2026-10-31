import math
import streamlit as st


def parse_number(testo, nome_campo):
    """Converte il testo in float accettando sia la virgola che il punto."""
    testo = str(testo).strip().replace(",", ".")
    if not testo:
        raise ValueError(f"Il campo '{nome_campo}' è vuoto.")
    try:
        valore = float(testo)
    except ValueError:
        raise ValueError(f"Il campo '{nome_campo}' non contiene un numero valido.")
    if not math.isfinite(valore):
        raise ValueError(f"Il campo '{nome_campo}' non contiene un numero valido.")
    return valore


def fmt(valore):
    """Formatta con 2 decimali e virgola come separatore."""
    return f"{valore:.2f}".replace(".", ",")


def scheda_inquilino(titolo, consumo, perc, importo):
    """Scheda con bordo: titolo + tre indicatori."""
    with st.container(border=True):
        st.subheader(titolo)
        st.metric("Totale consumato", f"{fmt(consumo)} kWh")
        st.metric("Percentuale consumata", f"{fmt(perc)} %")
        st.metric("Totale da saldare", f"{fmt(importo)} €")


st.title("Ripartizione bolletta tra inquilini")

# ---------------- INPUT (dentro un form: Invio = Calcola) ----------------
with st.form("form_bolletta"):
    st.subheader("Dati da inserire")
    str_ini1 = st.text_input("Lettura iniziale inquilino 1 [kWh]", placeholder="inserisci qui")
    str_fin1 = st.text_input("Lettura finale inquilino 1 [kWh]", placeholder="inserisci qui")
    str_ini2 = st.text_input("Lettura iniziale inquilino 2 [kWh]", placeholder="inserisci qui")
    str_fin2 = st.text_input("Lettura finale inquilino 2 [kWh]", placeholder="inserisci qui")
    str_bolletta = st.text_input("Bolletta ricevuta [EURO]", placeholder="inserisci qui")
    calcola = st.form_submit_button("Calcola", type="primary")

# ---------------- CALCOLO ----------------
if calcola:
    try:
        ini1 = parse_number(str_ini1, "Lettura iniziale inquilino 1")
        fin1 = parse_number(str_fin1, "Lettura finale inquilino 1")
        ini2 = parse_number(str_ini2, "Lettura iniziale inquilino 2")
        fin2 = parse_number(str_fin2, "Lettura finale inquilino 2")
        bolletta = parse_number(str_bolletta, "Bolletta ricevuta")

        consumo1 = fin1 - ini1
        consumo2 = fin2 - ini2

        if consumo1 < 0:
            raise ValueError("Inquilino 1: la lettura finale è minore di quella iniziale.")
        if consumo2 < 0:
            raise ValueError("Inquilino 2: la lettura finale è minore di quella iniziale.")
        if bolletta < 0:
            raise ValueError("La bolletta non può essere negativa.")

        totale_consumi = consumo1 + consumo2
        if totale_consumi == 0:
            raise ValueError("Il consumo totale è zero: impossibile calcolare le percentuali.")

        perc1 = consumo1 / totale_consumi * 100
        perc2 = 100 - perc1

        # Il secondo importo è calcolato per differenza: la somma torna sempre alla bolletta
        importo1 = round(bolletta * perc1 / 100, 2)
        importo2 = round(bolletta - importo1, 2)

        # ---------------- OUTPUT ----------------
        st.divider()
        st.header("Risultati")

        col1, col2 = st.columns(2)
        with col1:
            scheda_inquilino("Inquilino 1", consumo1, perc1, importo1)
        with col2:
            scheda_inquilino("Inquilino 2", consumo2, perc2, importo2)

        # Riepilogo complessivo
        with st.container(border=True):
            r1, r2 = st.columns(2)
            r1.metric("Consumo totale", f"{fmt(totale_consumi)} kWh")
            r2.metric("Bolletta ripartita", f"{fmt(importo1 + importo2)} €")

    except ValueError as e:
        st.error(str(e))