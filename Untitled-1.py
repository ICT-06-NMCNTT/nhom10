# %%
# 1. Thiết lập hạn mức miễn trừ
# ======================
@dataclass
class MienTru:
    ban_than: float = 11_000_000      # miễn trừ bản thân / tháng
    phu_thuoc: float = 4_400_000      # miễn trừ 1 người phụ thuộc / tháng

# ======================

# 2. Thông tin người lao động
# ======================
@dataclass
class NguoiLaoDong:
    ten: str
    nam: int
    so_nguoi_phu_thuoc: int

# ======================
# Biểu thuế lũy tiến từng phần
# (ngưỡng thu nhập tính thuế theo tháng)
# ======================
BAC_THUE = [
    (5_000_000, 0.05),
    (10_000_000, 0.10),
    (18_000_000, 0.15),
    (32_000_000, 0.20),
    (52_000_000, 0.25),
    (80_000_000, 0.30),
    (float('inf'), 0.35)
]

# ======================
# Hàm tính thuế TNCN tháng
# ======================
def tinh_thue_thang(thu_nhap: float, mien_tru: MienTru, so_phu_thuoc: int) -> float:
    giam_tru = mien_tru.ban_than + so_phu_thuoc * mien_tru.phu_thuoc
    thu_nhap_tinh_thue = max(0, thu_nhap - giam_tru)

    thue = 0.0
    thu_nhap_con_lai = thu_nhap_tinh_thue
    muc_duoi = 0

    for muc_tren, ty_le in BAC_THUE:
        if thu_nhap_con_lai <= 0:
            break
        muc_chiu_thue = min(muc_tren - muc_duoi, thu_nhap_con_lai)
        thue += muc_chiu_thue * ty_le
        thu_nhap_con_lai -= muc_chiu_thue
        muc_duoi = muc_tren

    return thue

# ======================
# 3 & 4. Quản lý thu nhập và quyết toán năm
# ======================
@dataclass
class QuanLyThue:
    nguoi_lao_dong: NguoiLaoDong
    mien_tru: MienTru
    thu_nhap_thang: Dict[int, float] = field(default_factory=dict)

    def nhap_thu_nhap_thang(self, thang: int, thu_nhap: float):
        self.thu_nhap_thang[thang] = thu_nhap

    def quyet_toan_nam(self):
        print("=" * 80)
        print(f"QUYẾT TOÁN THUẾ TNCN NĂM {self.nguoi_lao_dong.nam}")
        print(f"Người lao động : {self.nguoi_lao_dong.ten}")
        print(f"Số người phụ thuộc : {self.nguoi_lao_dong.so_nguoi_phu_thuoc}")
        print("=" * 80)
        print(f"{'Tháng':<10}{'Thu nhập':<20}{'Thuế TNCN':<20}")

        tong_thue_tam_nop = 0
        tong_thu_nhap = 0

        for thang in range(1, 13):
            thu_nhap = self.thu_nhap_thang.get(thang, 0)
            thue = tinh_thue_thang(
                thu_nhap,
                self.mien_tru,
                self.nguoi_lao_dong.so_nguoi_phu_thuoc
            )
            tong_thue_tam_nop += thue
            tong_thu_nhap += thu_nhap
            print(f"{thang:<10}{thu_nhap:<20,.0f}{thue:<20,.0f}")

        # Thuế thực tế tính lại theo năm (chia đều thu nhập)
        thu_nhap_bq_thang = tong_thu_nhap / 12
        thue_bq_thang = tinh_thue_thang(
            thu_nhap_bq_thang,
            self.mien_tru,
            self.nguoi_lao_dong.so_nguoi_phu_thuoc
        )
        thue_thuc_te = thue_bq_thang * 12
        hoan_thue = max(0, tong_thue_tam_nop - thue_thuc_te)

        print("=" * 80)
        print(f"Tổng thuế TNCN đã tạm nộp : {tong_thue_tam_nop:,.0f} VND")
        print(f"Thuế TNCN thực tế phải nộp : {thue_thuc_te:,.0f} VND")
        print(f"Tiền thuế được hoàn lại : {hoan_thue:,.0f} VND")
        print("=" * 80)

