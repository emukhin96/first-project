"""
Script to translate the Central Bank of Russia exchange rates PDF
from Russian to English and produce a translated PDF output.
"""

from fpdf import FPDF

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

ALL_CURRENCIES = [
    ("036", "AUD", "1", "Australian Dollar", "56.6632"),
    ("944", "AZN", "1", "Azerbaijani Manat", "47.1914"),
    ("012", "DZD", "100", "Algerian Dinars", "60.5958"),
    ("051", "AMD", "100", "Armenian Drams", "21.2495"),
    ("764", "THB", "10", "Thai Bahts", "24.8892"),
    ("048", "BHD", "1", "Bahraini Dinar", "213.3193"),
    ("933", "BYN", "1", "Belarusian Ruble", "27.3508"),
    ("068", "BOB", "1", "Boliviano", "11.6100"),
    ("986", "BRL", "1", "Brazilian Real", "15.4137"),
    ("410", "KRW", "1000", "South Korean Won", "54.2137"),
    ("344", "HKD", "1", "Hong Kong Dollar", "10.2682"),
    ("980", "UAH", "10", "Ukrainian Hryvnias", "18.1655"),
    ("208", "DKK", "1", "Danish Krone", "12.3975"),
    ("784", "AED", "1", "UAE Dirham", "21.8449"),
    ("840", "USD", "1", "US Dollar", "80.2254"),
    ("704", "VND", "10000", "Vietnamese Dongs", "32.0069"),
    ("978", "EUR", "1", "Euro", "91.9847"),
    ("818", "EGP", "10", "Egyptian Pounds", "15.2949"),
    ("985", "PLN", "1", "Polish Zloty", "21.5214"),
    ("392", "JPY", "100", "Japanese Yen", "50.3928"),
    ("356", "INR", "100", "Indian Rupees", "86.7860"),
    ("364", "IRR", "1000000", "Iranian Rials", "58.8139"),
    ("124", "CAD", "1", "Canadian Dollar", "58.9156"),
    ("634", "QAR", "1", "Qatari Riyal", "22.0399"),
    ("192", "CUP", "10", "Cuban Pesos", "33.4273"),
    ("104", "MMK", "1000", "Myanmar Kyats", "38.2026"),
    ("981", "GEL", "1", "Georgian Lari", "29.3640"),
    ("498", "MDL", "10", "Moldovan Lei", "46.2690"),
    ("566", "NGN", "1000", "Nigerian Nairas", "58.4944"),
    ("554", "NZD", "1", "New Zealand Dollar", "46.9800"),
    ("934", "TMT", "1", "Turkmenistani New Manat", "22.9215"),
    ("578", "NOK", "10", "Norwegian Kroner", "83.0259"),
    ("512", "OMR", "1", "Omani Rial", "208.6486"),
    ("946", "RON", "1", "Romanian Leu", "18.0570"),
    ("360", "IDR", "10000", "Indonesian Rupiahs", "47.4735"),
    ("710", "ZAR", "10", "South African Rands", "47.5004"),
    ("682", "SAR", "1", "Saudi Riyal", "21.3934"),
    ("960", "XDR", "1", "SDR (Special Drawing Rights)", "109.3721"),
    ("941", "RSD", "100", "Serbian Dinars", "78.5899"),
    ("702", "SGD", "1", "Singapore Dollar", "62.7300"),
    ("417", "KGS", "100", "Kyrgyzstani Soms", "91.7389"),
    ("972", "TJS", "10", "Tajikistani Somonis", "83.4542"),
    ("050", "BDT", "100", "Bangladeshi Takas", "65.3385"),
    ("398", "KZT", "100", "Kazakhstani Tenges", "16.3166"),
    ("496", "MNT", "1000", "Mongolian Tugriks", "22.4954"),
    ("949", "TRY", "10", "Turkish Liras", "18.2038"),
    ("860", "UZS", "10000", "Uzbekistani Sums", "66.4028"),
    ("348", "HUF", "100", "Hungarian Forints", "23.4187"),
    ("826", "GBP", "1", "British Pound Sterling", "107.0929"),
    ("203", "CZK", "10", "Czech Korunas", "37.9209"),
    ("752", "SEK", "10", "Swedish Kronor", "86.4886"),
    ("756", "CHF", "1", "Swiss Franc", "101.7701"),
    ("230", "ETB", "100", "Ethiopian Birrs", "51.1763"),
    ("156", "CNY", "1", "Chinese Yuan", "11.6504"),
]

