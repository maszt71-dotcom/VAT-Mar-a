import streamlit as st

st.set_page_config(page_title="Kalkulator VAT marża PRO+", page_icon="💰", layout="centered")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
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
    .divider-space { height: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def pln(x: float) -> str:
    return f"{x:,.2f} zł".replace(",", " ")


st.title("💰 Kalkulator VAT marża PRO+")
st.caption("Wygląd bardziej jak aplikacja: czytelne kafelki, osobno VAT, PIT liniowy i zdrowotne.")

with st.form("kalkulator"):
    st.subheader("Dane wejściowe")
    col1, col2 = st.columns(2)
    with col1:
        zakup = st.number_input("Zakup (umowa)", min_value=0.0, value=547.0, step=100.0)
        faktura_marza = st.number_input("Faktura VAT marża", min_value=0.0, value=2000.0, step=100.0)
        koszt_brutto = st.number_input("Koszty (faktura brutto 23%)", min_value=0.0, value=600.0, step=100.0)
    with col2:
        cena_na_reke = st.number_input("Cena sprzedaży / ile klient realnie płaci", min_value=0.0, value=3000.0, step=100.0)
        target_zostaje = st.number_input("Ile ma zostać na rękę", min_value=0.0, value=500.0, step=100.0)

    licz = st.form_submit_button("Oblicz")

if licz or True:
    marza = faktura_marza - zakup
    vat_marza = marza * 23 / 123 if marza > 0 else 0.0

    vat_koszt = koszt_brutto * 23 / 123 if koszt_brutto > 0 else 0.0
    koszt_netto = koszt_brutto - vat_koszt

    vat_do_zaplaty = vat_marza - vat_koszt
    dochod = marza - vat_marza - koszt_netto
    pit_liniowy = dochod * 0.19 if dochod > 0 else 0.0
    zdrowotne = dochod * 0.049 if dochod > 0 else 0.0

    realnie_zostaje = cena_na_reke - zakup - koszt_brutto - max(vat_do_zaplaty, 0) - pit_liniowy - zdrowotne
    roznica_do_celu = realnie_zostaje - target_zostaje

    kolor_zostaje = "value-green" if realnie_zostaje >= 0 else "value-red"
    kolor_cel = "value-green" if roznica_do_celu >= 0 else "value-red"
    kolor_vat = "value-orange" if vat_do_zaplaty > 0 else "value-green"

    st.markdown("<div class='app-shell'>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-small">Teraz realnie zostaje</div>
            <p class="hero-big {kolor_zostaje}">{pln(realnie_zostaje)}</p>
            <div class="pill-row">
                <div class="pill">Cel: {pln(target_zostaje)}</div>
                <div class="pill">Różnica do celu: {pln(roznica_do_celu)}</div>
                <div class="pill">Cena realnie zapłacona: {pln(cena_na_reke)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Podatki do zapłaty</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">VAT do zapłaty</div>
                <div class="value {kolor_vat}">{pln(vat_do_zaplaty)}</div>
                <div class="subvalue">VAT marża: {pln(vat_marza)}<br>VAT z kosztów: {pln(vat_koszt)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">PIT liniowy 19%</div>
                <div class="value value-blue">{pln(pit_liniowy)}</div>
                <div class="subvalue">Liczony od dochodu: {pln(dochod)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Zdrowotne 4,9%</div>
                <div class="value value-red">{pln(zdrowotne)}</div>
                <div class="subvalue">Liczona od dochodu: {pln(dochod)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='divider-space'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Podsumowanie transakcji</div>", unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Ile ma zostać</div>
                <div class="value">{pln(target_zostaje)}</div>
                <div class="subvalue">Twój zakładany cel</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c5:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Różnica do celu</div>
                <div class="value {kolor_cel}">{pln(roznica_do_celu)}</div>
                <div class="subvalue">Na plusie lub brakuje do celu</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c6:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Podatki razem</div>
                <div class="value">{pln(max(vat_do_zaplaty, 0) + pit_liniowy + zdrowotne)}</div>
                <div class="subvalue">VAT + PIT liniowy + zdrowotne</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Pokaż szczegóły obliczeń"):
        st.write(f"**Zakup (umowa):** {pln(zakup)}")
        st.write(f"**Faktura VAT marża:** {pln(faktura_marza)}")
        st.write(f"**Cena realnie zapłacona:** {pln(cena_na_reke)}")
        st.write(f"**Koszty brutto:** {pln(koszt_brutto)}")
        st.write(f"**Marża do VAT:** {pln(marza)}")
        st.write(f"**VAT marża:** {pln(vat_marza)}")
        st.write(f"**VAT z kosztów:** {pln(vat_koszt)}")
        st.write(f"**Koszt netto:** {pln(koszt_netto)}")
        st.write(f"**Dochód do PIT i zdrowotnego:** {pln(dochod)}")
        st.write(f"**PIT liniowy:** {pln(pit_liniowy)}")
        st.write(f"**Zdrowotne:** {pln(zdrowotne)}")
        st.write(f"**Realnie zostaje:** {pln(realnie_zostaje)}")

    if realnie_zostaje < 0:
        st.error("Na tej transakcji wychodzisz na minus.")
    elif roznica_do_celu < 0:
        st.warning("Do zakładanego celu jeszcze brakuje.")
    else:
        st.success("Cel osiągnięty.")

    st.markdown("</div>", unsafe_allow_html=True)
