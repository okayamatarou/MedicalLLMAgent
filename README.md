# 遺伝カウンセリング教育システム

ローカルLLMを使用した遺伝カウンセリング教育システムです。学生と教官が患者シミュレーションを通じてカウンセリングスキルを向上させることができます。

## 🎯 主な機能

### ✅ 実装済み機能
- **ローカルLLMによる患者シミュレーション** - Ollama + Llama2を使用した患者役AI
- **Hydra設定管理** - コードを書かずに設定変更可能
- **学生・教官向けWebUI** - 直感的なインターフェース
- **モデル切り替え機能** - 複数のLLMモデル間での性能比較
- **セッション管理** - 複数のカウンセリングセッションを管理
- **リアルタイムチャット** - WebSocketによるリアルタイム通信

### 🔧 技術スタック
- **バックエンド**: FastAPI + Python + Poetry
- **フロントエンド**: React + TypeScript + Vite + Tailwind CSS
- **設定管理**: Hydra + OmegaConf
- **LLM**: Ollama (ローカル実行)
- **UI コンポーネント**: shadcn/ui

## 🚀 クイックスタート

### 前提条件
- Python 3.12+
- Node.js 18+
- Poetry
- Ollama

### インストール
```bash
# 1. Ollamaのインストール
curl -fsSL https://ollama.ai/install.sh | sh

# 2. LLMモデルのダウンロード
ollama pull llama2

# 3. バックエンドのセットアップ
cd backend
poetry install

# 4. フロントエンドのセットアップ
cd frontend
npm install
```

### 起動
```bash
# ターミナル1: Ollama
ollama serve

# ターミナル2: バックエンド
cd backend
poetry run fastapi dev app/main.py

# ターミナル3: フロントエンド
cd frontend
npm run dev
```

ブラウザで http://localhost:5173 にアクセス

## 📁 プロジェクト構造

```
genetic-counseling-system/
├── backend/                 # FastAPI バックエンド
│   ├── app/
│   │   ├── main.py         # メインアプリケーション
│   │   ├── config.py       # Hydra設定管理
│   │   ├── models/         # LLMモデル実装
│   │   └── services/       # ビジネスロジック
│   └── pyproject.toml      # Python依存関係
├── frontend/               # React フロントエンド
│   ├── src/
│   │   ├── components/     # UIコンポーネント
│   │   └── App.tsx        # メインアプリ
│   └── package.json       # Node.js依存関係
├── configs/               # Hydra設定ファイル
│   ├── config.yaml        # メイン設定
│   ├── model/            # LLMモデル設定
│   ├── prompt/           # 患者シナリオ設定
│   └── ui/               # UI設定
└── docs/                 # ドキュメント
    └── SETUP.md          # 詳細セットアップガイド
```

## 🎓 使用方法

### 1. セッション作成
1. 「新しいセッション」ボタンをクリック
2. ユーザーID、患者シナリオ、LLMモデルを選択
3. 「セッション開始」をクリック

### 2. カウンセリング実習
- チャット画面でカウンセラーとして質問
- AIが設定された患者として応答
- 会話を通じてカウンセリングスキルを練習

### 3. 設定管理
- **設定タブ**: モデルパラメータの調整
- **患者シナリオタブ**: 患者設定の変更
- **UI設定タブ**: インターフェースのカスタマイズ

## ⚙️ 設定例

### 患者シナリオ設定
```yaml
prompt:
  name: "default_patient"
  description: "標準的な患者シミュレーション"
  system_prompt: |
    あなたは遺伝カウンセリングを受ける患者です。
    【基本設定】
    - 年齢: 32歳
    - 性別: 女性
    - 職業: 会社員
    【相談内容】
    - 第二子を希望しているが、遺伝的リスクについて心配
```

### LLMモデル設定
```yaml
model:
  name: "llama2"
  type: "ollama"
  model_id: "llama2"
  temperature: 0.7
  max_tokens: 2048
```

## 🔍 API エンドポイント

- `GET /config` - 設定取得
- `POST /config/update` - 設定更新
- `POST /sessions` - セッション作成
- `POST /chat` - チャット送信
- `GET /health` - ヘルスチェック

## 📚 詳細ドキュメント

詳細なセットアップ手順とトラブルシューティングについては [docs/SETUP.md](docs/SETUP.md) を参照してください。

## 🤝 開発者向け

### 開発環境
- バックエンド開発サーバー: http://localhost:8000
- フロントエンド開発サーバー: http://localhost:5173
- Ollama API: http://localhost:11434

### 設定ファイルの編集
Hydra設定ファイルを直接編集するか、UIの設定タブから変更可能です。変更は即座に反映されます。

## 📄 ライセンス

このプロジェクトは教育目的で開発されています。
