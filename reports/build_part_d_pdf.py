"""
Part D - Business Recommendations Report (PDF builder).

Generates reports/Part_D_Recommendations.pdf: a formal ~900-word business
recommendations report with Harvard referencing, answering the four required
questions:
  1. Which model performed best?
  2. How could that model be improved?
  3. How must the approach be adapted for the SS1 requested (client) data?
  4. Do the results align with the Part A literature?

Run:
    python reports/build_part_d_pdf.py

Output:
    reports/Part_D_Recommendations.pdf
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "Part_D_Recommendations.pdf"

styles = getSampleStyleSheet()
TITLE = ParagraphStyle("TitleC", parent=styles["Heading1"], fontSize=16,
                       spaceAfter=2, textColor=colors.HexColor("#0B3D5C"))
SUB = ParagraphStyle("SubC", parent=styles["BodyText"], fontSize=9,
                     textColor=colors.grey, spaceAfter=10)
H2 = ParagraphStyle("H2c", parent=styles["Heading2"], fontSize=11.5,
                    spaceBefore=10, spaceAfter=3,
                    textColor=colors.HexColor("#0B3D5C"))
BODY = ParagraphStyle("BodyC", parent=styles["BodyText"], fontSize=10, leading=14,
                      spaceAfter=6, alignment=4)  # justified
REF = ParagraphStyle("RefC", parent=styles["BodyText"], fontSize=8.6, leading=11.5,
                     leftIndent=14, firstLineIndent=-14, spaceAfter=3)

# Body paragraphs. Word count of the substantive body (Introduction..Conclusion)
# is ~900 words.
PARAS = [
    ("Executive summary", [
        "This report recommends how STADIO Equities should proceed with the "
        "account-activation model proposed in SS1, based on evidence gathered by "
        "proving the approach on a public analogue of the client problem - the UCI "
        "Bank Marketing dataset (Moro, Cortez and Rita, 2014). Two models were "
        "built and compared: a Logistic Regression baseline (Model 1) and an "
        "XGBoost gradient-boosted ensemble (Model 2). XGBoost is recommended as the "
        "primary model, with Logistic Regression retained as an interpretable "
        "challenger. The remainder of the report justifies this choice, sets out how "
        "the model can be improved, explains how it must be adapted once the client "
        "releases the SS1 requested data, and confirms that the findings align with "
        "the published literature.",
    ]),
    ("1. Which model performed best?", [
        "On the held-out test set of 6,179 accounts, XGBoost outperformed Logistic "
        "Regression on every headline metric: ROC-AUC of 0.812 versus 0.800, "
        "PR-AUC of 0.485 versus 0.461, F1 of 0.524 versus 0.505, and top-decile "
        "lift of 4.58 versus 4.49. Both models comfortably exceed the SS1 success "
        "criteria (ROC-AUC of at least 0.75 and top-decile lift of at least 2.0), "
        "meaning either would deliver business value, but XGBoost is the stronger "
        "performer.",
        "The advantage is statistically credible rather than incidental. A McNemar "
        "test on the paired test-set predictions gives a chi-square of 6.89 "
        "(p = 0.009), and a bootstrap confidence interval for the difference in "
        "ROC-AUC (XGBoost minus Logistic Regression) is +0.012 with a 95% interval "
        "of [+0.004, +0.020] that excludes zero. A note of caution is warranted: "
        "under five-fold cross-validation the gap narrows (0.792 versus 0.788) and "
        "a paired t-test is not significant (p = 0.202). The honest conclusion is "
        "that XGBoost is the best model and its edge is real but modest; Logistic "
        "Regression remains a defensible choice where transparency is paramount.",
    ]),
    ("2. How could the recommended model be improved?", [
        "Several concrete improvements are available. First, systematic "
        "hyper-parameter tuning (for example a cross-validated grid or Bayesian "
        "search over tree depth, learning rate, subsampling and regularisation) "
        "should widen the current margin, as the model was trained with sensible but "
        "untuned defaults and early stopping. Second, the class imbalance "
        "(11.3% positive) can be addressed more aggressively: Arifah et al. (2023) "
        "report substantial gains on this same dataset by combining XGBoost with "
        "SMOTE over-sampling, which should be trialled against the current "
        "scale_pos_weight approach. Third, probability calibration (Platt or "
        "isotonic) would make the predicted scores more reliable for ranking and "
        "budgeting. Fourth, the decision threshold should be set from the client's "
        "true cost of a wasted contact versus the value of an activated account "
        "rather than from F1 alone. Finally, richer behavioural features - the "
        "in-app and engagement signals requested in SS1 - are likely to raise "
        "performance well beyond what the public proxy can show. Together these "
        "steps form a clear, low-risk optimisation path that can be pursued "
        "incrementally, measuring the incremental lift of each change on a fixed "
        "validation window before it is accepted.",
    ]),
    ("3. How must the approach be adapted for the SS1 data?", [
        "The public dataset is an analogue, not the client's data, so several "
        "adaptations are required before deployment. The client's event-level "
        "records (registration, deposits, sessions and marketing touches, as set out "
        "in the SS1 data request) must be aggregated to one row per account, and the "
        "target redefined as the SS1 activation event - a first qualifying deposit "
        "within the 30-day activation window. Care must be taken to exclude any "
        "feature that is only observable after the outcome; this mirrors the removal "
        "of the call-duration attribute in the public data, which is leakage. "
        "Time-aware validation is essential: exploratory analysis of the public data "
        "revealed strong non-stationarity (the positive rate drifted from roughly "
        "6% to 38% across the 2008-2010 campaign period), so the client model should "
        "be validated on a forward time window and monitored for drift after launch. "
        "The engineered features that proved valuable here - prior-contact history "
        "and success flags - have direct analogues in the client's behavioural and "
        "nudge data and should be reconstructed.",
    ]),
    ("4. Do the results align with the Part A literature?", [
        "Yes. The finding that XGBoost is the best model is consistent with Dias and "
        "Antonio (2025), who found gradient boosting superior to logistic regression "
        "and other ensembles on an imbalanced customer-behaviour target, and with "
        "Arifah et al. (2023), who applied XGBoost to this exact dataset. The "
        "importance of macro-economic context in our model (the number of employees "
        "and employment-variation rate were the two strongest predictors) echoes "
        "Moro, Cortez and Rita (2014), whose central contribution was to show that "
        "socio-economic context improves telemarketing prediction. Our absolute "
        "ROC-AUC (about 0.81) is lower than some published figures (for example the "
        "0.94 reported by Arifah et al.), which is expected and appropriate: those "
        "higher results typically rely on SMOTE and, in some cases, retain the "
        "leakage-prone call-duration attribute, whereas this project deliberately "
        "excluded duration and applied only in-training imbalance weighting to keep "
        "the estimate realistic and deployable. In short, the direction of the "
        "evidence agrees with the literature while the absolute numbers reflect the "
        "deliberately conservative, leakage-safe design adopted here.",
    ]),
    ("Conclusion", [
        "STADIO Equities should adopt XGBoost as the primary account-activation "
        "model, retain Logistic Regression as a transparent challenger, and invest "
        "in tuning, imbalance handling and calibration before launch. Once the SS1 "
        "data is released, the pipeline should be re-fitted on account-level client "
        "data with a leakage-safe 30-day activation target and time-aware "
        "validation. The public-data evidence, corroborated by the literature, gives "
        "high confidence that the SS1 approach is sound and ready to be proven on "
        "the client's own data.",
    ]),
]

REFERENCES = [
    "Arifah, D., Saragih, T.H., Kartini, D., Muliadi, M. and Mazdadi, M.I. (2023) "
    "'Application of SMOTE to handle imbalance class in deposit classification using "
    "the Extreme Gradient Boosting algorithm', <i>Jurnal Ilmiah Teknik Elektro "
    "Komputer dan Informatika (JITEKI)</i>, 9(2), pp.396-410. "
    "doi:10.26555/jiteki.v9i2.26155.",
    "Dias, J.R. and Antonio, N. (2025) 'Predicting customer churn using machine "
    "learning: a case study in the software industry', <i>Journal of Marketing "
    "Analytics</i>, 13(1), pp.111-127. doi:10.1057/s41270-023-00269-9.",
    "Moro, S., Cortez, P. and Rita, P. (2014) 'A data-driven approach to predict the "
    "success of bank telemarketing', <i>Decision Support Systems</i>, 62, pp.22-31. "
    "doi:10.1016/j.dss.2014.03.001.",
]


def build():
    doc = SimpleDocTemplate(
        str(OUT_PATH), pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="Part D - Business Recommendations",
        author="STADIO Equities Capstone (CAP182)",
    )
    story = [
        Paragraph("Part D &ndash; Business Recommendations", TITLE),
        Paragraph("Machine-Learning Capstone (CAP182) &middot; SS2 &middot; "
                  "STADIO Equities account-activation project", SUB),
    ]
    for heading, paras in PARAS:
        story.append(Paragraph(heading, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    story.append(Spacer(1, 6))
    story.append(Paragraph("References", H2))
    for r in REFERENCES:
        story.append(Paragraph(r, REF))

    doc.build(story)

    # crude word count of the body for the log
    words = sum(len(p.split()) for _, paras in PARAS for p in paras)
    print(f"Wrote {OUT_PATH.relative_to(ROOT)}  (~{words} words in body)")


if __name__ == "__main__":
    build()
