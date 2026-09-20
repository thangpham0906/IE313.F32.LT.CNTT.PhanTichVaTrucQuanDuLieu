# GitHub Copilot Instructions for IE313 (UIT - VNU-HCM)
- Course: IE313 - Data Analysis and Visualization (ThS. Phạm Thế Sơn).
- Strict Matplotlib OO API: Do not suggest `plt.plot()`, `plt.title()`, or `plt.xlabel()`. Always suggest `fig, ax = plt.subplots()` followed by `ax.set_*()`.
- Vietnamese Font Support: Use `plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']` and `plt.rcParams['axes.unicode_minus'] = False`.
- Zero Data Leakage: Combine `StandardScaler()`, `PolynomialFeatures()`, and estimator inside `sklearn.pipeline.Pipeline`.
- Reproducibility: Always pin `random_state=42` in `train_test_split`, `KFold`, and estimators.
- Statistical Rigor: Report dual test statistics ($r$ or $F$) with exact $p$-values ($\alpha = 0.05$).
- Raw Data Immutability: Never modify files under `datasets/raw/`.
- Bilingual Rule: Code identifiers in English; docstrings, markdown, and chart labels in Vietnamese.
