# hephaestus kill

## 概要

`hephaestus kill` は、すべてのエージェントを停止し、tmuxセッションを終了するコマンドです。

## 使用方法

```bash
hephaestus kill [OPTIONS]
```

## オプション

| オプション | 短縮形 | 説明 |
|-----------|--------|------|
| `--force` | `-f` | 確認プロンプトをスキップして強制終了 |
| `--help` | - | ヘルプメッセージを表示 |

## 動作

1. セッションの存在を確認
2. 確認プロンプトを表示（`--force`オプションがない場合）
3. セッションの状態を保存
4. tmuxセッションを終了
5. すべてのエージェントプロセスを停止

## 使用例

### 通常の終了（確認あり）

```bash
hephaestus kill
```

以下の確認が表示されます：
```
Are you sure you want to kill session 'hephaestus' and stop all agents? [y/N]:
```

### 強制終了（確認なし）

```bash
hephaestus kill --force
```

確認なしで即座にセッションを終了します。

## セッション状態の保存

終了前に、以下の情報が `.hephaestus-work/cache/last_session_state.json` に保存されます：

```json
{
  "session_name": "hephaestus",
  "terminated_at": 1699376400.123,
  "worker_count": 3
}
```

## エラーと対処

### セッションが存在しない

```
No active session found: hephaestus
```

この場合、既にセッションは終了しています。

### 初期化されていない

```
No .hephaestus-work directory found. Nothing to kill.
```

環境が初期化されていない、またはすでにクリーンな状態です。

## 注意事項

- killすると、実行中のタスクも中断されます
- 未完了のタスクは`tasks/in_progress/`に残ります
- 次回起動時に、未完了タスクを確認できます
- `--force`オプションは、スクリプトやCI/CD環境で便利です

## データの保持

以下のデータは終了後も保持されます：

- ✅ タスクファイル（`tasks/`）
- ✅ ログファイル（`logs/`）
- ✅ 通信履歴（`communication/`）
- ✅ 設定ファイル（`config.yaml`）
- ✅ エージェント設定（`.claude/`）

## 再起動

終了後、同じ環境で再起動できます：

```bash
hephaestus attach --create
```

## 関連コマンド

- [hephaestus attach](./attach_ja.md) - セッションの起動
- [hephaestus status](./status_ja.md) - セッション状態の確認
- [hephaestus init](./init_ja.md) - 環境の再初期化
