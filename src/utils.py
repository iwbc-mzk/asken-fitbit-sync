from const import UNITS


def micrograms_to_iu(mcg: float) -> float:
    return mcg * 40


def salt_g_to_sodium_mg(salt: float) -> float:
    return salt * 1000 / 2.54


def remove_unit(nutrition_value: str) -> float:
    """Remove unit from nutrition value and convert to float."""
    # 単位削除処理で上から順に一致を確認するので接頭辞付きを上に記載する

    for unit in UNITS:
        if nutrition_value.endswith(unit):
            return float(nutrition_value[: -UNITS[unit]["word_cnt"]].strip())

    return float(nutrition_value)
