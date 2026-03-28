import streamlit as st

st.set_page_config(page_title="VAT MARŻA PRO", layout="centered")

# -------- STYLE --------
st.markdown("""
<style>
.block-container {max-width: 850px;}
.hero {
    background: linear-gradient(135deg,#111827,#1f2937);
    color: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 15px;
}
.hero-big {
    font-size: 36px;
    font-weight: 800;
}
.card {
    background: white;
    border-radius: 16px;
    padding: 15px;
    border: 1px solid #eee;
    text-align: center;
}
.label {font-size: 13px; color: #666;}
.value {font-size: 22px; font-weight: 700;}
.green {color: green;}
.red {color: red;}
.orange {color: #c4320a;}
.blue {color: #155eef;}
</style>
""", unsafe_allow_html=True)


def pln(x):
    return f"{x:,.2f} zł".replace(",", " ")


def to_float(x):
    try:
        return float(x.replace(",", "."))
    except:
        return 0.0

# -------- INPUTY --------
st.title("💰 Kalkulator VAT marża")

c1, c2 = st.columns(2)

with c1:
    zakup = to_float(st.text_input("Zakup (umowa)", placeholder="np. 547"))
    faktura = to_float(st.text_input("Faktura VAT marża (sprzedaż)", placeholder="np. 2000"))

with c2:
    koszt = to_float(st.text_input("Koszty faktura brutto", placeholder="np. 600"))

# -------- OBLICZENIA --------

# VAT
marza = faktura - zakup
vat_marza = marza * 23 / 123 if marza > 0 else 0
vat_koszt = koszt * 23 / 123
vat_do_zaplaty = vat_marza - vat_koszt

# wynik po VAT
po_vat = faktura - zakup - koszt - max(vat_do_zaplaty, 0)

# PIT + zdrowotne od wyniku po VAT
pit = po_vat * 0.19 if po_vat > 0 else 0
zdrowotne = po_vat * 0.049 if po_vat > 0 else 0

# końcowy zarobek
zarobek = po_vat - pit - zdrowotne

podatki = max(vat_do_zaplaty, 0) + pit + zdrowotne

# -------- UI --------
kolor = "green" if zarobek >= 0 else "red"

st.markdown(f"""
<div class="hero">
    <div>Zarobek końcowy</div>
    <div class="hero-big {kolor}">{pln(zarobek)}</div>
</div>
""", unsafe_allow_html=True)

# podatki
st.subheader("Podatki")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='card'><div class='label'>VAT</div><div class='value orange'>{pln(vat_do_zaplaty)}</div></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='card'><div class='label'>PIT</div><div class='value blue'>{pln(pit)}</div></div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='card'><div class='label'>Zdrowotne</div><div class='value red'>{pln(zdrowotne)}</div></div>", unsafe_allow_html=True)

with c4:
    st.markdown(f"<div class='card'><div class='label'>Razem</div><div class='value'>{pln(podatki)}</div></div>", unsafe_allow_html=True)

# podsumowanie
st.subheader("Podsumowanie")

c1, c2 = st.columns(2)

with c1:
    st.markdown(f"<div class='card'><div class='label'>Po VAT</div><div class='value'>{pln(po_vat)}</div></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='card'><div class='label'>Po podatkach</div><div class='value'>{pln(zarobek)}</div></div>", unsafe_allow_html=True)

# szczegóły
with st.expander("Szczegóły"):
    st.write("Marża:", pln(marza))
    st.write("VAT marża:", pln(vat_marza))
    st.write("VAT z kosztów:", pln(vat_koszt))
    st.write("VAT do zapłaty:", pln(vat_do_zaplaty))
    st.write("Wynik po VAT:", pln(po_vat))
    st.write("PIT:", pln(pit))
    st.write("Zdrowotne:", pln(zdrowotne))
    st.write("Zarobek końcowy:", pln(zarobek))