# ======================
# Ví dụ sử dụng chương trình
# ======================
if __name__ == '__main__':
    mien_tru = MienTru()
    nld = NguoiLaoDong("Nguyễn Văn A", 2024, 1)
    ql = QuanLyThue(nld, mien_tru)

    # Nhập thu nhập một số tháng
    ql.nhap_thu_nhap_thang(1, 20_000_000)
    ql.nhap_thu_nhap_thang(2, 20_000_000)
    ql.nhap_thu_nhap_thang(3, 25_000_000)
    ql.nhap_thu_nhap_thang(6, 30_000_000)

    # Quyết toán năm
    ql.quyet_toan_nam()

# %%
class TaxCalculator:
    def __init__(self):
        # 1. Hạn mức miễn trừ
        self.personal_deduction = 11_000_000
        self.dependent_deduction = 4_400_000

        # 2. Thông tin người lao động
        self.name = ""
        self.year = 0
        self.dependents = 0

        # Thu nhập 12 tháng
        self.incomes = {m: 0 for m in range(1, 13)}

    # ---------------------------
    # Chức năng 1
    def set_deductions(self):
        print("\n--- THIET LAP GIAM TRU ---")
        self.personal_deduction = int(input("Giảm trừ bản thân (VNĐ/tháng): "))
        self.dependent_deduction = int(input("Giảm trừ 1 người phụ thuộc (VNĐ/tháng): "))

    # ---------------------------
    # Chức năng 2
    def set_taxpayer_info(self):
        print("\n--- THONG TIN NGUOI LAO DONG ---")
        self.name = input("Tên người lao động: ")
        self.year = int(input("Năm tính thuế: "))
        self.dependents = int(input("Số người phụ thuộc: "))

    # ---------------------------
    # Chức năng 3
    def input_monthly_income(self):
        print("\n--- NHAP THU NHAP TUNG THANG ---")
        for month in range(1, 13):
            income = input(f"Thu nhập tháng {month} (Enter nếu không có): ")
            if income.strip() != "":
                self.incomes[month] = int(income)

    # ---------------------------
    def taxable_income(self, income):
        deduction = self.personal_deduction + self.dependents * self.dependent_deduction
        return max(0, income - deduction)

    # ---------------------------
    def calculate_tax(self, taxable):
        brackets = [
            (5_000_000, 0.05),
            (10_000_000, 0.10),
            (18_000_000, 0.15),
            (32_000_000, 0.20),
            (52_000_000, 0.25),
            (80_000_000, 0.30),
            (float("inf"), 0.35)
        ]

        tax = 0
        prev_limit = 0

        for limit, rate in brackets:
            if taxable > prev_limit:
                tax += (min(taxable, limit) - prev_limit) * rate
                prev_limit = limit

        return tax

    # ---------------------------
    # Chức năng 4
    def annual_settlement(self):
        print("\n==============================================")
        print(f"NGUOI NOP THUE: {self.name}")
        print(f"NAM TINH THUE: {self.year}")
        print(f"SO NGUOI PHU THUOC: {self.dependents}")
        print("==============================================")

        print(f"{'Thang':<6}{'Thu nhap':>15}{'Thue TNCN':>15}")

        total_tax_paid = 0
        total_income = 0

        for month in range(1, 13):
            income = self.incomes[month]
            taxable = self.taxable_income(income)
            tax = self.calculate_tax(taxable)

            total_income += income
            total_tax_paid += tax

            print(f"{month:<6}{income:>15,.0f}{tax:>15,.0f}")

        print("----------------------------------------------")

        annual_taxable = self.taxable_income(total_income / 12) * 12
        actual_annual_tax = self.calculate_tax(annual_taxable / 12) * 12
        refund = total_tax_paid - actual_annual_tax

        print(f"Tong thue TNCN da tam nop: {total_tax_paid:,.0f}")
        print(f"Thue TNCN thuc te:        {actual_annual_tax:,.0f}")

        if refund > 0:
            print(f"So tien duoc hoan:        {refund:,.0f}")
        else:
            print(f"So tien can nop them:    {-refund:,.0f}")


# ===============================
# CHUONG TRINH CHINH
# ===============================
if __name__ == "__main__":
    app = TaxCalculator()
    app.set_deductions()
    app.set_taxpayer_info()
    app.input_monthly_income()
    app.annual_settlement()

# %%



