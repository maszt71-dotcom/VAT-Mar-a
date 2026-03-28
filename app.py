import streamlit as st

st.set_page_config(page_title="Kalkulator VAT marża PRO+", page_icon="💰", layout="centered")

st.markdown("""
<style>
.block-container {
    max-width: 920px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}
.app-shell {
    background: linear-gradient(180deg,#f7f8fc 0%,#eef2ff 100%);
    border: 1px solid #e7eaf6;
    border-radius: 26px;
    padding: 18px;
    box-shadow: 0 12px 30px rgba(36,41,61,0.08);
}
.hero {
    background: linear-gradient(135deg,#111827 0%,#1f2937 100%);
    color: white;
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 16px;
}
.hero-small {
    opacity: 0.82;
    font-size: 14px;
    margin-bottom: 6px;
}
.hero-big {
    font-size: 38px;
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
}
.card {
    background: white;
    border: 1px solid #e8ecf5;
    border-radius: 20px;
    padding: 16px;
    min-height: 120px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}
.label {
    font-size: 13px;
    color: #667085;
    margin-bottom: 8px;
}
.value {
    font-size: 26px;
    font-weight: 800;
    line-height: 1.15;
    color: #101828;
}
.value-green { color: #0a7a33; }
.value-red { color: #c62828; }
.value-blue { color: #155eef; }
.value-orange { color: #c4320a; }
.subvalue {
    margin-top: 8px;
    font-size: 12px;
    color: #667085;
}
.section-title {
    font-size: 15px;
    font-weight: 700;
    color: #344054;
    margin: 12px 0 10px 2px;
}
.pill-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
}
.pill {
    background: white;
    border: 1px solid #e8ecf5;
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 13px;
    color: #475467;
}
</style>
""", unsafe_allow_html=True)


def pln(x: float) -> str:
    return f"{x:,.2f} zł".replace(",", " ")


def to_float(x: str) -> float:
    try:
        x = x.replace(",", ".").strip()
        return float(x) if x else 0.0
    except Exception:
        return 0.0


st.title("💰 Kalkulator VAT marża PRO+")
st.caption("Cena sprzedaży = cena na rękę")

col1, col2 = st.columns(2)

with col1:
    zakup = to_float(st.text_input("Zakup (umowa)", placeholder="np. 547"))
    faktura_marza = to_float(st.text_input("Faktura VAT marża", placeholder="np. 2000"))
    koszt_brutto = to_float(st.text_input("Koszty (faktura brutto 23%)", placeholder="np. 600"))

with col2:
    cena_sprzedazy = to_float(st.text_input("Cena sprzedaży (na rękę)", placeholder="np. 3000"))
    koszty_dodatkowe = to_float(st.text_input("Koszty dodatkowe bez faktury", placeholder="np. 200"))

# --- VAT ---
marza = faktura_marza - zakup
vat_marza = marza * 23 / 123 if marza > 0 else 0.0
vat_z_kosztow = koszt_brutto * 23 / 123 if koszt_brutto > 0 else 0.0
vat_do_zaplaty = vat_marza - vat_z_kosztow

# --- zarobek przed kosztami dodatkowymi ---
zarobek_przed_dodatkowymi = cena_sprzedazy - zakup - koszt_brutto - max(vat_do_zaplaty, 0)

# --- podatki od zarobku przed dodatkowymi ---
pit = zarobek_przed_dodatkowymi * 0.19 if zarobek_przed_dodatkowymi > 0 else 0.0
zdrowotne = zarobek_przed_dodatkowymi * 0.049 if zarobek_przed_dodatkowymi > 0 else 0.0

# --- zarobek po podatkach ---
zarobek_po_podatkach = zarobek_przed_dodatkowymi - pit - zdrowotne

# --- koszty dodatkowe odejmowane na twardo ---
zarobek_koncowy = zarobek_po_podatkach - koszty_dodatkowe

podatki_razem = max(vat_do_zaplaty, 0) + pit + zdrowotne

