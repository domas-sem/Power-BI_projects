"""
Insurance Claims Fraud Detection Project - EDA and Data Cleaning
Author: Domas Semenauskas
Purpose: Demonstrate Python fundamentals (variables, data types, conditional
         logic, functions) together with data cleaning and exploratory data
         analysis (EDA), using a publicly available insurance claims dataset.
Dataset: insurance_claims.csv
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. KONFIGURACIJA / KINTAMIEJI
# -----------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FAILO_KELIAS = os.path.join(SCRIPT_DIR, "insurance_claims.csv")
ISSKIRTIES_STULPELIS = "umbrella_limit"
TIKSLO_STULPELIS = "fraud_reported"

# -----------------------------
# 2. DUOMENU IKELIMAS
# -----------------------------
def ikelti_duomenis(kelias: str) -> pd.DataFrame:
    """Ikelti CSV faila i pandas DataFrame."""
    df = pd.read_csv(kelias)
    print(f"Duomenys ikelti: {df.shape[0]} eilutes, {df.shape[1]} stulpeliai")
    return df


def apzvelgti_duomenis(df: pd.DataFrame) -> None:
    """Atspausdinti pagrindine informacija apie duomenu struktura."""
    print("\n--- Duomenu tipai ---")
    print(df.dtypes)
    print("\n--- Truksamos reiksmes ---")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    print("\n--- Statistine apzvalga ---")
    print(df.describe().T)


# -----------------------------
# 3. DUOMENU VALYMAS
# -----------------------------
def sutvarkyti_truksamas_reiksmes(df: pd.DataFrame) -> pd.DataFrame:
    """Pakeisti '?' zymeklius i NaN reiksmes stulpeliuose, kur jie naudojami."""
    df = df.replace("?", np.nan)
    return df


def sutvarkyti_isskirtis(df: pd.DataFrame, stulpelis: str) -> pd.DataFrame:
    """
    Sutvarkyti neigiamas/nerealias reiksmes skaitiniame stulpelyje naudojant
    salygine logika (if/else). Neigiamos umbrella_limit reiksmes pakeiciamos
    i 0, nes neigiama riba nera reali.
    """
    if stulpelis in df.columns:
        df[stulpelis] = df[stulpelis].apply(lambda x: 0 if x < 0 else x)
    return df


def pasalinti_duplikatus(df: pd.DataFrame) -> pd.DataFrame:
    """Pasalinti pilnai sutampancias eilutes, jei tokiu yra."""
    pries = df.shape[0]
    df = df.drop_duplicates()
    po = df.shape[0]
    print(f"Pasalinta {pries - po} dublikatu eiluciu")
    return df


def pasalinti_nenaudojamus_stulpelius(df: pd.DataFrame, stulpeliai: list) -> pd.DataFrame:
    """Pasalinti stulpelius, kurie neturi analitines vertes (ID, tusti stulpeliai)."""
    esami = [c for c in stulpeliai if c in df.columns]
    return df.drop(columns=esami)


def konvertuoti_datas(df: pd.DataFrame, stulpeliai: list) -> pd.DataFrame:
    """Konvertuoti teksto formato datas i datetime tipa."""
    for stulpelis in stulpeliai:
        if stulpelis in df.columns:
            df[stulpelis] = pd.to_datetime(df[stulpelis], errors="coerce")
    return df


# -----------------------------
# 4. KINTAMUJU KURIMAS / SALYGINE LOGIKA
# -----------------------------
def koduoti_tiksla(df: pd.DataFrame, tikslo_stulpelis: str) -> pd.DataFrame:
    """Konvertuoti Y/N tikslo stulpeli i binarini 1/0 naudojant salygine logika."""
    df[tikslo_stulpelis] = df[tikslo_stulpelis].apply(lambda x: 1 if x == "Y" else 0)
    return df


def kategorizuoti_kliento_stazei(menesiai: float) -> str:
    """
    Funkcijos pavyzdys, demonstruojantis salygine logika (if/elif/else).
    Suskirsto klientus i grupes pagal tai, kiek laiko jie turi polisa.
    """
    if menesiai < 12:
        return "Naujas"
    elif 12 <= menesiai < 60:
        return "Isitvirtines"
    else:
        return "Ilgametis"


def prideti_stazes_kategorija(df: pd.DataFrame) -> pd.DataFrame:
    """Pritaikyti kategorizuoti_kliento_stazei() ir sukurti nauja stulpeli."""
    if "months_as_customer" in df.columns:
        df["kliento_stazes_grupe"] = df["months_as_customer"].apply(kategorizuoti_kliento_stazei)
    return df


def pazymeti_didele_rizika(eilute) -> int:
    """
    Keliu salygu logikos pavyzdys, kombinuojantis kelis stulpelius, siekiant
    pazymeti potencialiai dideles rizikos zalas.
    """
    didele_suma = eilute.get("total_claim_amount", 0) > 40000
    trumpa_staze = eilute.get("months_as_customer", 999) < 12
    if didele_suma and trumpa_staze:
        return 1
    return 0


def prideti_rizikos_zyma(df: pd.DataFrame) -> pd.DataFrame:
    """Pritaikyti pazymeti_didele_rizika() eilutems ir sukurti rizikos zymos stulpeli."""
    df["dideles_rizikos_zyma"] = df.apply(pazymeti_didele_rizika, axis=1)
    return df


def apskaiciuoti_zalos_santyki(df: pd.DataFrame) -> pd.DataFrame:
    """Apskaiciuoti, kokia dalis bendros zalos sudaro transporto priemones zala."""
    if "vehicle_claim" in df.columns and "total_claim_amount" in df.columns:
        df["vehicle_claim_dalis"] = np.where(
            df["total_claim_amount"] > 0,
            df["vehicle_claim"] / df["total_claim_amount"],
            0
        )
    return df


# -----------------------------
# 5. PAGRINDINIS VALYMO IR ANALIZES PROCESAS
# -----------------------------
def main():
    df = ikelti_duomenis(FAILO_KELIAS)
    apzvelgti_duomenis(df)

    df = sutvarkyti_truksamas_reiksmes(df)
    df = sutvarkyti_isskirtis(df, ISSKIRTIES_STULPELIS)
    df = pasalinti_duplikatus(df)
    df = pasalinti_nenaudojamus_stulpelius(df, ["_c39"])
    df = konvertuoti_datas(df, ["policy_bind_date", "incident_date"])

    df = koduoti_tiksla(df, TIKSLO_STULPELIS)
    df = prideti_stazes_kategorija(df)
    df = prideti_rizikos_zyma(df)
    df = apskaiciuoti_zalos_santyki(df)

    print("\n--- Sukciavimo lygis pagal ivykio tipa (%) ---")
    print(df.groupby("incident_type")[TIKSLO_STULPELIS].mean().sort_values(ascending=False) * 100)

    print("\n--- Sukciavimo lygis pagal poliso valstija (%) ---")
    print(df.groupby("policy_state")[TIKSLO_STULPELIS].mean().sort_values(ascending=False) * 100)

    print("\n--- Vidutine zalos suma pagal rizikos zyma ---")
    print(df.groupby("dideles_rizikos_zyma")["total_claim_amount"].mean())

    df.to_csv("insurance_claims_sutvarkytas.csv", index=False)
    print("\nSutvarkytas duomenu rinkinys issaugotas kaip insurance_claims_sutvarkytas.csv")

    return df


if __name__ == "__main__":
    main()
    
