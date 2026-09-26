// Part A - Related Work and Data (Word .docx builder)
// Output: literature_review/Part_A_Related_Work_and_Data.docx
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, HeadingLevel,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(ROOT, "literature_review");
fs.mkdirSync(OUT_DIR, { recursive: true });
const OUT = path.join(OUT_DIR, "Part_A_Related_Work_and_Data.docx");

const NAVY = "0B3D5C";
const KEYBG = "EAF1F6";
const BORDER = "B7C9D6";

// content width for A4 with 1" margins = 11906 - 2880 = 9026 DXA
const KEY_W = 2450;
const VAL_W = 6576;
const TABLE_W = KEY_W + VAL_W;

// mini rich-text: parse <i>..</i> and <c>..</c> (monospace) into TextRuns
function runs(text, base = {}) {
  const out = [];
  const re = /<(i|c)>([\s\S]*?)<\/\1>/g;
  let last = 0, m;
  const push = (t, extra) => { if (t) out.push(new TextRun({ text: t, ...base, ...extra })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index), {});
    if (m[1] === "i") push(m[2], { italics: true });
    else push(m[2], { font: "Consolas", size: (base.size || 18) - 1 });
    last = re.lastIndex;
  }
  push(text.slice(last), {});
  return out.length ? out : [new TextRun({ text: "", ...base })];
}

const cellBorders = () => {
  const b = { style: BorderStyle.SINGLE, size: 4, color: BORDER };
  return { top: b, bottom: b, left: b, right: b };
};

function kvTable(rows) {
  const trs = rows.map(([k, v]) =>
    new TableRow({
      children: [
        new TableCell({
          width: { size: KEY_W, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, fill: KEYBG, color: "auto" },
          borders: cellBorders(),
          margins: { top: 60, bottom: 60, left: 90, right: 90 },
          children: [new Paragraph({
            children: [new TextRun({ text: k, bold: true, color: NAVY, size: 18 })],
          })],
        }),
        new TableCell({
          width: { size: VAL_W, type: WidthType.DXA },
          borders: cellBorders(),
          margins: { top: 60, bottom: 60, left: 90, right: 90 },
          children: [new Paragraph({ children: runs(v, { size: 18 }) })],
        }),
      ],
    })
  );
  return new Table({
    columnWidths: [KEY_W, VAL_W],
    width: { size: TABLE_W, type: WidthType.DXA },
    rows: trs,
  });
}

const H = (text) => new Paragraph({
  spacing: { before: 220, after: 90 },
  children: [new TextRun({ text, bold: true, color: NAVY, size: 24 })],
});

// ---------------------------------------------------------------- content
const PAPER1 = [
  ["Title", "A data-driven approach to predict the success of bank telemarketing"],
  ["Harvard reference", "Moro, S., Cortez, P. & Rita, P. (2014) 'A data-driven approach to predict the success of bank telemarketing', <i>Decision Support Systems</i>, 62, pp.22-31. doi:10.1016/j.dss.2014.03.001."],
  ["Link", "https://doi.org/10.1016/j.dss.2014.03.001"],
  ["Modelling", "Four classifiers compared under a rolling-window evaluation: Logistic Regression, Decision Tree, Support Vector Machine and Neural Network. The Neural Network gave the best discrimination (AUC ~0.80, cumulative-lift based selection). Feature relevance assessed with a sensitivity-analysis procedure."],
  ["Preprocessing", "Semi-automatic feature selection reducing 150+ candidate attributes to 22; removal of the call-duration attribute for realistic (pre-call) modelling; categorical encoding; addition of socio-economic context variables (employment variation, consumer confidence, Euribor)."],
  ["Datasets used", "The UCI Bank Marketing dataset (Portuguese retail bank, direct telemarketing campaigns, 2008-2010). This is the same public dataset adopted in the present project."],
  ["Key takeaways", "Establishes the reference formulation for predicting deposit subscription from demographic, campaign and macro-economic features. Confirms that call-duration is leakage and must be dropped for deployable models, and that macro-economic context materially improves performance - both decisions are replicated in this project."],
];

const PAPER2 = [
  ["Title", "Predicting customer churn using machine learning: a case study in the software industry"],
  ["Harvard reference", "Dias, J.R. & Antonio, N. (2025) 'Predicting customer churn using machine learning: a case study in the software industry', <i>Journal of Marketing Analytics</i>, 13(1), pp.111-127. doi:10.1057/s41270-023-00269-9."],
  ["Link", "https://doi.org/10.1057/s41270-023-00269-9"],
  ["Modelling", "Six supervised classifiers benchmarked: Random Forest, AdaBoost, Gradient Boosting, Multilayer Perceptron, XGBoost and Logistic Regression. XGBoost was the strongest model (Recall ~0.85, ROC-AUC ~0.86)."],
  ["Preprocessing", "Handling of class imbalance through resampling; feature scaling; categorical encoding; hyper-parameter tuning by cross-validated search; evaluation on a held-out set using Recall, F1 and ROC-AUC with business cost in mind."],
  ["Datasets used", "A proprietary customer-behaviour dataset from a software (SaaS) provider - not public - but the customer-retention / activation framing is directly analogous to the SS1 account-activation problem."],
  ["Key takeaways", "Provides recent, peer-reviewed evidence that gradient-boosted trees (XGBoost) outperform logistic regression and other ensembles on imbalanced customer-behaviour targets, and that Recall / ROC-AUC are the appropriate business metrics - supporting the choice of XGBoost as Model 2 here."],
];

