"""
Translate the Central Bank of Russia exchange rates PDF from Russian to English,
preserving the original layout, colors, font sizes, and graphical elements.

Uses PyMuPDF to redact Russian text in-place and overlay English translations
at the exact same positions.
"""

import fitz

INPUT_PDF = "/workspace/original.pdf"
OUTPUT_PDF = "/workspace/exchange_rates_translated.pdf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TRANSLATIONS: dict[str, str] = {
    # Header
    "107016, Москва, ул. Неглинная, д. 12, к. В, Банк России":
        "107016, Moscow, Neglinnaya St., 12, Bldg. B, Bank of Russia",
    "8 800 300-30-00": "8 800 300-30-00",
    "www.cbr.ru": "www.cbr.ru",

    # Title (two lines)
    "Официальные курсы валют на заданную":
        "Official Currency Exchange Rates",
    "дату, устанавливаемые ежедневно":
        "for a Given Date, Set Daily",

    # Description (three lines)
    "Центральный банк Российской Федерации установил с 14.03.2026 следующие":
        "The Central Bank of the Russian Federation has established the following",
    "курсы иностранных валют к рублю Российской Федерации без обязательств":
        "foreign currency exchange rates against the Russian Ruble effective from",
    "Банка России покупать или продавать указанные валюты по данному курсу":
        "14.03.2026, without obligation to buy or sell at the given rate.",

    "15.03.2026": "15.03.2026",

    # Table headers
    "Цифр. код": "Num. Code",
    "Букв. код": "Alpha Code",
    "Единиц": "Units",
    "Валюта": "Currency",
    "Курс": "Rate",

    # Page 1 currencies
    "Австралийский доллар": "Australian Dollar",
    "Азербайджанский манат": "Azerbaijani Manat",
    "Алжирских динаров": "Algerian Dinars",
    "Армянских драмов": "Armenian Drams",
    "Батов": "Thai Bahts",
    "Бахрейнский динар": "Bahraini Dinar",
    "Белорусский рубль": "Belarusian Ruble",
    "Боливиано": "Boliviano",
    "Бразильский реал": "Brazilian Real",
    "Вон": "South Korean Won",
    "Гонконгский доллар": "Hong Kong Dollar",
    "Гривен": "Ukrainian Hryvnias",
    "Датская крона": "Danish Krone",
    "Дирхам ОАЭ": "UAE Dirham",
    "Доллар США": "US Dollar",
    "Донгов": "Vietnamese Dongs",
    "Евро": "Euro",
    "Египетских фунтов": "Egyptian Pounds",
    "Злотый": "Polish Zloty",
    "Иен": "Japanese Yen",
    "Индийских рупий": "Indian Rupees",
    "Иранских риалов": "Iranian Rials",
    "Канадский доллар": "Canadian Dollar",
    "Катарский риал": "Qatari Riyal",
    "Кубинских песо": "Cuban Pesos",
    "Кьятов": "Myanmar Kyats",
    "Лари": "Georgian Lari",
    "Молдавских леев": "Moldovan Lei",
    "Найр": "Nigerian Nairas",
    "Новозеландский доллар": "New Zealand Dollar",
    "Новый туркменский манат": "Turkmen New Manat",
    "Норвежских крон": "Norwegian Kroner",
    "Оманский риал": "Omani Rial",
    "Румынский лей": "Romanian Leu",
    "Рупий": "Indonesian Rupiahs",
    "Рэндов": "South African Rands",
    "Саудовский риял": "Saudi Riyal",

    # Page 2 currencies
    "СДР (специальные права заимствования)": "SDR (Special Drawing Rights)",
    "Сербских динаров": "Serbian Dinars",
    "Сингапурский доллар": "Singapore Dollar",
    "Сомов": "Kyrgyzstani Soms",
    "Сомони": "Tajikistani Somonis",
    "Так": "Bangladeshi Takas",
    "Тенге": "Kazakhstani Tenges",
    "Тугриков": "Mongolian Tugriks",
    "Турецких лир": "Turkish Liras",
    "Узбекских сумов": "Uzbekistani Sums",
    "Форинтов": "Hungarian Forints",
    "Фунт стерлингов": "British Pound Sterling",
    "Чешских крон": "Czech Korunas",
    "Шведских крон": "Swedish Kronor",
    "Швейцарский франк": "Swiss Franc",
    "Эфиопских быров": "Ethiopian Birrs",
    "Юань": "Chinese Yuan",

    # Footer
    "Последнее обновление страницы: 13.03.2026":
        "Last page update: 13.03.2026",
}

