// Part D - Business Recommendations (Word .docx builder)
// Output: reports/Part_D_Recommendations.docx
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "reports", "Part_D_Recommendations.docx");
const NAVY = "0B3D5C";

// rich text with <i>..</i> and <c>..</c> (monospace)
function runs(text, base = {}) {
  const out = [];
  const re = /<(i|c)>([\s\S]*?)<\/\1>/g;
  let last = 0, m;
  const push = (t, extra) => { if (t) out.push(new TextRun({ text: t, ...base, ...extra })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index), {});
    if (m[1] === "i") push(m[2], { italics: true });
    else push(m[2], { font: "Consolas", size: (base.size || 20) - 1 });
    last = re.lastIndex;
  }
  push(text.slice(last), {});
  return out.length ? out : [new TextRun({ text: "", ...base })];
}

const H = (text) => new Paragraph({
  spacing: { before: 220, after: 80 },
  children: [new TextRun({ text, bold: true, color: NAVY, size: 23 })],
});

const P = (text) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 120, line: 276 },
  children: runs(text, { size: 20 }),
});

const SECTIONS = [
  ["Executive summary", [
    "This report recommends how STADIO Equities should proceed with the account-activation model proposed in SS1, based on evidence gathered by proving the approach on a public analogue of the client problem - the UCI Bank Marketing dataset (Moro, Cortez and Rita, 2014). Two models were built and compared: a Logistic Regression baseline (Model 1) and an XGBoost gradient-boosted ensemble (Model 2). XGBoost is recommended as the primary model, with Logistic Regression retained as an interpretable challenger. The remainder of the report justifies this choice, sets out how the model can be improved, explains how it must be adapted once the client releases the SS1 requested data, and confirms that the findings align with the published literature.",
  ]],
  ["1. Which model performed best?", [
    "On the held-out test set of 6,179 accounts, XGBoost outperformed Logistic Regression on every headline metric: ROC-AUC of 0.812 versus 0.800, PR-AUC of 0.485 versus 0.461, F1 of 0.524 versus 0.505, and top-decile lift of 4.58 versus 4.49. Both models comfortably exceed the SS1 success criteria (ROC-AUC of at least 0.75 and top-decile lift of at least 2.0), meaning either would deliver business value, but XGBoost is the stronger performer.",
    "The advantage is statistically credible rather than incidental. A McNemar test on the paired test-set predictions gives a chi-square of 6.89 (p = 0.009), and a bootstrap confidence interval for the difference in ROC-AUC (XGBoost minus Logistic Regression) is +0.012 with a 95% interval of [+0.004, +0.020] that excludes zero. A note of caution is warranted: under five-fold cross-validation the gap narrows (0.792 versus 0.788) and a paired t-test is not significant (p = 0.202). The honest conclusion is that XGBoost is the best model and its edge is real but modest; Logistic Regression remains a defensible choice where transparency is paramount.",
  ]],
  ["2. How could the recommended model be improved?", [
    "Several concrete improvements are available. First, systematic hyper-parameter tuning (for example a cross-validated grid or Bayesian search over tree depth, learning rate, subsampling and regularisation) should widen the current margin, as the model was trained with sensible but untuned defaults and early stopping. Second, the class imbalance (11.3% positive) can be addressed more aggressively: Arifah et al. (2023) report substantial gains on this same dataset by combining XGBoost with SMOTE over-sampling, which should be trialled against the current scale_pos_weight approach. Third, probability calibration (Platt or isotonic) would make the predicted scores more reliable for ranking and budgeting. Fourth, the decision threshold should be set from the client's true cost of a wasted contact versus the value of an activated account rather than from F1 alone. Finally, richer behavioural features - the in-app and engagement signals requested in SS1 - are likely to raise performance well beyond what the public proxy can show. Together these steps form a clear, low-risk optimisation path that can be pursued incrementally, measuring the incremental lift of each change on a fixed validation window before it is accepted.",
  ]],
  ["3. How must the approach be adapted for the SS1 data?", [
    "The public dataset is an analogue, not the client's data, so several adaptations are required before deployment. The client's event-level records (registration, deposits, sessions and marketing touches, as set out in the SS1 data request) must be aggregated to one row per account, and the target redefined as the SS1 activation event - a first qualifying deposit within the 30-day activation window. Care must be taken to exclude any feature that is only observable after the outcome; this mirrors the removal of the call-duration attribute in the public data, which is leakage. Time-aware validation is essential: exploratory analysis of the public data revealed strong non-stationarity (the positive rate drifted from roughly 6% to 38% across the 2008-2010 campaign period), so the client model should be validated on a forward time window and monitored for drift after launch. The engineered features that proved valuable here - prior-contact history and success flags - have direct analogues in the client's behavioural and nudge data and should be reconstructed.",
  ]],
  ["4. Do the results align with the Part A literature?", [
    "Yes. The finding that XGBoost is the best model is consistent with Dias and Antonio (2025), who found gradient boosting superior to logistic regression and other ensembles on an imbalanced customer-behaviour target, and with Arifah et al. (2023), who applied XGBoost to this exact dataset. The importance of macro-economic context in our model (the number of employees and employment-variation rate were the two strongest predictors) echoes Moro, Cortez and Rita (2014), whose central contribution was to show that socio-economic context improves telemarketing prediction. Our absolute ROC-AUC (about 0.81) is lower than some published figures (for example the 0.94 reported by Arifah et al.), which is expected and appropriate: those higher results typically rely on SMOTE and, in some cases, retain the leakage-prone call-duration attribute, whereas this project deliberately excluded duration and applied only in-training imbalance weighting to keep the estimate realistic and deployable. In short, the direction of the evidence agrees with the literature while the absolute numbers reflect the deliberately conservative, leakage-safe design adopted here.",
  ]],
  ["Conclusion", [
    "STADIO Equities should adopt XGBoost as the primary account-activation model, retain Logistic Regression as a transparent challenger, and invest in tuning, imbalance handling and calibration before launch. Once the SS1 data is released, the pipeline should be re-fitted on account-level client data with a leakage-safe 30-day activation target and time-aware validation. The public-data evidence, corroborated by the literature, gives high confidence that the SS1 approach is sound and ready to be proven on the client's own data.",
  ]],
];

