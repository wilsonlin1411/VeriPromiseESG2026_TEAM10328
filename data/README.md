# Data Directory

此資料夾保留可公開的訓練資料與 submission 格式範例。Validation 與 test data 不放在公開 GitHub，請使用者自行依競賽規則取得後放到 Google Drive。

請在 Google Drive 建立：

```text
/content/drive/MyDrive/VeriPromiseESG2026/data/
```

公開 repository 內可包含：

| 檔名 | 用途 | 必要性 |
| --- | --- | --- |
| `vpesg4k_train_1000.json` | Stage 1-5 訓練資料 | 已公開 |
| `sample_submission_format.csv` | 人工核對 submission 欄位格式 | 選用 |

請自行放入 Google Drive，但不要提交到公開 GitHub：

| 檔名 | 用途 | 必要性 |
| --- | --- | --- |
| `vpesg4k_valdata_1000.json` | Stage 1-6 local validation 與診斷資料 | 必要 |
| `vpesg4k_testdata_2000.json` | Stage 1-6 test submission 產生與分布診斷 | 必要 |

Notebooks 會從下列 Drive root 讀取資料：

```python
BASE_DIR = "/content/drive/MyDrive/VeriPromiseESG2026"
```

若 Drive root 不同，請修改每本 notebook 第一個設定區塊的 `BASE_DIR`。
