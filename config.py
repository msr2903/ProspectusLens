# Find the page that contains these keywords
keywords_dict = {
    "underwriter": [
        ["keterangan tentang penjaminan emisi efek"],
        ["susunan dan jumlah porsi penjaminan"]
    ],
    "balance_sheet": [
        ["laporan posisi keuangan", "cash and cash equivalent", "catatan/"],
        ["laporan posisi keuangan", "cash", "total assets", "catatan/"],
        ["laporan posisi keuangan", "piutang", "jumlah aset", "catatan"],
        ["laporan posisi keuangan", "piutang", "total aset", "catatan"],
        ["consolidated statement", "piutang", "total aset", "catatan/"],
        ["piutang", "total aset", "notes"],
        ["piutang", "jumlah aset", "notes"]
    ],
    "cash_flow": [
        ["laporan arus kas", "arus kas dari", "aktivitas operasi", "catatan/"],
        ["laporan arus kas", "arus kas dari", "catatan/"],
        ["laporan arus kas", "arus kas dari", "catatan"],
        ["arus kas dari", "aktivitas operasi", "catatan"]
    ],
    "income_statement": [
        ["laporan laba rugi", "penjualan", "pokok penjualan", "catatan/"],
        ["laporan laba rugi", "revenues", "beban pokok", "catatan/"],
        ["laporan laba rugi", "revenue", "beban pokok", "catatan/"],
        ["laporan laba rugi", "penjualan", "beban pokok", "catatan"],
        ["laporan laba rugi", "pendapatan", "beban pokok", "catatan"],
        ["laporan laba rugi", "income", "catatan/"],
        ["laporan laba rugi", "pendapatan", "catatan/"],
        ["laporan laba rugi", "pendapatan usaha", "catatan"],
        ["laporan laba rugi", "pendapatan", "catatan"],
        ["penjualan", "beban pokok", "catatan"]
    ]
}

# Stop extraction until this keywords matched
stop_keywords = {
    "balance_sheet": [["laba per saham"], ["jumlah ekuitas"], ["total ekuitas"]],
    "cash_flow": [["kas dan setara kas"], ["kas dan bank"], ["kas dan setara"]],
    "income_statement": [["per saham"], ["total comprehensive"], ["laba komprehensif"], ["laba bersih per"]]
}

# Exclude pages when this keywords matched
anti_keywords = {
    "balance_sheet": [],
    "cash_flow": [],
    "income_statement": [["laporan perubahan ekuitas"], ["laporan arus kas"]]
}