const REFERENCES = [
  "Arifah, D., Saragih, T.H., Kartini, D., Muliadi, M. and Mazdadi, M.I. (2023) 'Application of SMOTE to handle imbalance class in deposit classification using the Extreme Gradient Boosting algorithm', <i>Jurnal Ilmiah Teknik Elektro Komputer dan Informatika (JITEKI)</i>, 9(2), pp.396-410. doi:10.26555/jiteki.v9i2.26155.",
  "Dias, J.R. and Antonio, N. (2025) 'Predicting customer churn using machine learning: a case study in the software industry', <i>Journal of Marketing Analytics</i>, 13(1), pp.111-127. doi:10.1057/s41270-023-00269-9.",
  "Moro, S., Cortez, P. and Rita, P. (2014) 'A data-driven approach to predict the success of bank telemarketing', <i>Decision Support Systems</i>, 62, pp.22-31. doi:10.1016/j.dss.2014.03.001.",
];

const children = [
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { after: 40 },
    children: [new TextRun({ text: "Part D – Business Recommendations", bold: true, color: NAVY, size: 32 })],
  }),
  new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ text: "Machine-Learning Capstone (CAP182) · SS2 · STADIO Equities account-activation project", color: "666666", size: 18 })],
  }),
];
for (const [h, paras] of SECTIONS) {
  children.push(H(h));
  for (const p of paras) children.push(P(p));
}
children.push(H("References"));
for (const r of REFERENCES) {
  children.push(new Paragraph({
    spacing: { after: 60 },
    indent: { left: 360, hanging: 360 },
    children: runs(r, { size: 18 }),
  }));
}

const doc = new Document({
  creator: "STADIO Equities Capstone (CAP182)",
  title: "Part D - Business Recommendations",
  sections: [{
    properties: { page: { margin: { top: 1080, bottom: 1080, left: 1584, right: 1584 } } },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("Wrote " + path.relative(ROOT, OUT));
});
