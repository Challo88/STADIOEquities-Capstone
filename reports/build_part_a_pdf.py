"""
Part A - Related Work and Data (PDF builder).

Generates literature_review/Part_A_Related_Work_and_Data.pdf containing:
  - Table 1..3 : one literature-review table per publication
                 (Title, Harvard reference, Link, Modelling, Preprocessing,
                  Datasets used, Key takeaways)
  - Table 4    : dataset-description table for the public dataset used in this
                 project (UCI Bank Marketing - bank-additional-full.csv)

Run:
    python reports/build_part_a_pdf.py

Output:
    literature_review/Part_A_Related_Work_and_Data.pdf
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether,
)

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "literature_review"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "Part_A_Related_Work_and_Data.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1c", parent=styles["Heading1"], fontSize=16, spaceAfter=6,
                    textColor=colors.HexColor("#0B3D5C"))
H2 = ParagraphStyle("H2c", parent=styles["Heading2"], fontSize=12, spaceBefore=10,
                    spaceAfter=4, textColor=colors.HexColor("#0B3D5C"))
BODY = ParagraphStyle("Bodyc", parent=styles["BodyText"], fontSize=9.5, leading=13)
CELL = ParagraphStyle("Cell", parent=styles["BodyText"], fontSize=8.8, leading=11.5)
CELL_KEY = ParagraphStyle("CellKey", parent=CELL, fontName="Helvetica-Bold",
                          textColor=colors.HexColor("#0B3D5C"))
SMALL = ParagraphStyle("Small", parent=styles["BodyText"], fontSize=8, leading=10,
                       textColor=colors.grey)


def kv_table(rows):
    """Build a 2-column attribute/value table from a list of (key, value)."""
    data = [[Paragraph(k, CELL_KEY), Paragraph(v, CELL)] for k, v in rows]
    tbl = Table(data, colWidths=[3.6 * cm, 12.9 * cm])
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B7C9D6")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF1F6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tbl


# ---------------------------------------------------------------- literature
PAPER1 = [
    ("Title", "A data-driven approach to predict the success of bank telemarketing"),
    ("Harvard reference",
     "Moro, S., Cortez, P. &amp; Rita, P. (2014) 'A data-driven approach to predict "
     "the success of bank telemarketing', <i>Decision Support Systems</i>, 62, "
     "pp.22-31. doi:10.1016/j.dss.2014.03.001."),
    ("Link", "https://doi.org/10.1016/j.dss.2014.03.001"),
    ("Modelling",
     "Four classifiers compared under a rolling-window evaluation: Logistic "
     "Regression, Decision Tree, Support Vector Machine and Neural Network. The "
     "Neural Network gave the best discrimination (AUC ~0.80, cumulative-lift "
     "based selection). Feature relevance assessed with a sensitivity-analysis "
     "procedure."),
    ("Preprocessing",
     "Semi-automatic feature selection reducing 150+ candidate attributes to 22; "
     "removal of the call-duration attribute for realistic (pre-call) modelling; "
     "categorical encoding; addition of socio-economic context variables "
     "(employment variation, consumer confidence, Euribor)."),
    ("Datasets used",
     "The UCI Bank Marketing dataset (Portuguese retail bank, direct telemarketing "
     "campaigns, 2008-2010). This is the same public dataset adopted in the present "
     "project."),
    ("Key takeaways",
     "Establishes the reference formulation for predicting deposit subscription from "
     "demographic, campaign and macro-economic features. Confirms that "
     "call-duration is leakage and must be dropped for deployable models, and that "
     "macro-economic context materially improves performance - both decisions are "
     "replicated in this project."),
]

PAPER2 = [
    ("Title", "Predicting customer churn using machine learning: a case study in the "
              "software industry"),
    ("Harvard reference",
     "Dias, J.R. &amp; Antonio, N. (2025) 'Predicting customer churn using machine "
     "learning: a case study in the software industry', <i>Journal of Marketing "
     "Analytics</i>, 13(1), pp.111-127. doi:10.1057/s41270-023-00269-9."),
    ("Link", "https://doi.org/10.1057/s41270-023-00269-9"),
    ("Modelling",
     "Six supervised classifiers benchmarked: Random Forest, AdaBoost, Gradient "
     "Boosting, Multilayer Perceptron, XGBoost and Logistic Regression. XGBoost was "
     "the strongest model (Recall ~0.85, ROC-AUC ~0.86)."),
    ("Preprocessing",
     "Handling of class imbalance through resampling; feature scaling; categorical "
     "encoding; hyper-parameter tuning by cross-validated search; evaluation on a "
     "held-out set using Recall, F1 and ROC-AUC with business cost in mind."),
    ("Datasets used",
     "A proprietary customer-behaviour dataset from a software (SaaS) provider - not "
     "public - but the customer-retention / activation framing is directly analogous "
     "to the SS1 account-activation problem."),
    ("Key takeaways",
     "Provides recent, peer-reviewed evidence that gradient-boosted trees (XGBoost) "
     "outperform logistic regression and other ensembles on imbalanced "
     "customer-behaviour targets, and that Recall / ROC-AUC are the appropriate "
     "business metrics - supporting the choice of XGBoost as Model 2 here."),
]

PAPER3 = [
    ("Title", "Application of SMOTE to handle imbalance class in deposit "
              "classification using the Extreme Gradient Boosting algorithm"),
    ("Harvard reference",
     "Arifah, D., Saragih, T.H., Kartini, D., Muliadi, M. &amp; Mazdadi, M.I. (2023) "
     "'Application of SMOTE to handle imbalance class in deposit classification using "
     "the Extreme Gradient Boosting algorithm', <i>Jurnal Ilmiah Teknik Elektro "
     "Komputer dan Informatika (JITEKI)</i>, 9(2), pp.396-410. "
     "doi:10.26555/jiteki.v9i2.26155."),
    ("Link", "https://doi.org/10.26555/jiteki.v9i2.26155"),
    ("Modelling",
     "Extreme Gradient Boosting (XGBoost) as the classifier, combined with SMOTE "
     "over-sampling to correct class imbalance. Reported accuracy ~0.910 and "
     "ROC ~0.938 after SMOTE."),
    ("Preprocessing",
     "SMOTE synthetic over-sampling of the minority (subscribed) class; "
     "categorical encoding; train/test partitioning; comparison of performance "
     "with and without SMOTE to isolate the effect of balancing."),
    ("Datasets used",
     "The UCI Bank Marketing dataset (~11.7% positive rate) - the same public "
     "dataset used in this project, making its results directly comparable."),
    ("Key takeaways",
     "Demonstrates, on the identical public dataset, that XGBoost with explicit "
     "imbalance handling is a strong performer for deposit classification. Motivates "
     "the imbalance strategy (scale_pos_weight / class_weight) used here and the "
     "recommendation to trial SMOTE as a future improvement in Part D."),
]

# ---------------------------------------------------------------- dataset table
DATASET = [
    ("Name", "UCI Bank Marketing - <font face='Courier'>bank-additional-full.csv</font> "
             "(the full, socio-economically enriched version)"),
    ("Harvard reference",
     "Moro, S., Cortez, P. &amp; Rita, P. (2014) 'A data-driven approach to predict "
     "the success of bank telemarketing', <i>Decision Support Systems</i>, 62, "
     "pp.22-31. Dataset hosted at the UCI Machine Learning Repository. "
     "doi:10.24432/C5K306."),
    ("Link", "https://archive.ics.uci.edu/dataset/222/bank+marketing"),
    ("Number of instances", "41,188 rows (one row per client contact)"),
    ("Number of feature columns",
     "20 input attributes (after removing the leakage attribute "
     "<font face='Courier'>duration</font>, 19 predictors are used; the project then "
     "engineers 5 additional features, giving 77 columns after one-hot encoding)"),
    ("Number of classes", "2 (binary classification)"),
    ("Target and its range",
     "<font face='Courier'>y</font> - has the client subscribed a term deposit? "
     "Values: 'yes' / 'no', mapped to 1 / 0. Positive (subscribed) rate = 11.27%, "
     "i.e. an imbalanced target."),
    ("Origin",
     "Direct (telephone) marketing campaigns of a Portuguese retail bank, "
     "May 2008 - November 2010, enriched by the authors with five Banco de Portugal "
     "socio-economic indicators (employment variation rate, consumer price index, "
     "consumer confidence index, Euribor 3-month rate, number of employees)."),
]


def build():
    doc = SimpleDocTemplate(
        str(OUT_PATH), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="Part A - Related Work and Data",
        author="STADIO Equities Capstone (CAP182)",
    )
    story = []
    story.append(Paragraph("Part A &ndash; Related Work and Data", H1))
    story.append(Paragraph(
        "Machine-Learning Capstone (CAP182) &middot; SS2 &middot; STADIO Equities "
        "account-activation project. Three peer-reviewed publications relevant to "
        "predicting deposit subscription / customer activation from behavioural and "
        "demographic data, followed by a description of the public dataset used to "
        "prove the approach.", BODY))
    story.append(Spacer(1, 6))

    for idx, (title, rows) in enumerate([
        ("Table 1 &ndash; Literature review: Moro, Cortez &amp; Rita (2014)", PAPER1),
        ("Table 2 &ndash; Literature review: Dias &amp; Antonio (2025)", PAPER2),
        ("Table 3 &ndash; Literature review: Arifah et al. (2023)", PAPER3),
    ], start=1):
        story.append(KeepTogether([Paragraph(title, H2), Spacer(1, 3), kv_table(rows)]))
        story.append(Spacer(1, 8))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Table 4 &ndash; Description of the public dataset used in this project", H2))
    story.append(Spacer(1, 3))
    story.append(kv_table(DATASET))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Note: two of the three reviewed publications (Moro et al., 2014 and "
        "Arifah et al., 2023) use this exact public dataset, satisfying the "
        "requirement that at least one reviewed paper relies on a dataset also "
        "available to this project and enabling direct comparison of results in "
        "Part C and Part D.", SMALL))

    doc.build(story)
    print(f"Wrote {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
