# hephaestus monitor

## 概要

`hephaestus monitor` は、タスクの配布を監視し、自動的にWorkerエージェントに通知するコマンドです。

## 使用方法

```bash
hephaestus monitor [OPTIONS]
```

## オプション

| オプション | 短縮形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--interval` | `-i` | 5 | タスクチェック間隔（秒） |
| `--max-iterations` | `-m` | 120 | 最大監視回数（約10分） |
| `--help` | - | - | ヘルプメッセージを表示 |

## 動作

1. `communication/master_to_worker/` ディレクトリを監視
2. 新しいタスク割り当てファイルを検出
3. 該当するWorkerにtmux経由で通知
4. Worker がタスクを受信・実行
5. 定期的にステータスを表示

## 使用例

### 基本的な監視

```bash
hephaestus monitor
```

デフォルト設定（5秒間隔、120回まで）で監視を開始します。

### カスタム間隔で監視

```bash
# 10秒間隔でチェック
hephaestus monitor --interval 10

# 2秒間隔でチェック（高頻度）
hephaestus monitor -i 2
```

### 長時間監視

```bash
# 300回まで監視（約25分、5秒間隔）
hephaestus monitor --max-iterations 300

# 600回まで監視（約50分、5秒間隔）
hephaestus monitor -m 600
```

## 監視出力

```
┌─────────────────── Task Monitor Started ───────────────────┐
│ Monitoring task distribution                               │
│                                                            │
│ Session: hephaestus                                        │
│ Workers: 3                                                 │
│ Check interval: 5s                                         │
│ Max duration: ~10 minutes                                  │
└────────────────────────────────────────────────────────────┘

Press Ctrl+C to stop monitoring

[10:15:30] New task detected: task_001.md → worker-1
[10:15:35] Task acknowledged by worker-1
[10:16:20] Task completed by worker-1
[10:16:25] New task detected: task_002.md → worker-2
...
```

## 停止方法

### 手動停止

`Ctrl+C` を押すと監視が停止し、ステータスサマリーが表示されます：

```
Monitoring stopped by user
Tasks: 5 total, 3 completed
```

### 自動停止

最大監視回数に達すると自動的に停止します：

```
✓ Monitoring completed
Tasks: 5 total, 5 completed
```

## 通知方式

Monitorは以下の方法でWorkerに通知します：

1. **tmux send-keys**: Workerのペインに直接メッセージを送信
2. **通知メッセージ**: `"New task assigned! Please read [filename]..."`
3. **ファイルパス指定**: タスクファイルの場所を明示

## エラーと対処

### セッションが起動していない

```
No active session found: hephaestus

Start the session first with: hephaestus attach --create
```

**対処**: まずセッションを起動してください。

### 初期化されていない

```
Not initialized. Run 'hephaestus init' first.
```

**対処**: `hephaestus init` を実行してください。

## 使用シーン

### 開発・デバッグ時

```bash
# 短い間隔で監視
hephaestus monitor -i 2 -m 30
```

### 本番運用時

```bash
# 長時間安定監視
hephaestus monitor -i 10 -m 1000
```

### バックグラウンド実行

```bash
# nohupでバックグラウンド実行
nohup hephaestus monitor -i 5 -m 500 > monitor.log 2>&1 &
```

## 監視される情報

- 新規タスク割り当て
- Worker応答
- タスク完了通知
- エラー発生

## 注意事項

- Monitorは読み取り専用で、タスクの変更はしません
- 複数のMonitorを同時に実行しても問題ありません
- tmuxセッションとは独立して動作します

## 関連コマンド

- [hephaestus attach](./attach_ja.md) - セッションの起動（必須）
- [hephaestus dashboard](./dashboard_ja.md) - グラフィカルな監視
- [hephaestus logs](./logs_ja.md) - 詳細なログ確認
- [hephaestus status](./status_ja.md) - 現在の状態確認
