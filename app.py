import streamlit as st

st.set_page_config(page_title="Kalkulator VAT marża PRO", page_icon="💰", layout="centered")

# ---------- STYLE ----------
st.markdown(
    """
    <style>
    .main {padding-top: 1rem;}
    .block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 760px;}
    h1, h2, h3 {margin-bottom: 0.3rem;}
    .big-number {
        font-size: 34px;
        font-weight: 700;
        padding: 14px 18px;
        border-radius: 14px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 12px;
    }
    .good {
        background: #e8f7ec;
        color: #146c2e;
        border: 1px solid #b7e4c3;
    }
    .bad {
        background: #fdecec;
        color: #a61b1b;
        border: 1px solid #f2b5b5;
    }
    .card {
        border: 1px solid #e6e6e6;
        border-radius: 14px;
        padding: 14px 16px;
        background: #ffffff;
        margin-bottom: 10px;
    }
    .small-note {
        color: #666;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HELPERS ----------
def pln(x: float) -> str:
    return f"{x:,.2f} zł".replace(",", " ")


def netto_z_brutto_23(brutto: float) -> float:
    return brutto / 1.23 if brutto > 0 else 0.0


def vat_z_brutto_23(brutto: float) -> float:
    return brutto - netto_z_brutto_23(brutto) if brutto > 0 else 0.0


def licz_kalkulacje(zakup_umowa: float, sprzedaz: float, koszty_faktura_brutto: float, inne_koszty: float):
    # VAT marża liczony od różnicy sprzedaż - zakup na umowę
    marza_brutto = sprzedaz - zakup_umowa
    vat_marza = (marza_brutto * 23 / 123) if marza_brutto > 0 else 0.0

    # Koszt z faktury
    koszt_netto = netto_z_brutto_23(koszty_faktura_brutto)
    vat_z_kosztow = vat_z_brutto_23(koszty_faktura_brutto)

    # VAT do zapłaty według Twojego założenia: VAT marża - VAT z kosztów
    vat_do_zaplaty = vat_marza - vat_z_kosztow

    # Dochód do PIT i zdrowotnego
    dochod = marza_brutto - vat_marza - koszt_netto - inne_koszty
    pit_liniowy = dochod * 0.19 if dochod > 0 else 0.0
    zdrowotne = dochod * 0.049 if dochod > 0 else 0.0

    podatki_razem = vat_do_zaplaty + pit_liniowy + zdrowotne
    na_reke = dochod - pit_liniowy - zdrowotne
    koszt_calkowity = zakup_umowa + koszty_faktura_brutto + inne_koszty + max(vat_do_zaplaty, 0) + pit_liniowy + zdrowotne

    return {
        "marza_brutto": marza_brutto,
        "vat_marza": vat_marza,
        "koszt_netto": koszt_netto,
        "vat_z_kosztow": vat_z_kosztow,
        "vat_do_zaplaty": vat_do_zaplaty,
        "dochod": dochod,
        "pit_liniowy": pit_liniowy,
        "zdrowotne": zdrowotne,
        "podatki_razem": podatki_razem,
        "na_reke": na_reke,
        "koszt_calkowity": koszt_calkowity,
    }


def licz_max_zakup(sprzedaz: float, koszty_faktura_brutto: float, inne_koszty: float, target_na_reke: float):
    # Szukanie metodą prób dla maksymalnego zakupu, który zostawi target na rękę
    low = 0.0
    high = max(sprzedaz, 1.0)

    for _ in range(80):
        mid = (low + high) / 2
        wynik = licz_kalkulacje(mid, sprzedaz, koszty_faktura_brutto, inne_koszty)
        if wynik["na_reke"] >= target_na_reke:
            low = mid
        else:
            high = mid
    return low


# ---------- HEADER ----------
st.title("💰 Kalkulator VAT marża PRO")
st.caption("Szybki kalkulator pod handel autem: VAT marża, koszt z faktury, PIT liniowy i zdrowotne.")

# ---------- INPUTS ----------
with st.form("kalkulator_form"):
    st.subheader("Dane")
    zakup_umowa = st.number_input("Zakup na umowę", min_value=0.0, value=547.0, step=100.0)
    sprzedaz = st.number_input("Cena sprzedaży", min_value=0.0, value=2000.0, step=100.0)
    koszty_faktura_brutto = st.number_input("Koszty z faktury brutto (23%)", min_value=0.0, value=600.0, step=100.0)
    inne_koszty = st.number_input("Inne koszty bez faktury / dodatkowe wydatki", min_value=0.0, value=0.0, step=100.0)

    submitted = st.form_submit_button("Oblicz")

# ---------- CALCULATIONS ----------
if submitted or True:
    wynik = licz_kalkulacje(zakup_umowa, sprzedaz, koszty_faktura_brutto, inne_koszty)

    # Główna liczba
    na_reke_class = "good" if wynik["na_reke"] >= 0 else "bad"
    st.markdown(
        f"<div class='big-number {na_reke_class}'>Na rękę: {pln(wynik['na_reke'])}</div>",
        unsafe_allow_html=True,
    )

    # Krótkie kafelki
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='card'><b>VAT do zapłaty</b><br>{pln(wynik['vat_do_zaplaty'])}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><b>PIT liniowy 19%</b><br>{pln(wynik['pit_liniowy'])}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><b>Zdrowotne 4,9%</b><br>{pln(wynik['zdrowotne'])}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><b>Podatki razem</b><br>{pln(wynik['podatki_razem'])}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Szczegóły")

    st.write(f"**Marża brutto:** {pln(wynik['marza_brutto'])}")
    st.write(f"**VAT marża:** {pln(wynik['vat_marza'])}")
    st.write(f"**VAT z kosztów:** {pln(wynik['vat_z_kosztow'])}")
    st.write(f"**Koszt netto z faktury:** {pln(wynik['koszt_netto'])}")
    st.write(f"**Dochód do PIT i zdrowotnego:** {pln(wynik['dochod'])}")
    st.write(f"**Łączny koszt z podatkami:** {pln(wynik['koszt_calkowity'])}")

    if wynik["vat_do_zaplaty"] < 0:
        st.info("VAT do zapłaty wyszedł ujemny, bo VAT z kosztów jest większy niż VAT marża.")

    if wynik["dochod"] < 0:
        st.warning("Dochód jest ujemny — PIT i zdrowotne zostały policzone jako 0.")

    st.markdown("---")
    st.subheader("Ile mogę maksymalnie kupić?")
    target_na_reke = st.number_input("Ile chcesz, żeby zostało na rękę", min_value=0.0, value=500.0, step=100.0)
    max_zakup = licz_max_zakup(sprzedaz, koszty_faktura_brutto, inne_koszty, target_na_reke)
    st.success(f"Maksymalny zakup przy tej sprzedaży, żeby zostało około {pln(target_na_reke)}: {pln(max_zakup)}")

    st.markdown("---")
    st.subheader("Szybki podgląd")
    st.markdown(
        f"""
        <div class='card'>
        <b>Zakup:</b> {pln(zakup_umowa)}<br>
        <b>Sprzedaż:</b> {pln(sprzedaz)}<br>
        <b>Koszty brutto:</b> {pln(koszty_faktura_brutto)}<br>
        <b>Inne koszty:</b> {pln(inne_koszty)}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='small-note'>Założenie kalkulatora: VAT do zapłaty = VAT marża − VAT z kosztów, a PIT i zdrowotne liczone są od dochodu po odjęciu kosztu netto i innych kosztów.</div>", unsafe_allow_html=True)
