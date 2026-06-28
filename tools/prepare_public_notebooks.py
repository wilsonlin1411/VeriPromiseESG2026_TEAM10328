# -*- coding: utf-8 -*-
"""Prepare public-facing Colab notebooks.

This script rewrites the public header/setup/contract cells, strips execution
outputs, and removes Colab runtime metadata that may contain personal account
information. It is intentionally repo-local so future notebook regeneration can
repeat the same cleanup step before publishing.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"

COMMON_PIP = "transformers accelerate scikit-learn pandas numpy tqdm openpyxl"
STAGE6_PIP = "pandas numpy scikit-learn openpyxl"


STAGES = {
    "Stage1_macbert_multitask_baseline.ipynb": {
        "stage_name": "stage1_macbert_multitask_baseline",
        "display": "Stage 1 - MacBERT 多任務基準模型",
        "title": "# Stage 1: MacBERT 多任務基準模型",
        "summary": "訓練 MacBERT multi-task 5-fold baseline，產生 Stage 2 需要的 OOF/test 機率檔與第一版 submission。",
        "pip": COMMON_PIP,
        "inputs": [
            "data/vpesg4k_train_1000.json",
            "data/vpesg4k_valdata_1000.json",
            "data/vpesg4k_testdata_2000.json",
        ],
        "outputs": [
            "stage1_oof_val_test_probs.pkl",
            "stage1_val1000_predictions.csv",
            "stage1_metrics.json",
            "stage1_baseline_test2000_submission.csv",
        ],
        "section": "本節訓練 baseline 模型，並以固定檔名輸出後續 Stage 需要的 probability artifact。",
    },
    "Stage2_ckip_taskwise_ensemble.ipynb": {
        "stage_name": "stage2_ckip_taskwise_ensemble",
        "display": "Stage 2 - CKIP 任務別集成",
        "title": "# Stage 2: CKIP 任務別集成與後處理",
        "summary": "讀取 Stage 1 機率檔，訓練 CKIP 任務別模型，搜尋後處理與任務別 ensemble 設定。",
        "pip": COMMON_PIP,
        "inputs": [
            "data/vpesg4k_train_1000.json",
            "data/vpesg4k_valdata_1000.json",
            "data/vpesg4k_testdata_2000.json",
            "outputs/stage1_macbert_multitask_baseline/stage1_oof_val_test_probs.pkl",
        ],
        "outputs": [
            "stage2_postprocess_best_config.json",
            "stage2_ckip_oof_val_test_probs.pkl",
            "stage2_best_val_config.json",
            "stage2_best_val_test2000_submission.csv",
            "stage2_balanced_test2000_submission.csv",
        ],
        "section": "本節先重建 Stage 1 後處理版本，再加入 CKIP 任務別模型進行 ensemble。",
    },
    "Stage3_tta_t4_specialist_blend.ipynb": {
        "stage_name": "stage3_tta_t4_specialist_blend",
        "display": "Stage 3 - TTA 與 T4 Specialist 融合",
        "title": "# Stage 3: TTA 與 T4 Specialist 融合",
        "summary": "讀取 Stage 1/2 artifacts，加入 evidence quality specialist 與 head/middle/tail TTA 融合。",
        "pip": COMMON_PIP,
        "inputs": [
            "data/vpesg4k_train_1000.json",
            "data/vpesg4k_valdata_1000.json",
            "data/vpesg4k_testdata_2000.json",
            "outputs/stage1_macbert_multitask_baseline/stage1_oof_val_test_probs.pkl",
            "outputs/stage2_ckip_taskwise_ensemble/stage2_ckip_oof_val_test_probs.pkl",
            "outputs/stage2_ckip_taskwise_ensemble/stage2_best_val_config.json",
        ],
        "outputs": [
            "stage3_t4_specialist_probs.pkl",
            "stage3_3view_probs.pkl",
            "stage3_best_config.json",
            "stage3_best_val_test2000_submission.csv",
            "stage3_conservative_test2000_submission.csv",
        ],
        "section": "本節針對 evidence_quality 與多視角推論做補強，輸出 Stage 4 會讀取的 TTA probability artifact。",
    },
    "Stage4_t2_specialist_calibration.ipynb": {
        "stage_name": "stage4_t2_specialist_calibration",
        "display": "Stage 4 - T2 Specialist 與 Cue Calibration",
        "title": "# Stage 4: T2 Specialist 與 Cue Calibration",
        "summary": "讀取 Stage 3 artifacts，訓練 verification timeline specialist，並進行 cue calibration 與保守版搜尋。",
        "pip": COMMON_PIP,
        "inputs": [
            "data/vpesg4k_train_1000.json",
            "data/vpesg4k_valdata_1000.json",
            "data/vpesg4k_testdata_2000.json",
            "outputs/stage3_tta_t4_specialist_blend/stage3_t4_specialist_probs.pkl",
            "outputs/stage3_tta_t4_specialist_blend/stage3_3view_probs.pkl",
            "outputs/stage3_tta_t4_specialist_blend/stage3_best_config.json",
        ],
        "outputs": [
            "stage4_t2_specialist_probs.pkl",
            "stage4_t2_best_config.json",
            "stage4_conservative_config.json",
            "stage4_config.json",
            "stage4_best_val_test2000_submission.csv",
            "stage4_safe_test2000_submission.csv",
        ],
        "section": "本節補強 verification_timeline，並動態過濾 optional base choice，避免缺少候選來源時中斷。",
    },
    "Stage5_model_bank_final_submission.ipynb": {
        "stage_name": "stage5_model_bank_final_submission",
        "display": "Stage 5 - Model Bank 最終提交",
        "title": "# Stage 5: Model Bank 最終提交",
        "summary": "讀取 Stage 3/4 artifacts，進行 minority augmentation、T2 mini model bank search，產生 final submission 候選。",
        "pip": COMMON_PIP,
        "inputs": [
            "data/vpesg4k_train_1000.json",
            "data/vpesg4k_valdata_1000.json",
            "data/vpesg4k_testdata_2000.json",
            "outputs/stage3_tta_t4_specialist_blend/stage3_t4_specialist_probs.pkl",
            "outputs/stage3_tta_t4_specialist_blend/stage3_3view_probs.pkl",
            "outputs/stage3_tta_t4_specialist_blend/stage3_best_config.json",
            "outputs/stage4_t2_specialist_calibration/stage4_t2_specialist_probs.pkl",
            "outputs/stage4_t2_specialist_calibration/stage4_t2_best_config.json",
            "outputs/stage4_t2_specialist_calibration/stage4_conservative_config.json",
            "outputs/stage4_t2_specialist_calibration/stage4_config.json",
        ],
        "outputs": [
            "stage5_t2_aug_specialist_probs.pkl",
            "stage5_augmentation_config.json",
            "stage5_config.json",
            "stage5_best_val_test2000_submission.csv",
            "stage5_low_risk_high_score_test2000_submission.csv",
            "stage5_safe_test2000_submission.csv",
        ],
        "section": "本節整合 Stage 3/4 的 probability sources，動態過濾不可用候選，產生最終 submission 候選。",
    },
    "Stage6_submission_diagnostic_optional.ipynb": {
        "stage_name": "stage6_submission_diagnostic_optional",
        "display": "Stage 6 - Submission 診斷",
        "title": "# Stage 6: Submission 診斷與推薦",
        "summary": "掃描前面 stages 的 validation predictions 與 test submissions，比較 validation score、group stability 與 test distribution risk。",
        "pip": STAGE6_PIP,
        "inputs": [
            "data/vpesg4k_train_1000.json",
            "data/vpesg4k_valdata_1000.json",
            "data/vpesg4k_testdata_2000.json",
        ],
        "outputs": [
            "stage6_version_summary.csv",
            "stage6_test_distribution_risk.csv",
            "stage6_recommendation.csv",
            "stage6_submission_diagnostic.xlsx",
            "stage6_report.md",
        ],
        "section": "本節不訓練模型，主要用於彙整前面 stages 的 val/test 輸出並產生提交建議。",
    },
}


REPORT_TITLE_REPLACEMENTS = {
    "# v30 val1000 MacBERT multitask clean pipeline report": "# Stage 1 MacBERT 多任務基準模型報告",
    "# stage2 CKIP + MacBERT task-wise ensemble report": "# Stage 2 CKIP + MacBERT 任務別集成報告",
    "# v34 combine v33 timeline + v32 T4 report": "# Stage 3 TTA 與 T4 Specialist 融合報告",
    "# Stage 4 Cue Feature Layer Calibration Report": "# Stage 4 T2 Specialist 與 Cue Calibration 報告",
    "# Stage 5 Mini Model Bank Ensemble Report": "# Stage 5 Model Bank 最終提交報告",
    "# v38_00 GroupKFold / Company Split Diagnostic Report": "# Stage 6 Submission 診斷報告",
}


def md_list(items: list[str]) -> str:
    return "".join(f"- `{item}`\n" for item in items)


def setup_source(cfg: dict[str, object]) -> str:
    req_lines = "".join(f'    "{p}",\n' for p in cfg["inputs"])
    return f'''# Colab 啟動區塊：安裝套件、掛載 Drive、檢查 GPU、驗證必要輸入檔。
!pip -q install {cfg["pip"]}

from google.colab import drive
drive.mount('/content/drive')

import os
from pathlib import Path

BASE_DIR = "/content/drive/MyDrive/VeriPromiseESG2026"
DATA_DIR = f"{{BASE_DIR}}/data"
OUTPUT_ROOT = f"{{BASE_DIR}}/outputs"
STAGE_NAME = "{cfg["stage_name"]}"
STAGE_DISPLAY_NAME = "{cfg["display"]}"
OUTPUT_DIR = f"{{OUTPUT_ROOT}}/{{STAGE_NAME}}"
OUT_DIR = OUTPUT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

REQUIRED_RELATIVE_PATHS = [
{req_lines}]

def stage_log(label, value):
    print(f"[{{STAGE_NAME}}] {{label}}: {{value}}")

def require_files(relative_paths):
    missing = []
    for rel in relative_paths:
        path = f"{{BASE_DIR}}/{{rel}}"
        if not os.path.exists(path):
            missing.append(path)
    if missing:
        msg = "缺少必要輸入檔。請先執行前一個 Stage，或將資料放到 Google Drive：\\n" + "\\n".join(missing)
        raise FileNotFoundError(msg)

require_files(REQUIRED_RELATIVE_PATHS)
stage_log("Stage", STAGE_DISPLAY_NAME)
stage_log("BASE_DIR", BASE_DIR)
stage_log("DATA_DIR", DATA_DIR)
stage_log("OUTPUT_DIR", OUTPUT_DIR)

# 完整訓練建議使用 Colab A100 或同級 GPU。
try:
    gpu_names = !nvidia-smi --query-gpu=name --format=csv,noheader
    gpu_names = list(gpu_names)
    stage_log("GPU", gpu_names)
    if not any("A100" in str(name) for name in gpu_names):
        stage_log("WARNING", "建議使用 A100；非 A100 runtime 可能需要更長時間。")
except Exception as exc:
    stage_log("WARNING", f"無法取得 GPU 資訊，請確認 Colab runtime 已啟用 GPU。{{exc}}")
'''


def intro_markdown(cfg: dict[str, object]) -> str:
    return f'''{cfg["title"]}

{cfg["summary"]}

預設 Drive root：`/content/drive/MyDrive/VeriPromiseESG2026`。
'''


def env_markdown() -> str:
    return '''## 0. Colab 執行環境與路徑檢查

請先執行下一個 setup cell。它會安裝套件、掛載 Google Drive、檢查 GPU、建立輸出資料夾，並驗證必要輸入檔是否存在。
'''


def contract_markdown(cfg: dict[str, object]) -> str:
    return f'''## 輸入輸出契約

Stage 顯示名稱：`{cfg["display"]}`

Google Drive 輸出資料夾：

```text
/content/drive/MyDrive/VeriPromiseESG2026/outputs/{cfg["stage_name"]}/
```

必要輸入檔：

{md_list(cfg["inputs"])}
主要輸出檔：

{md_list(cfg["outputs"])}
若必要輸入不存在，第一個 setup cell 會直接列出缺少的路徑並停止。
'''


def section_markdown(cfg: dict[str, object]) -> str:
    return f'''## Stage 主要流程

{cfg["section"]}
'''


def split_source(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def prepare_notebook(path: Path, cfg: dict[str, object]) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook["cells"]

    cells[0]["cell_type"] = "markdown"
    cells[0]["source"] = split_source(intro_markdown(cfg))
    cells[1]["cell_type"] = "markdown"
    cells[1]["source"] = split_source(env_markdown())
    cells[2]["cell_type"] = "code"
    cells[2]["source"] = split_source(setup_source(cfg))
    cells[3]["cell_type"] = "markdown"
    cells[3]["source"] = split_source(contract_markdown(cfg))
    cells[4]["cell_type"] = "markdown"
    cells[4]["source"] = split_source(section_markdown(cfg))

    for cell in cells:
        source = "".join(cell.get("source", []))
        for old, new in REPORT_TITLE_REPLACEMENTS.items():
            source = source.replace(old, new)
        cell["source"] = split_source(source)

        metadata = cell.setdefault("metadata", {})
        metadata.pop("executionInfo", None)
        metadata.pop("outputId", None)
        metadata.pop("colab", None)

        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    notebook["metadata"] = {
        "colab": {"provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    }

    path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for filename, cfg in STAGES.items():
        path = NOTEBOOK_DIR / filename
        prepare_notebook(path, cfg)
        print(f"prepared {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
