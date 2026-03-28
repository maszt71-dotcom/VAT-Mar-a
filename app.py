import streamlit as st

st.set_page_config(page_title="Kalkulator VAT marża PRO+", page_icon="💰", layout="centered")

st.title("💰 Kalkulator VAT marża PRO+")
st.caption("Uwzględnia: faktura VAT marża + realna cena na rękę")

# INPUTY
zakup = st.number_input("Zakup (umowa)", min_value=0.0, value=547.0)
faktura_marza = st.number_input("Faktura VAT marża (dla podatków)", min_value=0.0, value=2000.0)
cena_na_reke = st.number_input("Cena sprzedaży (ile klient realnie płaci)", min_value=0.0, value=3000.0)
koszt_brutto = st.number_input("Koszty (faktura brutto 23%)", min_value=0.0, value=600.0)

target_zostaje = st.number_input("Ile ma zostać na rękę", min_value=0.0, value=500.0)

if st.button("Oblicz"):

    # MARŻA liczona z faktury (bo tak jest podatkowo)
    marza = faktura_marza - zakup

    vat_marza = marza * 23 / 123 if marza > 0 else 0

    # VAT z kosztów
    vat_koszt = koszt_brutto * 23 / 123
    koszt_netto = koszt_brutto - vat_koszt

    vat_do_zaplaty = vat_marza - vat_koszt

    # DOCHÓD podatkowy
    dochod = marza - vat_marza - koszt_netto

    pit = dochod * 0.19 if dochod > 0 else 0
    zdrowotne = dochod * 0.049 if dochod > 0 else 0

    # REALNY ZYSK = co dostajesz minus wszystko
    realny_zysk = cena_na_reke - zakup - koszt_brutto - max(vat_do_zaplaty, 0) - pit - zdrowotne

    st.markdown("---")
    st.subheader("📊 Wyniki")

    st.write(f"Marża (do VAT): {marza:.2f} zł")
    st.write(f"VAT do zapłaty: {vat_do_zaplaty:.2f} zł")
    st.write(f"PIT: {pit:.2f} zł")
    st.write(f"Zdrowotne: {zdrowotne:.2f} zł")

    st.markdown("## 💰 REALNIE NA RĘKĘ:")
    st.success(f"{realny_zysk:.2f} zł")

    # maksymalny zakup, żeby zostało target_zostaje
    # wzór uproszczony dla tego samego układu podatków
    max_zakup = cena_na_reke - koszt_brutto - max(vat_do_zaplaty, 0) - pit - zdrowotne - target_zostaje
    
    st.markdown("---")
    st.subheader("🎯 Maksymalny zakup")
    st.write(f"Żeby zostało na rękę: {target_zostaje:.2f} zł")
    st.info(f"Maksymalna cena zakupu: {max_zakup:.2f} zł")

    if realny_zysk < 0:
        st.error("Transakcja na minusie!")
    if max_zakup < 0:
        st.warning("Przy tych ustawieniach nie da się osiągnąć takiego zysku.")
