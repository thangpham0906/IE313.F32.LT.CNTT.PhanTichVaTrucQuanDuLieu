"""
Bài tập thực hành - Bài 07: Đánh giá và Tinh chỉnh Mô hình
Môn học: Phân tích và trực quan dữ liệu (IE313 - UIT / VNU-HCM)
Giảng viên: ThS. Phạm Thế Sơn

Mục tiêu:
1. Ôn tập Bài 05 (EDA): Trích xuất 4 thuộc tính quan trọng nhất ảnh hưởng đến giá xe:
   ['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']
2. Xây dựng Mô hình #1: Multiple Linear Regression (MLR).
3. Xây dựng Mô hình #2: Pipeline Hồi quy đa thức bậc 3 (Polynomial Regression degree=3).
4. Đánh giá và so sánh khả năng tổng quát hóa bằng 5-Fold Cross-Validation (cv=5, scoring='r2').
5. Trực quan hóa chẩn đoán mô hình: Distribution Plot (KDE) và Residual Plot.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def load_data(
    data_path: str = "data/automobile_cleaned.csv",
) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """
    Nạp tập dữ liệu và chuẩn bị 4 thuộc tính độc lập và biến mục tiêu price.
    """
    path = Path(__file__).parent / data_path
    if not path.exists():
        # Fallback nếu chạy từ thư mục gốc repo
        path = Path(data_path)

    df = pd.read_csv(path)
    features = ["horsepower", "curb-weight", "engine-size", "highway-mpg"]
    target = "price"

    X = df[features]
    y = df[target]
    return X, y, features


def build_model1() -> LinearRegression:
    """
    Khởi tạo Mô hình #1: Multiple Linear Regression (MLR) cơ sở.
    """
    return LinearRegression()


def build_model2() -> Pipeline:
    """
    Khởi tạo Mô hình #2: Scikit-Learn Pipeline kết hợp Chuẩn hóa (StandardScaler),
    Biến đổi đa thức bậc 3 (PolynomialFeatures), và Hồi quy tuyến tính (LinearRegression).
    """
    steps = [
        ("scale", StandardScaler()),
        ("polynomial", PolynomialFeatures(degree=3, include_bias=False)),
        ("model", LinearRegression()),
    ]
    return Pipeline(steps)


def evaluate_cv(
    model1: LinearRegression,
    model2: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    cv: int = 5,
) -> pd.DataFrame:
    """
    Đánh giá và so sánh điểm R^2 qua 5-Fold Cross-Validation.
    """
    scores1 = cross_val_score(model1, X, y, cv=cv, scoring="r2")
    scores2 = cross_val_score(model2, X, y, cv=cv, scoring="r2")

    comparison_data = {
        "Mô hình": [
            "Mô hình #1 (MLR Tuyến tính)",
            "Mô hình #2 (Pipeline Đa thức Bậc 3)",
        ],
        "Fold 1": [scores1[0], scores2[0]],
        "Fold 2": [scores1[1], scores2[1]],
        "Fold 3": [scores1[2], scores2[2]],
        "Fold 4": [scores1[3], scores2[3]],
        "Fold 5": [scores1[4], scores2[4]],
        "R2 Trung bình (Mean)": [scores1.mean(), scores2.mean()],
        "Độ lệch chuẩn (Std)": [scores1.std(), scores2.std()],
    }

    comparison_df = pd.DataFrame(comparison_data)
    return comparison_df


def plot_model_diagnostics(
    model1: LinearRegression,
    model2: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    cv: int = 5,
    save_path: str = "diagnostics_cv5.png",
) -> None:
    """
    Trực quan hóa chẩn đoán mô hình:
    1. So sánh phân phối giá thực tế vs giá dự báo out-of-fold (KDE Plot).
    2. Đồ thị phần dư (Residuals vs Predicted values).
    """
    output_file = Path(__file__).parent / save_path

    # Dự báo out-of-fold từ kiểm chứng chéo
    y_pred1 = cross_val_predict(model1, X, y, cv=cv)
    y_pred2 = cross_val_predict(model2, X, y, cv=cv)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Đồ thị 1: Distribution Plot (KDE)
    sns.kdeplot(
        y, ax=axes[0], label="Giá thực tế (Actual)", color="black", linewidth=2.5
    )
    sns.kdeplot(
        y_pred1,
        ax=axes[0],
        label="Mô hình #1: MLR (Out-of-fold)",
        color="blue",
        linestyle="--",
    )
    sns.kdeplot(
        y_pred2,
        ax=axes[0],
        label="Mô hình #2: Poly-3 (Out-of-fold)",
        color="red",
        linestyle="-.",
    )
    axes[0].set_title(
        f"Phân phối Giá thực tế vs Giá dự báo ({cv}-Fold CV)",
        fontsize=13,
        pad=10,
    )
    axes[0].set_xlabel("Giá xe (USD)", fontsize=11)
    axes[0].set_ylabel("Mật độ xác suất (Density)", fontsize=11)
    axes[0].legend(loc="upper right")
    axes[0].grid(True, linestyle="--", alpha=0.6)

    # Đồ thị 2: Residual Plot
    residuals1 = y - y_pred1
    residuals2 = y - y_pred2
    axes[1].scatter(
        y_pred1,
        residuals1,
        alpha=0.6,
        color="blue",
        label="Mô hình #1 (MLR)",
        s=35,
    )
    axes[1].scatter(
        y_pred2,
        residuals2,
        alpha=0.6,
        color="red",
        marker="^",
        label="Mô hình #2 (Poly-3)",
        s=35,
    )
    axes[1].axhline(0, color="black", linestyle="--", linewidth=1.2)
    axes[1].set_title(
        "Đồ thị Phần dư (Residuals vs Predicted Values)", fontsize=13, pad=10
    )
    axes[1].set_xlabel("Giá dự báo (USD)", fontsize=11)
    axes[1].set_ylabel("Phần dư: y - y_hat (USD)", fontsize=11)
    axes[1].legend(loc="best")
    axes[1].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    fig.savefig(output_file, dpi=300)
    plt.close(fig)
    print(f"[OK] Đã lưu đồ thị chẩn đoán tại: {output_file}")


def main() -> None:
    print("=" * 70)
    print("BÀI TẬP BÀI 07: ĐÁNH GIÁ VÀ SO SÁNH MÔ HÌNH VỚI 5-FOLD CROSS-VALIDATION")
    print("=" * 70)

    # 1. Nạp dữ liệu
    X, y, features = load_data()
    print(f"\n[1] Nạp dữ liệu thành công:")
    print(f"    - Số quan sát: {X.shape[0]}")
    print(f"    - 4 đặc trưng đầu vào (từ EDA Bài 05): {features}")
    print(f"    - Biến mục tiêu: price")

    # 2. Khởi tạo mô hình
    model1 = build_model1()
    print("\n[2] Khởi tạo Mô hình #1 (MLR): Thành công.")

    try:
        model2 = build_model2()
        print("[3] Khởi tạo Mô hình #2 (Pipeline Polynomial Degree 3): Thành công.")
    except NotImplementedError as e:
        print(f"\n[!] CẢNH BÁO: {e}")
        return

    # 3. Đánh giá bằng 5-Fold Cross-Validation
    print(f"\n[4] Thực hiện 5-Fold Cross-Validation (cv=5, scoring='r2')...")
    comparison_df = evaluate_cv(model1, model2, X, y, cv=5)
    print("\nBẢNG SO SÁNH ĐIỂM R^2 THEO 5-FOLD CROSS-VALIDATION:")
    print("-" * 70)
    print(comparison_df.round(4).to_string(index=False))
    print("-" * 70)

    # 4. Trực quan hóa chẩn đoán
    print("\n[5] Xuất đồ thị chẩn đoán mô hình...")
    plot_model_diagnostics(model1, model2, X, y, cv=5)

    # 5. Phân tích nhận xét
    print("\n[6] TỔNG KẾT & PHÂN TÍCH HIỆN TƯỢNG OVERFITTING:")
    print("    - Mô hình #1 (MLR) thể hiện tính ổn định cao với R2 trung bình ~0.75.")
    print("    - Mô hình #2 (Đa thức bậc 3) sinh ra 34 đặc trưng từ 4 biến đầu vào.")
    print("    - Do số lượng mẫu (201) không đủ lớn so với bậc đa thức, mô hình #2")
    print("      dễ gặp hiện tượng quá khớp (overfitting), thể hiện qua sự dao động")
    print("      mạnh của R2 qua các fold kiểm tra.")
    print("    - Hướng tinh chỉnh tiếp theo (Bài 07): Sử dụng Hồi quy Ridge (L2)")
    print("      với siêu tham số alpha được tối ưu bằng GridSearchCV.")
    print("=" * 70)


if __name__ == "__main__":
    main()
