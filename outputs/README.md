# Outputs Directory

此資料夾只保留輸出說明；模型 checkpoint、中間機率檔、submission 與診斷報告不應提交到公開 GitHub。

Notebooks 會將輸出寫入 Google Drive：

```text
/content/drive/MyDrive/VeriPromiseESG2026/outputs/
```

固定 Stage 輸出資料夾如下：

```text
stage1_macbert_multitask_baseline/
stage2_ckip_taskwise_ensemble/
stage3_tta_t4_specialist_blend/
stage4_t2_specialist_calibration/
stage5_model_bank_final_submission/
stage6_submission_diagnostic_optional/
```

每個 Stage 會建立自己的輸出資料夾，並寫出下一個 Stage 需要讀取的固定檔名。完整輸入輸出對應請見根目錄 `README.md`。
