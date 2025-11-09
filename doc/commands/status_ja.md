# hephaestus status

## 概要

`hephaestus status` は、Hephaestusの現在の状態を表示するコマンドです。

## 使用方法

```bash
hephaestus status
```

## 表示内容

以下の情報が表示されます：

- **Work Directory**: .hephaestus-workディレクトリのパス
- **Tmux Session**: tmuxセッション名
- **Session Active**: セッションが起動しているかどうか
- **Worker Count**: Workerエージェントの数

## 出力例

```
                Hephaestus Status
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component      ┃ Status                           ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Work Directory │ /path/to/.hephaestus-work         │
│ Tmux Session   │ hephaestus                       │
│ Session Active │ Yes                              │
│ Worker Count   │ 3                                │
└────────────────┴──────────────────────────────────┘
```

## 使用例

### 基本的な使用

```bash
hephaestus status
```

### スクリプトでの使用

```bash
# セッションが起動しているか確認
if hephaestus status | grep -q "Session Active.*Yes"; then
    echo "Hephaestus is running"
else
    echo "Hephaestus is not running"
fi
```

## セッションの状態

### 起動中

```
Session Active │ Yes
```

セッションが正常に起動し、エージェントが動作しています。

### 停止中

```
Session Active │ No
```

セッションが起動していません。`hephaestus attach --create` で起動できます。

## エラーと対処

### 初期化されていない

```
Not initialized. Run 'hephaestus init' first.
```

**対処**: まず `hephaestus init` を実行してください。

## 関連コマンド

- [hephaestus init](./init_ja.md) - 環境の初期化
- [hephaestus attach](./attach_ja.md) - セッションの起動/アタッチ
- [hephaestus dashboard](./dashboard_ja.md) - 詳細な状態監視
- [hephaestus logs](./logs_ja.md) - ログの確認
