# 遺伝カウンセリング教育システム セットアップガイド

## 概要
このシステムは、ローカルLLMを使用した遺伝カウンセリング教育システムです。学生と教官が患者シミュレーションを通じてカウンセリングスキルを向上させることができます。

## 必要な環境
- Python 3.12+
- Node.js 18+
- Poetry (Python依存関係管理)
- npm/yarn (Node.js依存関係管理)
- Ollama (ローカルLLM実行環境)

## インストール手順

### 1. Ollamaのインストール
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. LLMモデルのダウンロード
```bash
ollama pull llama2
```

### 3. バックエンドのセットアップ
```bash
cd backend
poetry install
```

### 4. フロントエンドのセットアップ
```bash
cd frontend
npm install
```

## 起動方法

### 1. Ollamaサービスの開始
```bash
ollama serve
```

### 2. バックエンドの起動
```bash
cd backend
poetry run fastapi dev app/main.py
```

### 3. フロントエンドの起動
```bash
cd frontend
npm run dev
```

### 4. アクセス
ブラウザで http://localhost:5173 にアクセス

## 設定管理

### Hydra設定ファイル
- `configs/config.yaml` - メイン設定
- `configs/model/` - LLMモデル設定
- `configs/prompt/` - 患者シナリオ設定
- `configs/ui/` - UI設定

### 設定の変更
1. UIの「設定」タブから変更
2. 設定ファイルを直接編集
3. APIエンドポイント経由で変更

## 使用方法

### 1. セッション作成
1. 「新しいセッション」ボタンをクリック
2. ユーザーID、患者シナリオ、LLMモデルを選択
3. 「セッション開始」をクリック

### 2. カウンセリング実習
1. チャット画面でカウンセラーとして質問
2. AIが患者として応答
3. 会話を通じてカウンセリングスキルを練習

### 3. 設定変更
1. 「設定」タブでモデルパラメータを調整
2. 「患者シナリオ」タブで患者設定を変更
3. 「UI設定」タブでインターフェースをカスタマイズ

## トラブルシューティング

### Ollamaが起動しない
```bash
sudo systemctl start ollama
```

### モデルが見つからない
```bash
ollama list
ollama pull llama2
```

### ポートが使用中
- バックエンド: ポート8000
- フロントエンド: ポート5173
- Ollama: ポート11434

## 開発者向け情報

### アーキテクチャ
- バックエンド: FastAPI + Python
- フロントエンド: React + TypeScript + Vite
- 設定管理: Hydra + OmegaConf
- LLM: Ollama (ローカル実行)

### API エンドポイント
- `GET /config` - 設定取得
- `POST /config/update` - 設定更新
- `POST /sessions` - セッション作成
- `POST /chat` - チャット送信
- `GET /health` - ヘルスチェック

### 設定ファイル構造
```yaml
model:
  name: "llama2"
  type: "ollama"
  model_id: "llama2"
  temperature: 0.7
  max_tokens: 2048

prompt:
  name: "default_patient"
  system_prompt: "患者の設定..."
  
ui:
  layout:
    sidebar_width: 300
    chat_height: 600
```