COL_WIDTHS = [18, 18, 18, 80, 36]
HEADERS = ["Num. Code", "Alpha Code", "Units", "Currency", "Rate"]
ROW_H = 5.0
FONT_SZ = 7.0
PAGE_BOTTOM = 280  # leave room for footer


class TranslatedPDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "", 7)
        self.set_text_color(100, 100, 100)
        self.cell(0, 4, "107016, Moscow, Neglinnaya St., 12, Bldg. B, Bank of Russia",
                  align="L", new_x="LMARGIN", new_y="NEXT")
        self.cell(60, 4, "8 800 300-30-00", new_x="RIGHT")
        self.cell(0, 4, "www.cbr.ru", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, f"Page {self.page_no()} of {self.alias_nb_pages()}", align="C")


def _draw_table_header(pdf: FPDF) -> None:
    pdf.set_font("DejaVu", "B", FONT_SZ)
    pdf.set_fill_color(60, 80, 130)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(HEADERS):
        align = "R" if i == 4 else ("C" if i < 3 else "L")
        pdf.cell(COL_WIDTHS[i], ROW_H + 0.5, h, border=1, align=align, fill=True)
    pdf.ln()
    pdf.set_text_color(0, 0, 0)


def _draw_table_row(pdf: FPDF, row: tuple[str, ...], fill: bool) -> None:
    pdf.set_font("DejaVu", "", FONT_SZ)
    if fill:
        pdf.set_fill_color(235, 240, 250)
    else:
        pdf.set_fill_color(255, 255, 255)
    for i, val in enumerate(row):
        align = "R" if i == 4 else ("C" if i < 3 else "L")
        pdf.cell(COL_WIDTHS[i], ROW_H, val, border=1, align=align, fill=True)
    pdf.ln()


def build_pdf(output_path: str) -> None:
    pdf = TranslatedPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)

    pdf.add_font("DejaVu", "", FONT_DIR + "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", FONT_DIR + "DejaVuSans-Bold.ttf")

    pdf.add_page()

    # Title
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 6, "Official Exchange Rates for a Given Date, Set Daily",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Description
    pdf.set_font("DejaVu", "", 7.5)
    pdf.multi_cell(
        0, 4,
        "The Central Bank of the Russian Federation has established the following "
        "foreign currency exchange rates against the Russian Ruble effective from "
        "14.03.2026, without any obligation of the Bank of Russia to buy or sell "
        "the specified currencies at the given rate.",
        align="J",
    )
    pdf.ln(1)

    # Date
    pdf.set_font("DejaVu", "B", 9)
    pdf.cell(0, 5, "15.03.2026", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    # Table
    _draw_table_header(pdf)

    fill = False
    for row in ALL_CURRENCIES:
        if pdf.get_y() + ROW_H > PAGE_BOTTOM:
            pdf.add_page()
            _draw_table_header(pdf)
            fill = False
        _draw_table_row(pdf, row, fill)
        fill = not fill

    # "Last page update" note at the bottom of the last page
    pdf.ln(3)
    pdf.set_font("DejaVu", "", 7)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 4, "Last page update: 13.03.2026", align="L")

    pdf.output(output_path)
    print(f"Translated PDF saved to: {output_path}")


if __name__ == "__main__":
    build_pdf("/workspace/exchange_rates_translated.pdf")
