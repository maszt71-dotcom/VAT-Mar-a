import streamlit as st

st.set_page_config(page_title="Kalkulator VAT marża PRO+", page_icon="💰", layout="centered")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 920px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    .app-shell {
        background: linear-gradient(180deg, #f7f8fc 0%, #eef2ff 100%);
        border: 1px solid #e7eaf6;
        border-radius: 26px;
        padding: 18px;
        box-shadow: 0 12px 30px rgba(36, 41, 61, 0.08);
    }
    .hero {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        color: white;
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 10px 24px rgba(17, 24, 39, 0.20);
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
    .section-title {
        font-size: 15px;
        font-weight: 700;
        color: #344054;
        margin: 8px 0 10px 2px;
    }
    .card {
        background: white;
        border: 1px solid #e8ecf5;
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        height: 100%;
    }
    .label {
        font-size: 13px;
        color: #667085;
        margin-bottom: 8px;
    }
    .value {
        font-size: 28px;
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
    .pill-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 8px;
        margin-bottom: 14px;
    }
    .pill {
        background: white;
        border: 1px solid #e8ecf5;
        border-radius: 999px;
        padding: 8px 12px;
        font-size: 13px;
        color: #475467;
        box-shadow: 0 2px 6px rgba(15,23,42,0.04);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def pln(x: float) -> str:
    return f"{x:,.2f} zł".replace(",", " ")


def policz(zakup: float, faktura_marza: float, cena_na_reke: float, koszt_brutto: float):
    marza = faktura_marza - zakup
    vat_marza = marza * 23 / 123 if marza > 0 else 0.0

    vat_z_kosztow = koszt_brutto * 23 / 123 if koszt_brutto > 0 else 0.0
    koszt_netto = koszt_brutto - vat_z_kosztow

    vat_do_zaplaty = vat_marza - vat_z_kosztow
    dochod = marza - vat_marza - koszt_netto
    pit_liniowy = dochod * 0.19 if dochod > 0 else 0.0
    zdrowotne = dochod * 0.049 if dochod > 0 else 0.0

    zarobek = cena_na_reke - zakup - koszt_brutto - max(vat_do_zaplaty, 0) - pit_liniowy - zdrowotne
    podatki_razem = max(vat_do_zaplaty, 0) + pit_liniowy + zdrowotne

    return {
        "marza": marza,
        "vat_marza": vat_marza,
        "vat_z_kosztow": vat_z_kosztow,
        "koszt_netto": koszt_netto,
        "vat_do_zaplaty": vat_do_zaplaty,
        "dochod": dochod,
        "pit_liniowy": pit_liniowy,
        "zdrowotne": zdrowotne,
        "zarobek": zarobek,
        "podatki_razem": podatki_razem,
    }


def znajdz_cene_na_reke_dla_zarobku(zakup: float, faktura_marza: float, koszt_brutto: float, oczekiwany_zarobek: float):
    start = policz(zakup, faktura_marza, 0.0, koszt_brutto)
    baza_bez_ceny = start["zarobek"]
    potrzebna_cena = oczekiwany_zarobek - baza_bez_ceny
    return max(potrzebna_cena, 0.0)


st.title("💰 Kalkulator VAT marża PRO+")
st.caption("VAT do zapłaty = VAT marża − VAT z kosztów. Osobno VAT, PIT liniowy i zdrowotne.")

with st.form("kalkulator"):
    st.subheader("Dane wejściowe")
    c1, c2 = st.columns(2)
    with c1:
        zakup = st.number_input("Zakup (umowa)", min_value=0.0, value=547.0, step=100.0)
        faktura_marza = st.number_input("Faktura VAT marża", min_value=0.0, value=2000.0, step=100.0)
        koszt_brutto = st.number_input("Koszty (faktura brutto 23%)", min_value=0.0, value=600.0, step=100.0)
    with c2:
        cena_na_reke = st.number_input("Cena sprzedaży / ile klient realnie płaci", min_value=0.0, value=3000.0, step=100.0)
        oczekiwany_zarobek = st.number_input("Jaki zarobek chcesz osiągnąć", min_value=0.0, value=500.0, step=100.0)

    licz = st.form_submit_button("Oblicz")

if licz or True:
    wynik = policz(zakup, faktura_marza, cena_na_reke, koszt_brutto)
    potrzebna_cena_na_reke = znajdz_cene_na_reke_dla_zarobku(zakup, faktura_marza, koszt_brutto, oczekiwany_zarobek)
    roznica_do_celu = wynik["zarobek"] - oczekiwany_zarobek

    kolor_zarobek = "value-green" if wynik["zarobek"] >= 0 else "value-red"
    kolor_cel = "value-green" if roznica_do_celu >= 0 else "value-red"
    kolor_vat = "value-orange" if wynik["vat_do_zaplaty"] > 0 else "value-green"

    st.markdown("<div class='app-shell'>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-small">Zarobek teraz</div>
            <p class="hero-big {kolor_zarobek}">{pln(wynik['zarobek'])}</p>
            <div class="pill-row">
                <div class="pill">Cel zarobku: {pln(oczekiwany_zarobek)}</div>
                <div class="pill">Różnica do celu: {pln(roznica_do_celu)}</div>
                <div class="pill">Cena realnie zapłacona: {pln(cena_na_reke)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Podatki do zapłaty</div>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)

    with t1:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">VAT do zapłaty</div>
                <div class="value {kolor_vat}">{pln(wynik['vat_do_zaplaty'])}</div>
                <div class="subvalue">VAT marża − VAT z kosztów</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t2:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">PIT liniowy 19%</div>
                <div class="value value-blue">{pln(wynik['pit_liniowy'])}</div>
                <div class="subvalue">Od dochodu: {pln(wynik['dochod'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t3:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Zdrowotne 4,9%</div>
                <div class="value value-red">{pln(wynik['zdrowotne'])}</div>
                <div class="subvalue">Od dochodu: {pln(wynik['dochod'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t4:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Podatki razem</div>
                <div class="value">{pln(wynik['podatki_razem'])}</div>
                <div class="subvalue">VAT + PIT + zdrowotne</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-title'>Liczenie w drugą stronę</div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)

    with b1:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Oczekiwany zarobek</div>
                <div class="value">{pln(oczekiwany_zarobek)}</div>
                <div class="subvalue">To chcesz osiągnąć</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b2:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Brakuje / nadwyżka</div>
                <div class="value {kolor_cel}">{pln(roznica_do_celu)}</div>
                <div class="subvalue">Porównanie do celu</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b3:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Potrzebna cena na rękę</div>
                <div class="value value-blue">{pln(potrzebna_cena_na_reke)}</div>
                <div class="subvalue">Żeby osiągnąć wpisany zarobek</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Pokaż szczegóły obliczeń"):
        st.write(f"**Zakup (umowa):** {pln(zakup)}")
        st.write(f"**Faktura VAT marża:** {pln(faktura_marza)}")
        st.write(f"**Cena realnie zapłacona:** {pln(cena_na_reke)}")
        st.write(f"**Koszty brutto:** {pln(koszt_brutto)}")
        st.write(f"**Marża do VAT:** {pln(wynik['marza'])}")
        st.write(f"**VAT marża:** {pln(wynik['vat_marza'])}")
        st.write(f"**VAT z kosztów:** {pln(wynik['vat_z_kosztow'])}")
        st.write(f"**VAT do zapłaty:** {pln(wynik['vat_do_zaplaty'])}")
        st.write(f"**Koszt netto:** {pln(wynik['koszt_netto'])}")
        st.write(f"**Dochód do PIT i zdrowotnego:** {pln(wynik['dochod'])}")
        st.write(f"**PIT liniowy:** {pln(wynik['pit_liniowy'])}")
        st.write(f"**Zdrowotne:** {pln(wynik['zdrowotne'])}")
        st.write(f"**Zarobek teraz:** {pln(wynik['zarobek'])}")
        st.write(f"**Potrzebna cena na rękę dla celu:** {pln(potrzebna_cena_na_reke)}")

    if wynik["zarobek"] < 0:
        st.error("Na tej transakcji wychodzisz na minus.")
    elif roznica_do_celu < 0:
        st.warning("Do oczekiwanego zarobku jeszcze brakuje.")
    else:
        st.success("Cel zarobku osiągnięty.")

    st.markdown("</div>", unsafe_allow_html=True)
