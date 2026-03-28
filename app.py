import streamlit as st

st.set_page_config(page_title="Kalkulator VAT marża PRO+", page_icon="💰", layout="centered")

st.markdown("""
<style>
.block-container {max-width: 920px; padding-top: 1rem; padding-bottom: 2rem;}
.app-shell {background: linear-gradient(180deg,#f7f8fc 0%,#eef2ff 100%); border:1px solid #e7eaf6; border-radius:26px; padding:18px;}
.hero {background: linear-gradient(135deg,#111827 0%,#1f2937 100%); color:white; border-radius:22px; padding:22px; margin-bottom:16px;}
.hero-big {font-size:38px; font-weight:800;}
.card {background:white; border:1px solid #e8ecf5; border-radius:20px; padding:16px;}
.label {font-size:13px; color:#667085;}
.value {font-size:26px; font-weight:800;}
.value-green {color:#0a7a33;} .value-red {color:#c62828;} .value-blue {color:#155eef;} .value-orange {color:#c4320a;}
</style>
""", unsafe_allow_html=True)


def pln(x): return f"{x:,.2f} zł".replace(","," ")

def to_float(x):
    try: return float(x)
    except: return 0.0

st.title("💰 Kalkulator VAT marża PRO+")

c1,c2 = st.columns(2)
with c1:
    zakup = to_float(st.text_input("Zakup (umowa)", placeholder="np. 547"))
    faktura_marza = to_float(st.text_input("Faktura VAT marża", placeholder="np. 2000"))
    koszt_brutto = to_float(st.text_input("Koszty (faktura brutto)", placeholder="np. 600"))
with c2:
    cena = to_float(st.text_input("Cena sprzedaży (na rękę)", placeholder="np. 3000"))
    koszty_dodatkowe = to_float(st.text_input("Koszty dodatkowe (bez faktury)", placeholder="np. 200"))

# --- KROK 1: ZAROBEK PRZED KOSZTAMI DODATKOWYMI ---
marza = faktura_marza - zakup
vat_marza = marza*23/123 if marza>0 else 0
vat_koszt = koszt_brutto*23/123
vat_do_zaplaty = vat_marza - vat_koszt
koszt_netto = koszt_brutto - vat_koszt

# dochód do podatków (BEZ kosztów dodatkowych)
dochod = marza - vat_marza - koszt_netto
pit = dochod*0.19 if dochod>0 else 0
zdrowotne = dochod*0.049 if dochod>0 else 0

# zarobek przed kosztami dodatkowymi
zarobek_przed = cena - zakup - koszt_brutto - max(vat_do_zaplaty,0) - pit - zdrowotne

# --- KROK 2: ODEJMUJEMY KOSZTY DODATKOWE NA TWARDO ---
zarobek_koncowy = zarobek_przed - koszty_dodatkowe

podatki = max(vat_do_zaplaty,0)+pit+zdrowotne

# --- UI ---
st.markdown("<div class='app-shell'>", unsafe_allow_html=True)

st.markdown(f"""
<div class='hero'>
<div>Zarobek końcowy</div>
<div class='hero-big {'value-green' if zarobek_koncowy>=0 else 'value-red'}'>{pln(zarobek_koncowy)}</div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='card'><div class='label'>VAT</div><div class='value value-orange'>{pln(vat_do_zaplaty)}</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='card'><div class='label'>PIT 19%</div><div class='value value-blue'>{pln(pit)}</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='card'><div class='label'>Zdrowotne</div><div class='value value-red'>{pln(zdrowotne)}</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='card'><div class='label'>Podatki razem</div><div class='value'>{pln(podatki)}</div></div>", unsafe_allow_html=True)

c5,c6,c7 = st.columns(3)
with c5:
    st.markdown(f"<div class='card'><div class='label'>Zarobek przed dodatkowymi</div><div class='value'>{pln(zarobek_przed)}</div></div>", unsafe_allow_html=True)
with c6:
    st.markdown(f"<div class='card'><div class='label'>Koszty dodatkowe</div><div class='value value-orange'>{pln(koszty_dodatkowe)}</div></div>", unsafe_allow_html=True)
with c7:
    st.markdown(f"<div class='card'><div class='label'>Cena sprzedaży</div><div class='value'>{pln(cena)}</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
