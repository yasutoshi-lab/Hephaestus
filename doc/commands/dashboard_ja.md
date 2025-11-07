# hephaestus dashboard

## 概要

`hephaestus dashboard` は、エージェントの状態をリアルタイムで監視するためのTUI（Terminal User Interface）ダッシュボードを起動します。

## 使用方法

```bash
hephaestus dashboard
```

## 機能

ダッシュボードでは以下の情報がリアルタイムで表示されます：

### 1. エージェントステータス
- 各エージェント（Master、Worker-1、Worker-2...）の現在の状態
- ステータスインジケーター：
  - 🟢 **Active**: エージェントが正常に動作中
  - 🟡 **Idle**: エージェントは起動しているがタスクなし
  - 🔴 **Error**: エージェントにエラーが発生
  - ⚪ **Unknown**: セッションが起動していない

### 2. タスク概要テーブル
- タスクID
- ステータス（pending/in_progress/completed）
- 優先度
- 割り当て先のエージェント

### 3. 通信ログストリーム
- エージェント間の通信メッセージをリアルタイム表示
- 最新100行まで保持

## キーバインド

| キー | 機能 |
|------|------|
| `q` | ダッシュボードを終了 |
| `r` | 手動で画面を更新 |
| `^p` | コマンドパレットを開く |

## 自動更新

ダッシュボードは2秒ごとに自動的に情報を更新します。

## 使用例

### 基本的な使用

```bash
# ダッシュボードを起動
hephaestus dashboard
```

### セッション起動中のダッシュボード

```bash
# 別ターミナルでセッションを起動
terminal1$ hephaestus attach --create

# もう一つのターミナルでダッシュボードを表示
terminal2$ hephaestus dashboard
```

これにより、エージェントの動作をリアルタイムで監視できます。

## 警告とエラー

### セッションが起動していない場合

```
Warning: No active session found

The dashboard will show limited information.
Start the session with: hephaestus attach --create
```

この場合、ダッシュボードは起動しますが、すべてのエージェントが"Unknown"状態として表示されます。

### 初期化されていない場合

```
Not initialized. Run 'hephaestus init' first.
```

**対処**: まず`hephaestus init`を実行してください。

## ダッシュボード画面レイアウト

```
┌─────────────────────────────────────────────────────────┐
│            Hephaestus Dashboard              02:42:04   │
├─────────────────────────────────────────────────────────┤
│ Agent Status                                            │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│ │🟢 Master    │ │🟢 Worker-1  │ │🟢 Worker-2  │       │
│ │Status: Act..│ │Status: Act..│ │Status: Act..│       │
│ │Task: Analy..│ │Task: Execu..│ │Task: Gener..│       │
│ └─────────────┘ └─────────────┘ └─────────────┘       │
│                                                         │
│ Tasks Overview                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ID    │ Status      │ Priority │ Assigned To      │ │
│ │ t-001 │ in_progress │ high     │ worker-1         │ │
│ │ t-002 │ pending     │ medium   │ worker-2         │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Communication Log                                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 02:42:10 master -> worker-1: New task assigned...  │ │
│ │ 02:42:11 worker-1 -> master: Task acknowledged     │ │
│ │ 02:42:15 worker-1 -> master: Task completed        │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ q Quit  r Refresh                          ^p palette │
└─────────────────────────────────────────────────────────┘
```

## パフォーマンス

- ダッシュボードは軽量で、システムリソースをほとんど使用しません
- 大量のタスクやログがある場合でも、最新の情報のみを表示するため高速です

## 注意事項

- ダッシュボードは読み取り専用です（エージェントの操作はできません）
- tmuxセッション内では起動しないでください（別のターミナルウィンドウで起動推奨）
- ダッシュボードを終了してもエージェントセッションには影響しません

## トラブルシューティング

### 画面が正しく表示されない

ターミナルのサイズを確認してください。最小推奨サイズ：
- 幅: 80文字以上
- 高さ: 24行以上

### 情報が更新されない

`r`キーを押して手動更新を試してください。

## 関連コマンド

- [hephaestus attach](./attach_ja.md) - エージェントセッションの起動
- [hephaestus logs](./logs_ja.md) - ログの詳細表示
- [hephaestus status](./status_ja.md) - ステータスの簡易確認
- [hephaestus monitor](./monitor_ja.md) - タスク配布の監視

## 技術詳細

ダッシュボードは[Textual](https://github.com/Textualize/textual)フレームワークを使用して実装されています。