kolor_zarobek = "value-green" if zarobek_koncowy >= 0 else "value-red"
kolor_vat = "value-orange" if vat_do_zaplaty > 0 else "value-green"

st.markdown("<div class='app-shell'>", unsafe_allow_html=True)

st.markdown(f"""
<div class='hero'>
    <div class='hero-small'>Zarobek końcowy</div>
    <div class='hero-big {kolor_zarobek}'>{pln(zarobek_koncowy)}</div>
    <div class='pill-row'>
        <div class='pill'>Cena sprzedaży: {pln(cena_sprzedazy)}</div>
        <div class='pill'>Faktura VAT marża: {pln(faktura_marza)}</div>
        <div class='pill'>Zakup: {pln(zakup)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Podatki do zapłaty</div>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='card'>
        <div class='label'>VAT do zapłaty</div>
        <div class='value {kolor_vat}'>{pln(vat_do_zaplaty)}</div>
        <div class='subvalue'>VAT marża − VAT z kosztów</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='card'>
        <div class='label'>PIT liniowy 19%</div>
        <div class='value value-blue'>{pln(pit)}</div>
        <div class='subvalue'>Liczony od zarobku przed dodatkowymi</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='card'>
        <div class='label'>Zdrowotne 4,9%</div>
        <div class='value value-red'>{pln(zdrowotne)}</div>
        <div class='subvalue'>Liczone od zarobku przed dodatkowymi</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='card'>
        <div class='label'>Podatki razem</div>
        <div class='value'>{pln(podatki_razem)}</div>
        <div class='subvalue'>VAT + PIT + zdrowotne</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='section-title'>Podsumowanie</div>", unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)

with d1:
    st.markdown(f"""
    <div class='card'>
        <div class='label'>Zarobek przed dodatkowymi</div>
        <div class='value'>{pln(zarobek_przed_dodatkowymi)}</div>
        <div class='subvalue'>Przed PIT, zdrowotnym i kosztami dodatkowymi</div>
    </div>
    """, unsafe_allow_html=True)

with d2:
    st.markdown(f"""
    <div class='card'>
        <div class='label'>Koszty dodatkowe</div>
        <div class='value value-orange'>{pln(koszty_dodatkowe)}</div>
        <div class='subvalue'>Odejmowane na twardo na końcu</div>
    </div>
    """, unsafe_allow_html=True)

with d3:
    st.markdown(f"""
    <div class='card'>
        <div class='label'>Zarobek po podatkach</div>
        <div class='value'>{pln(zarobek_po_podatkach)}</div>
        <div class='subvalue'>Przed odjęciem kosztów dodatkowych</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("Pokaż szczegóły obliczeń"):
    st.write(f"**Zakup (umowa):** {pln(zakup)}")
    st.write(f"**Faktura VAT marża:** {pln(faktura_marza)}")
    st.write(f"**Cena sprzedaży (na rękę):** {pln(cena_sprzedazy)}")
    st.write(f"**Koszty brutto:** {pln(koszt_brutto)}")
    st.write(f"**Koszty dodatkowe bez faktury:** {pln(koszty_dodatkowe)}")
    st.write(f"**Marża:** {pln(marza)}")
    st.write(f"**VAT marża:** {pln(vat_marza)}")
    st.write(f"**VAT z kosztów:** {pln(vat_z_kosztow)}")
    st.write(f"**VAT do zapłaty:** {pln(vat_do_zaplaty)}")
    st.write(f"**Zarobek przed dodatkowymi:** {pln(zarobek_przed_dodatkowymi)}")
    st.write(f"**PIT liniowy:** {pln(pit)}")
    st.write(f"**Zdrowotne:** {pln(zdrowotne)}")
    st.write(f"**Zarobek po podatkach:** {pln(zarobek_po_podatkach)}")
    st.write(f"**Zarobek końcowy:** {pln(zarobek_koncowy)}")

if zarobek_koncowy < 0:
    st.error("Na tej transakcji wychodzisz na minus.")
else:
    st.success("Wynik policzony poprawnie z wpisanych danych.")

st.markdown("</div>", unsafe_allow_html=True)
