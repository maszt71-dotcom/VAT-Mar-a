import streamlit as st

st.set_page_config(page_title="VAT MARŻA PRO", layout="centered")

st.markdown("""
<style>
.block-container {max-width: 900px; padding-top: 1rem; padding-bottom: 2rem;}
.hero {
    background: linear-gradient(135deg,#111827,#1f2937);
    color:white;
    padding:20px;
    border-radius:20px;
    margin-bottom:18px;
}
.hero-split {
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}
.hero-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 14px;
}
.hero-small {font-size:14px; opacity:0.85; margin-bottom:6px;}
.hero-big {font-size:36px; font-weight:800;}
.card {background:white; border-radius:16px; padding:16px; border:1px solid #eee; text-align:center; min-height:110px;}
.label {font-size:13px; color:#666; margin-bottom:8px;}
.value {font-size:24px; font-weight:700;}
.green {color: green;} .red {color: red;} .orange {color:#c4320a;} .blue {color:#155eef;}
</style>
""", unsafe_allow_html=True)


def pln(x):
    znak = "+" if x > 0 else ""
    return f"{znak}{x:,.2f} zł".replace(",", " ")


def to_float(x):
    try:
        x = x.replace(",", ".").strip()
        return float(x) if x else 0.0
    except:
        return 0.0

st.title("💰 Kalkulator VAT marża")

# INPUTY (liczy się od razu)
c1, c2, c3 = st.columns(3)
with c1:
    zakup = to_float(st.text_input("Zakup (umowa)", placeholder="np. 547"))
with c2:
    koszt = to_float(st.text_input("Koszty faktura brutto", placeholder="np. 600"))
with c3:
    sprzedaz = to_float(st.text_input("Cena sprzedaży", placeholder="np. 2000"))

kasa_reka = to_float(st.text_input("Kasa do ręki", placeholder="np. 2000"))
koszty_gotowkowe = to_float(st.text_input("Koszty gotówkowe", placeholder="np. 150"))

# OBLICZENIA (zawsze aktywne)
marza = sprzedaz - zakup
vat_marza = marza * 23 / 123 if marza > 0 else 0.0
vat_z_kosztow = koszt * 23 / 123 if koszt > 0 else 0.0
vat_do_zaplaty = vat_marza - vat_z_kosztow

po_vat = sprzedaz - zakup - koszt - max(vat_do_zaplaty, 0)
pit = po_vat * 0.19 if po_vat > 0 else 0.0
zdrowotne = po_vat * 0.049 if po_vat > 0 else 0.0
zarobek = po_vat - pit - zdrowotne

podatki = max(vat_do_zaplaty, 0) + pit + zdrowotne
zakup_koszty_podatki = zakup + koszt + podatki
wszystko = kasa_reka - podatki - zakup - koszt - koszty_gotowkowe

# FORMUŁA
tyle_wyszlo = wszystko - podatki - zakup - koszt - koszty_gotowkowe

# UI
kolor = "green" if zarobek >= 0 else "red"
kolor_tyle = "green" if tyle_wyszlo >= 0 else "red"

st.markdown(f"""
<div class="hero">
    <div class="hero-split">
        <div class="hero-box">
            <div class="hero-small">Zarobek końcowy</div>
            <div class="hero-big {kolor}">{pln(zarobek)}</div>
        </div>
        <div class="hero-box">
            <div class="hero-small">Tyle wyszło</div>
            <div class="hero-big {kolor_tyle}">{pln(tyle_wyszlo)}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("Podatki")

a, b, c, d = st.columns(4)
with a:
    st.markdown(f"<div class='card'><div class='label'>VAT</div><div class='value orange'>{pln(vat_do_zaplaty)}</div></div>", unsafe_allow_html=True)
with b:
    st.markdown(f"<div class='card'><div class='label'>PIT</div><div class='value blue'>{pln(pit)}</div></div>", unsafe_allow_html=True)
with c:
    st.markdown(f"<div class='card'><div class='label'>Zdrowotne</div><div class='value red'>{pln(zdrowotne)}</div></div>", unsafe_allow_html=True)
with d:
    st.markdown(f"<div class='card'><div class='label'>Razem</div><div class='value'>{pln(podatki)}</div></div>", unsafe_allow_html=True)

st.subheader("Koszty")

k1, k2 = st.columns(2)
with k1:
    st.markdown(f"<div class='card'><div class='label'>Zakup + koszty + podatki</div><div class='value'>{pln(zakup_koszty_podatki)}</div></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='card'><div class='label'>Kasa do ręki - wszystko</div><div class='value'>{pln(wszystko)}</div></div>", unsafe_allow_html=True)

with st.expander("Szczegóły"):
    st.write("Zarobek:", pln(zarobek))
    st.write("Tyle wyszło:", pln(tyle_wyszlo))