TITLE_FONT = "fa46vz2-2gs-exs-qwfdd9lc"
DATA_FONT = "f73y1si-160h-cqg-16ef6vm"

CURRENCY_COL_RIGHT = 478.0


def hex_to_tuple(color_int: int) -> tuple[float, float, float]:
    r = ((color_int >> 16) & 0xFF) / 255.0
    g = ((color_int >> 8) & 0xFF) / 255.0
    b = (color_int & 0xFF) / 255.0
    return (r, g, b)


def get_row_bg_color(page, y_center: float) -> tuple[float, float, float] | None:
    """Sample the background color of a table row from the page's drawings."""
    for d in page.get_drawings():
        drect = d["rect"]
        fill = d.get("fill")
        if fill and drect.y0 <= y_center <= drect.y1:
            if drect.x0 < 240 and drect.x1 > 400:
                if fill != (1.0, 1.0, 1.0):
                    return fill
    return None


def translate_pdf() -> None:
    doc = fitz.open(INPUT_PDF)
    font_regular_obj = fitz.Font(fontfile=FONT_REGULAR)
    font_bold_obj = fitz.Font(fontfile=FONT_BOLD)

    for page_idx in range(len(doc)):
        page = doc[page_idx]

        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
        replacements: list[tuple[dict, str]] = []

        for block in blocks["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text and text in TRANSLATIONS:
                        replacements.append((span, TRANSLATIONS[text]))

        for span, en_text in replacements:
            bbox = span["bbox"]
            is_data = span["font"] == DATA_FONT
            measure_font = font_regular_obj if is_data else font_bold_obj
            font_size = span["size"]

            en_width = measure_font.text_length(en_text, fontsize=font_size)
            ru_width = bbox[2] - bbox[0]
            redact_right = bbox[0] + max(en_width, ru_width) + 2

            is_currency_cell = (
                abs(bbox[0] - 234.1) < 1.0
                and is_data
                and font_size < 10
            )
            if is_currency_cell:
                redact_right = min(redact_right, CURRENCY_COL_RIGHT)

            y_center = (bbox[1] + bbox[3]) / 2.0
            bg = get_row_bg_color(page, y_center)
            fill_color = bg if bg else (1, 1, 1)

            redact_rect = fitz.Rect(bbox[0], bbox[1], redact_right, bbox[3])
            page.add_redact_annot(redact_rect, text="", fill=fill_color)

        page.apply_redactions()

        for span, en_text in replacements:
            bbox = span["bbox"]
            font_size = span["size"]
            color = hex_to_tuple(span["color"])

            is_data = span["font"] == DATA_FONT
            font_file = FONT_REGULAR if is_data else FONT_BOLD
            font_name = "DjVu" if is_data else "DjVuB"
            measure_font = font_regular_obj if is_data else font_bold_obj

            is_title = span["font"] == TITLE_FONT
            if is_title:
                max_width = 530.0 - bbox[0]
                text_width = measure_font.text_length(en_text, fontsize=font_size)
                if text_width > max_width:
                    font_size = font_size * (max_width / text_width)

            insert_point = fitz.Point(bbox[0], bbox[3] - 1.0)

            page.insert_text(
                insert_point,
                en_text,
                fontsize=font_size,
                fontname=font_name,
                fontfile=font_file,
                color=color,
            )

    doc.save(OUTPUT_PDF, garbage=4, deflate=True)
    doc.close()
    print(f"Translated PDF saved to: {OUTPUT_PDF}")


if __name__ == "__main__":
    translate_pdf()