const PAPER3 = [
  ["Title", "Application of SMOTE to handle imbalance class in deposit classification using the Extreme Gradient Boosting algorithm"],
  ["Harvard reference", "Arifah, D., Saragih, T.H., Kartini, D., Muliadi, M. & Mazdadi, M.I. (2023) 'Application of SMOTE to handle imbalance class in deposit classification using the Extreme Gradient Boosting algorithm', <i>Jurnal Ilmiah Teknik Elektro Komputer dan Informatika (JITEKI)</i>, 9(2), pp.396-410. doi:10.26555/jiteki.v9i2.26155."],
  ["Link", "https://doi.org/10.26555/jiteki.v9i2.26155"],
  ["Modelling", "Extreme Gradient Boosting (XGBoost) as the classifier, combined with SMOTE over-sampling to correct class imbalance. Reported accuracy ~0.910 and ROC ~0.938 after SMOTE."],
  ["Preprocessing", "SMOTE synthetic over-sampling of the minority (subscribed) class; categorical encoding; train/test partitioning; comparison of performance with and without SMOTE to isolate the effect of balancing."],
  ["Datasets used", "The UCI Bank Marketing dataset (~11.7% positive rate) - the same public dataset used in this project, making its results directly comparable."],
  ["Key takeaways", "Demonstrates, on the identical public dataset, that XGBoost with explicit imbalance handling is a strong performer for deposit classification. Motivates the imbalance strategy (scale_pos_weight / class_weight) used here and the recommendation to trial SMOTE as a future improvement in Part D."],
];

const DATASET = [
  ["Name", "UCI Bank Marketing - <c>bank-additional-full.csv</c> (the full, socio-economically enriched version)"],
  ["Harvard reference", "Moro, S., Cortez, P. & Rita, P. (2014) 'A data-driven approach to predict the success of bank telemarketing', <i>Decision Support Systems</i>, 62, pp.22-31. Dataset hosted at the UCI Machine Learning Repository. doi:10.24432/C5K306."],
  ["Link", "https://archive.ics.uci.edu/dataset/222/bank+marketing"],
  ["Number of instances", "41,188 rows (one row per client contact)"],
  ["Number of feature columns", "20 input attributes (after removing the leakage attribute <c>duration</c>, 19 predictors are used; the project then engineers 5 additional features, giving 77 columns after one-hot encoding)"],
  ["Number of classes", "2 (binary classification)"],
  ["Target and its range", "<c>y</c> - has the client subscribed a term deposit? Values: 'yes' / 'no', mapped to 1 / 0. Positive (subscribed) rate = 11.27%, i.e. an imbalanced target."],
  ["Origin", "Direct (telephone) marketing campaigns of a Portuguese retail bank, May 2008 - November 2010, enriched by the authors with five Banco de Portugal socio-economic indicators (employment variation rate, consumer price index, consumer confidence index, Euribor 3-month rate, number of employees)."],
];

const doc = new Document({
  creator: "STADIO Equities Capstone (CAP182)",
  title: "Part A - Related Work and Data",
  sections: [{
    properties: { page: { margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
    children: [
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { after: 60 },
        children: [new TextRun({ text: "Part A – Related Work and Data", bold: true, color: NAVY, size: 32 })],
      }),
      new Paragraph({
        spacing: { after: 160 },
        children: runs("Machine-Learning Capstone (CAP182) · SS2 · STADIO Equities account-activation project. Three peer-reviewed publications relevant to predicting deposit subscription / customer activation from behavioural and demographic data, followed by a description of the public dataset used to prove the approach.", { size: 19 }),
      }),
      H("Table 1 – Literature review: Moro, Cortez & Rita (2014)"), kvTable(PAPER1),
      H("Table 2 – Literature review: Dias & Antonio (2025)"), kvTable(PAPER2),
      H("Table 3 – Literature review: Arifah et al. (2023)"), kvTable(PAPER3),
      H("Table 4 – Description of the public dataset used in this project"), kvTable(DATASET),
      new Paragraph({
        spacing: { before: 160 },
        children: runs("Note: two of the three reviewed publications (Moro et al., 2014 and Arifah et al., 2023) use this exact public dataset, satisfying the requirement that at least one reviewed paper relies on a dataset also available to this project and enabling direct comparison of results in Part C and Part D.", { size: 16, color: "666666" }),
      }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("Wrote " + path.relative(ROOT, OUT));
});
