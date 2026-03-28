import streamlit as st

st.set_page_config(page_title="Kalkulator VAT marża PRO+", page_icon="💰", layout="centered")

st.markdown(
    """
    <style>
    .block-container {max-width: 820px; padding-top: 1.2rem; padding-bottom: 2rem;}
    .top-card {
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 14px;
        border: 1px solid #e8e8e8;
        background: #ffffff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    .main-value {
        font-size: 34px;
        font-weight: 800;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .good {color: #0f8a3b;}
    .bad {color: #c62828;}
    .mini-card {
        border-radius: 16px;
        padding: 14px 16px;
        border: 1px solid #ececec;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        min-height: 110px;
    }
    .mini-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 8px;
    }
    .mini-value {
        font-size: 26px;
        font-weight: 800;
        line-height: 1.2;
    }
    .section-gap {margin-top: 10px; margin-bottom: 10px;}
    </style>
    """,
    unsafe_allow_html=True,
)


def pln(x: float) -> str:
    return f"{x:,.2f} zł".replace(",", " ")


st.title("💰 Kalkulator VAT marża PRO+")
st.caption("Faktura VAT marża do podatków + realna cena sprzedaży na rękę")

with st.form("kalkulator"):
    st.subheader("Dane")
    zakup = st.number_input("Zakup (umowa)", min_value=0.0, value=547.0, step=100.0)
    faktura_marza = st.number_input("Faktura VAT marża", min_value=0.0, value=2000.0, step=100.0)
    cena_na_reke = st.number_input("Cena sprzedaży / ile klient realnie płaci", min_value=0.0, value=3000.0, step=100.0)
    koszt_brutto = st.number_input("Koszty (faktura brutto 23%)", min_value=0.0, value=600.0, step=100.0)
    target_zostaje = st.number_input("Ile ma zostać na rękę", min_value=0.0, value=500.0, step=100.0)
    licz = st.form_submit_button("Oblicz")

if licz or True:
    # Podatki liczone od faktury VAT marża
    marza = faktura_marza - zakup
    vat_marza = marza * 23 / 123 if marza > 0 else 0.0

    vat_koszt = koszt_brutto * 23 / 123 if koszt_brutto > 0 else 0.0
    koszt_netto = koszt_brutto - vat_koszt

    vat_do_zaplaty = vat_marza - vat_koszt
    dochod = marza - vat_marza - koszt_netto
    pit = dochod * 0.19 if dochod > 0 else 0.0
    zdrowotne = dochod * 0.049 if dochod > 0 else 0.0

    realnie_zostaje = cena_na_reke - zakup - koszt_brutto - max(vat_do_zaplaty, 0) - pit - zdrowotne
    roznica_do_celu = realnie_zostaje - target_zostaje

    kolor_zostaje = "good" if realnie_zostaje >= 0 else "bad"
    kolor_roznica = "good" if roznica_do_celu >= 0 else "bad"

    st.markdown(
        f"""
        <div class="top-card">
            <div class="mini-title">Teraz realnie zostaje</div>
            <div class="main-value {kolor_zostaje}">{pln(realnie_zostaje)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="mini-title">Ile ma zostać</div>
                <div class="mini-value">{pln(target_zostaje)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="mini-title">Różnica do celu</div>
                <div class="mini-value {kolor_roznica}">{pln(roznica_do_celu)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="mini-title">VAT do zapłaty</div>
                <div class="mini-value">{pln(vat_do_zaplaty)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="mini-title">PIT + zdrowotne</div>
                <div class="mini-value">{pln(pit + zdrowotne)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Pokaż szczegóły"):
        st.write(f"**Zakup:** {pln(zakup)}")
        st.write(f"**Faktura VAT marża:** {pln(faktura_marza)}")
        st.write(f"**Cena realnie zapłacona:** {pln(cena_na_reke)}")
        st.write(f"**Koszt brutto:** {pln(koszt_brutto)}")
        st.write(f"**Marża do VAT:** {pln(marza)}")
        st.write(f"**VAT marża:** {pln(vat_marza)}")
        st.write(f"**VAT z kosztów:** {pln(vat_koszt)}")
        st.write(f"**Koszt netto:** {pln(koszt_netto)}")
        st.write(f"**Dochód do PIT i zdrowotnego:** {pln(dochod)}")
        st.write(f"**PIT:** {pln(pit)}")
        st.write(f"**Zdrowotne:** {pln(zdrowotne)}")

    if realnie_zostaje < 0:
        st.error("Na tej transakcji wychodzisz na minus.")
    elif roznica_do_celu < 0:
        st.warning("Do zakładanego celu jeszcze brakuje.")
    else:
        st.success("Cel osiągnięty.")
