"""Frozen decision constants of the pre registered experiment (thesis Chapter 3).

This module reconstructs the original ``src/prereg.py`` from the discovery and
confirmation notebooks and from Chapter 3 of the thesis. Diff it against ``FREEZE.md``
before relying on it: every literal below is either quoted from those sources or marked
``RECONSTRUCTED`` where the source did not state the value.

Nothing here reads data. The constants are asserted at import so a family member cannot
be added or dropped without the constant failing, exactly as in the original design.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from .schema import DISCOVERY_FRAMEWORKS, EXCLUDED_FRAMEWORKS, TEST_FRAMEWORKS

# ----------------------------------------------------------------- scope
CODES: Tuple[str, ...] = ("2.2", "2.3", "2.5")
CONFIRMATORY_CODES: Tuple[str, ...] = ("2.2", "2.3")
EXPLORATORY_CODES: Tuple[str, ...] = ("2.5",)
OUT_OF_SCOPE_CODES: Tuple[str, ...] = ("2.6",)

#: Metric columns per code (thesis Table 3), held constant across all windows.
MODEL_COLUMNS: Dict[str, List[str]] = {
    "2.2": ["question_rate", "first_output_pos"],
    "2.3": ["min_task_sim", "drift"],
    "2.5": ["passive_rate"],
}

#: One directional hypothesis per column (thesis Table 4).
DIRECTIONAL_HYPOTHESES: Dict[str, Dict[str, str]] = {
    "2.2": {"question_rate": "positive", "first_output_pos": "negative"},
    "2.3": {"min_task_sim": "negative", "drift": "positive"},
    "2.5": {"passive_rate": "positive"},
}
#: The one direction restated on the discovery half before the test half was opened.
RESTATED_DIRECTIONS: Dict[str, Tuple[str, ...]] = {"2.2": ("question_rate",)}
ORIGINAL_DIRECTIONS: Dict[str, Dict[str, str]] = {"2.2": {"question_rate": "negative"}}
RESTATEMENT_NOTE = (
    "question_rate was initially declared negative on the MAST reading of 2.2 (fewer questions "
    "implies a labelled fail to ask). The discovery half showed the opposite consistently in both "
    "frameworks, so the direction was restated to positive before the test half was opened. "
    "Wherever this direction is confirmed the result is labelled discovery informed and is weaker "
    "evidence than a taxonomy derived prediction held across both halves.")

#: The control block, identical across all codes.
CONTROLS: Tuple[str, ...] = ("log_events", "n_agents")

# --------------------------------------------------------------- windows
WINDOWS: Tuple[str, ...] = ("p25", "p50", "p75", "p100")
LOCALISATION_WINDOW = "p100"
EARLINESS_INFERENTIAL_WINDOW = "p50"
EARLINESS_DESCRIPTIVE_WINDOWS: Tuple[str, ...] = ("p25", "p75", "p100")
EARLINESS_WINDOW_JUSTIFICATION = (
    "p50 is chosen before any label is read: p25 carries the worst undefined rates for the 2.3 "
    "column set (drift needs two comparable segments), and p75 is too close to p100 to support a "
    "claim about earlier identification. An undefined metric at a window is censored, never imputed.")

# -------------------------------------------------------------- the split
EXPECTED_DISCOVERY_N = 927
EXPECTED_TEST_N = 625
EXPECTED_EXCLUDED_N = 90
EXPECTED_DISCOVERY_POSITIVES: Dict[str, int] = {"2.2": 91, "2.3": 192, "2.5": 137}
EXPECTED_TEST_POSITIVES: Dict[str, int] = {"2.2": 142, "2.3": 129, "2.5": 222}
SPLIT_RULE = (
    "Split by framework, not by random trace assignment: a random split would place traces from "
    "the same log dialect on both sides and inflate the held out score, because feature "
    "engineering adapts to a dialect during development. One split serves all three codes "
    "jointly because the codes co occur within traces.")

# ---------------------------------------------------------------- family
#: (code, window, within cell standardised)
BH_FAMILY: List[Tuple[str, str, bool]] = [
    ("2.2", "p100", False),
    ("2.3", "p100", False),
    ("2.2", EARLINESS_INFERENTIAL_WINDOW, False),
    ("2.3", EARLINESS_INFERENTIAL_WINDOW, False),
    ("2.3", "p100", True),
    ("2.3", EARLINESS_INFERENTIAL_WINDOW, True),
]
BH_FAMILY_SIZE = 6
BH_ALPHA = 0.05
STANDARDISATION_SENSITIVITY_CODES: Tuple[str, ...] = ("2.3",)
#: The four distinct row sets (members 5 and 6 reuse the row sets of members 2 and 4).
ROW_SET_ARMS: List[Tuple[str, str]] = [
    ("2.2", "p100"), ("2.3", "p100"),
    ("2.2", EARLINESS_INFERENTIAL_WINDOW), ("2.3", EARLINESS_INFERENTIAL_WINDOW),
]
N_ROW_SETS = 4

#: Row set literals of the original discovery run (author's cleaner), kept as reference.
REFERENCE_ROW_SETS_DISCOVERY: Dict[str, Dict[str, object]] = {
    "member_1_2.2_loc_p100": {"n": 923, "positives": 91, "composition": {"AG2": 597, "ChatDev": 326}},
    "member_2_2.3_loc_p100": {"n": 588, "positives": 169, "composition": {"ChatDev": 326, "AG2": 262}},
    "member_3_2.2_early_p50": {"n": 923, "positives": 91, "composition": {"AG2": 597, "ChatDev": 326}},
    "member_4_2.3_early_p50": {"n": 335, "positives": 154, "composition": {"ChatDev": 326, "AG2": 9}},
}

#: The metric tables the original experiment froze before the test half was opened, with the
#: file sha256 its FREEZE.md pins (section 12). The experiment notebooks read these tables
#: instead of recomputing the columns, because the reimplemented ``prereg_windows`` detector
#: does not reproduce the frozen definitions. Copied from the original repository's
#: ``Framework_Traces/experiment/data/cache/`` and ``data/sealed/``.
FROZEN_METRIC_TABLES: Dict[str, Dict[str, str]] = {
    "discovery": {"path": "frozen/metrics_discovery.parquet",
                  "sha256": "6c67aa70dc19e89dfe3b6121c875ea11d66ece36062ca18484d2196dfcbee7a8"},
    "test": {"path": "sealed/test_metrics.parquet",
             "sha256": "5a10e7bf21659b0454d99a62a1828477e319b2d4177ba7c0e7ff5e2d5a3717f3"},
}

#: Seed of the stratified folds in the original discovery notebook (``CV_SEED = 0``).
CV_SEED = 0

#: Specificity check of the original pre-registration (src/prereg.py, src/loading.py): the
#: metric blocks against the aggregated MAST group 1 and group 3 labels, outside the family,
#: reported uncorrected and bounded by the caveat below, which must appear as written.
SPECIFICITY_LABELS: Tuple[str, ...] = ("group1_any", "group3_any")
GROUP1_CODES: Tuple[str, ...] = ("1.1", "1.2", "1.3", "1.4", "1.5")
GROUP3_CODES: Tuple[str, ...] = ("3.1", "3.2", "3.3")
SPECIFICITY_IN_BH_FAMILY: bool = False
SPECIFICITY_CAVEAT: str = (
    "Failure to reject the null for MAST groups 1 and 3 is weak evidence that these "
    "metrics are specific to inter-agent misalignment, not proof of it. A non-significant "
    "result is consistent with specificity and equally consistent with insufficient power "
    "on those groups' row sets. No equivalence test with a pre-specified margin was "
    "declared, so no claim of equivalence is available either; the specificity discussion "
    "is therefore suggestive and is labelled as such wherever it appears."
)

FAMILY_MEMBERSHIP_RULE = (
    "Anything interpreted as evidence for or against the research question is a member, not "
    "everything that emits a p value, and not only the primary tests. Cross validation and leave "
    "one framework out produce no p value and are used only to argue against positive arms, so "
    "there is nothing for Benjamini Hochberg to protect against.")
CV_LOFO_EXCLUSION_REASON = (
    "Out of sample behaviour is allowed to weaken but never to strengthen a conclusion: an arm "
    "that failed its likelihood ratio test is not rehabilitated by a good held out score, and a "
    "confirmatory arm that fails here has failed.")

# --------------------------------------------------- framework internal arms
#: Amendment 1: the standardised model on one test framework's own rows (2 codes x 2 frameworks x 2 windows).
FRAMEWORK_INTERNAL_ARMS: List[Tuple[str, str, str]] = [
    (code, fw, window)
    for code in CONFIRMATORY_CODES
    for fw in TEST_FRAMEWORKS
    for window in (LOCALISATION_WINDOW, EARLINESS_INFERENTIAL_WINDOW)
]
FRAMEWORK_INTERNAL_ARMS_MAX = 8
FRAMEWORK_INTERNAL_MIN_POSITIVES = 20
FRAMEWORK_INTERNAL_MIN_NEGATIVES = 20
FRAMEWORK_INTERNAL_MAX_SE = 10.0
FRAMEWORK_INTERNAL_GATE = (
    "(a) at least 20 positives and 20 negatives; (b) convergence without perfect separation and "
    "every metric standard error below 10 on the standardised scale; (c) non zero variance in "
    "every model column. The gate reads row counts and convergence diagnostics only, never a p value.")
BH_FAMILY_SIZE_MIN = 6
BH_FAMILY_SIZE_MAX = 14

CONFIRMATION_MODE = "refit"
CONFIRMATION_REFITS_COEFFICIENTS = True
CONFIRMATION_FROZEN: Tuple[str, ...] = (
    "model column sets per code (MODEL_COLUMNS)",
    "window per analysis (localisation p100; earliness EARLINESS_INFERENTIAL_WINDOW)",
    "row set rule per arm (complete cases on that arm's columns at that window)",
    "test statistic (likelihood ratio, full model versus control only model)",
    "the control block (log_events, n_agents), identical across all codes",
    "family membership, family size, alpha and the BH correction",
    "the directional hypothesis per code",
)
CONFIRMATION_NOT_FROZEN: Tuple[str, ...] = (
    "regression coefficients, including the control coefficients",
    "the intercept and hence the base rate",
    "any standardisation constants (see the 2.3 within cell sensitivity analysis)",
)

# ----------------------------------------------------------- diagnostics
VIF_FLAG_THRESHOLD = 5.0          # RECONSTRUCTED: not stated in the uploaded material
VIF_MIN_FRAMEWORK_SHARE = 0.20    # RECONSTRUCTED: not stated in the uploaded material
DISCOVERY_MIN_CELL = 20
DISCOVERY_MIN_PER_CLASS = 5

#: Columns removed by the label free degeneracy rule (modal share >= 0.95 at every window).
EXCLUDED_BY_DEGENERACY: Dict[str, str] = {
    "clarify_before_output": "near constant on MetaGPT",
    "unanswered_share": "near constant on MetaGPT",
    "keyword_coverage": "near constant on ChatDev, a prompt echo artefact",
    "reply_latency": "constant on AG2 and Magentic, a construct failure rather than a transfer failure",
}

# ----------------------------------------------------------- the readings
CONTRARY_SIGN_RULE = (
    "A metric whose fitted coefficient opposes its declared direction is reported as contrary, "
    "not silently absorbed into a significant block. The sentence stating that a direction opposes "
    "the pre registration appears before its magnitude.")

EARLINESS_NULL_SENTENCE = (
    "The earliness test was pre-registered at a single window (p50) chosen before the data on "
    "definedness grounds. A non-significant result at that window means no earliness claim is "
    "supported by this experiment. The prefix curve at p25, p75 and p100 is reported as description "
    "only and carries no inferential weight: those windows were declared descriptive in advance, "
    "they were not corrected for as part of the family, and an apparent effect at any of them is a "
    "hypothesis for a future confirmation on data not used here, not a finding of this study. In "
    "particular, significance at p75 would not license the claim that failures are detectable "
    "before a run ends.")

EARLINESS_ROW_SET_CAVEAT = (
    "The earliness arms run on the rows where the metrics are defined at the pre-registered window, "
    "which is not the localisation row set. Any earliness claim for 2.3 is therefore conditional: it "
    "holds among traces where these metrics are defined at that point, and a rise in prevalence "
    "between windows is composition and not a change in the traces themselves.")

PREDICTION_2_3_TEST_HALF = (
    "Predicted for MetaGPT and Magentic: the pooled 2.3 model rejects its control model (members 2 "
    "and 4 significant after BH), and the within-framework-cell standardised model does not (members "
    "5 and 6 not significant after BH). Outcomes fixed in advance: (a) prediction holds -- the "
    "framework-offset explanation is supported on a framework pair sharing nothing with the "
    "discovery pair, and this class of metric carries between-system level information rather than "
    "a within-system association with the label; (b) the standardised model also survives -- the "
    "artifact explanation is WRONG, the within-framework association is real, and the discovery-half "
    "dissolution was specific to the ChatDev/AG2 pair; (c) the pooled model does not reject its "
    "control model either -- the effect does not reproduce at all, which is a null on the primary "
    "endpoint and is reported as one, not as indirect support for (a).")
PREDICTION_2_3_ASYMMETRY_CAVEAT = (
    "The standardised member's outcome carries no reading unless the unstandardised member is "
    "significant first.")

PREDICTION_FRAMEWORK_INTERNAL = (
    "Predicted: within-framework arms significant after BH, pooled arms not. Outcomes fixed in "
    "advance: (a) within-framework significant and pooled not -- the calibration reading is "
    "supported: trajectory metrics localise failure within a system while transferring poorly "
    "across systems. (b) both significant -- pooling is not destructive on this framework pair and "
    "the discovery-half offset was specific to ChatDev/AG2. (c) neither significant -- the metrics "
    "do not reproduce on unseen frameworks even under calibration, a null on the strongest "
    "available claim reported as the primary result. (d) within-framework null while pooled "
    "significant -- the pooled effect is between-system level information only, which contradicts "
    "the calibration reading and is reported as contradicting it.")

DISCOVERY_STANDARDISATION_CAVEAT = (
    "Agreement of the 2.3 earliness arm under within-cell standardisation is close to arithmetic "
    "necessity when the arm is almost a single framework, so it cannot later be read as robustness "
    "the localisation arm lacked.")

GOVERNING_PRINCIPLE = "A pre-registered null with a diagnosed mechanism is a result, not a disappointment."

# ------------------------------------------------------------ assertions
assert len(BH_FAMILY) == BH_FAMILY_SIZE, "BH family size drifted from the frozen literal"
assert len(ROW_SET_ARMS) == N_ROW_SETS
assert sum(std for _, _, std in BH_FAMILY) == 2 * len(STANDARDISATION_SENSITIVITY_CODES)
assert len(FRAMEWORK_INTERNAL_ARMS) == FRAMEWORK_INTERNAL_ARMS_MAX
assert BH_FAMILY_SIZE_MIN == BH_FAMILY_SIZE
assert BH_FAMILY_SIZE_MAX == BH_FAMILY_SIZE + FRAMEWORK_INTERNAL_ARMS_MAX
assert set(DISCOVERY_FRAMEWORKS) == {"ChatDev", "AG2"}
assert set(TEST_FRAMEWORKS) == {"MetaGPT", "Magentic"}
assert set(EXCLUDED_FRAMEWORKS) == {"AppWorld", "HyperAgent", "OpenManus"}
assert all(m in DIRECTIONAL_HYPOTHESES[c] for c in MODEL_COLUMNS for m in MODEL_COLUMNS[c])


def declared_direction(code: str, metric: str) -> str:
    return DIRECTIONAL_HYPOTHESES[code][metric]


def is_restated(code: str, metric: str) -> bool:
    return metric in RESTATED_DIRECTIONS.get(code, ())
