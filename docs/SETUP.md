# 遺伝カウンセリング教育システム セットアップガイド

## 概要
このシステムは、ローカルLLMを使用した遺伝カウンセリング教育システムです。学生と教官が患者シミュレーションを通じてカウンセリングスキルを向上させることができます。

## 必要な環境
- Python 3.12+
- Node.js 18+
- Poetry (Python依存関係管理)
- npm (Node.js依存関係管理)
- Ollama (ローカルLLM実行環境)

## OS別インストール手順

### 🪟 Windows環境

#### 1. 前提ソフトウェアのインストール

**Python 3.12のインストール**
```powershell
# Microsoft Store経由、またはpython.orgからダウンロード
winget install Python.Python.3.12
```

**Node.js 18+のインストール**
```powershell
# 公式サイトからLTSバージョンをダウンロード
winget install OpenJS.NodeJS
```

**Poetryのインストール**
```powershell
# PowerShellで実行
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

**Gitのインストール（必要に応じて）**
```powershell
winget install Git.Git
```

#### 2. Ollamaのインストール
```powershell
# 公式サイトからWindows版をダウンロード
# https://ollama.ai/download/windows
# インストーラーを実行後、PowerShellで確認
ollama --version
```

#### 3. LLMモデルのダウンロード
```powershell
ollama pull llama2
```

#### 4. プロジェクトのセットアップ
```powershell
# プロジェクトディレクトリに移動
cd genetic-counseling-system

# バックエンドのセットアップ
cd backend
poetry install
cd ..

# フロントエンドのセットアップ
cd frontend
npm install
cd ..
```

### 🍎 Mac環境

#### 1. 前提ソフトウェアのインストール

**Homebrewのインストール（推奨）**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Python 3.12のインストール**
```bash
# Homebrewを使用
brew install python@3.12

# または公式サイトからダウンロード
# https://www.python.org/downloads/macos/
```

**Node.js 18+のインストール**
```bash
# Homebrewを使用
brew install node

# またはnvmを使用（推奨）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

**Poetryのインストール**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### 2. Ollamaのインストール
```bash
# Homebrewを使用
brew install ollama

# または公式サイトからダウンロード
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 3. LLMモデルのダウンロード
```bash
ollama pull llama2
```

#### 4. プロジェクトのセットアップ
```bash
# プロジェクトディレクトリに移動
cd genetic-counseling-system

# バックエンドのセットアップ
cd backend
poetry install
cd ..

# フロントエンドのセットアップ
cd frontend
npm install
cd ..
```

## 起動方法

### 🪟 Windows環境での起動

**ターミナル1: Ollamaサービスの開始**
```powershell
# PowerShellまたはコマンドプロンプトで実行
ollama serve
```

**ターミナル2: バックエンドの起動**
```powershell
cd backend
poetry run fastapi dev app/main.py
```

**ターミナル3: フロントエンドの起動**
```powershell
cd frontend
npm run dev
```

### 🍎 Mac環境での起動

**ターミナル1: Ollamaサービスの開始**
```bash
ollama serve
```

**ターミナル2: バックエンドの起動**
```bash
cd backend
poetry run fastapi dev app/main.py
```

**ターミナル3: フロントエンドの起動**
```bash
cd frontend
npm run dev
```

### 4. アクセス
ブラウザで http://localhost:5173 にアクセス

## OS別の注意事項

### 🪟 Windows固有の注意点

1. **PowerShell実行ポリシー**
   ```powershell
   # 必要に応じて実行ポリシーを変更
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **パス区切り文字**
   - Windowsでは `\` を使用
   - コマンドでは `/` も使用可能

3. **ポート使用確認**
   ```powershell
   # ポートが使用中かチェック
   netstat -ano | findstr :8000
   netstat -ano | findstr :5173
   netstat -ano | findstr :11434
   ```

4. **ファイアウォール設定**
   - 初回起動時にWindowsファイアウォールの許可が必要な場合があります

### 🍎 Mac固有の注意点

1. **Xcode Command Line Tools**
   ```bash
   # 必要に応じてインストール
   xcode-select --install
   ```

2. **権限設定**
   ```bash
   # 必要に応じてファイル権限を設定
   chmod +x ollama
   ```

3. **ポート使用確認**
   ```bash
   # ポートが使用中かチェック
   lsof -i :8000
   lsof -i :5173
   lsof -i :11434
   ```

4. **Rosetta 2（Apple Siliconの場合）**
   - Intel用のソフトウェアを実行する場合に必要
   ```bash
   softwareupdate --install-rosetta
   ```

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

### 🪟 Windows環境のトラブルシューティング

**Ollamaが起動しない**
```powershell
# サービスの状態確認
Get-Service ollama

# 手動でサービス開始
Start-Service ollama

# または直接実行
ollama serve
```

**Poetryが認識されない**
```powershell
# パスの確認と追加
$env:PATH += ";$env:APPDATA\Python\Scripts"

# または再インストール
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

**ポートが使用中**
```powershell
# プロセス確認と終了
netstat -ano | findstr :8000
taskkill /PID <プロセスID> /F
```

**Node.jsのバージョン問題**
```powershell
# バージョン確認
node --version
npm --version

# 再インストール
winget uninstall OpenJS.NodeJS
winget install OpenJS.NodeJS
```

### 🍎 Mac環境のトラブルシューティング

**Ollamaが起動しない**
```bash
# Homebrewでインストールした場合
brew services start ollama

# 手動起動
ollama serve

# 権限問題の場合
sudo ollama serve
```

**Poetryが認識されない**
```bash
# パスの確認
echo $PATH

# .zshrcまたは.bash_profileに追加
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**ポートが使用中**
```bash
# プロセス確認と終了
lsof -i :8000
kill -9 <プロセスID>
```

**Python/Node.jsのバージョン問題**
```bash
# pyenvを使用してPythonバージョン管理
brew install pyenv
pyenv install 3.12.0
pyenv global 3.12.0

# nvmを使用してNode.jsバージョン管理
nvm install 18
nvm use 18
```

**Apple Silicon（M1/M2）での問題**
```bash
# Rosetta 2のインストール
softwareupdate --install-rosetta

# Intel版Homebrewの使用（必要に応じて）
arch -x86_64 brew install <package>
```

### 共通のトラブルシューティング

**モデルが見つからない**
```bash
# 利用可能なモデル確認
ollama list

# モデルの再ダウンロード
ollama pull llama2

# モデルの削除と再インストール
ollama rm llama2
ollama pull llama2
```

**設定ファイルの問題**
```bash
# 設定ファイルの確認
cat configs/config.yaml

# デフォルト設定での起動テスト
python backend/debug_config.py
```

**依存関係の問題**
```bash
# バックエンド依存関係の再インストール
cd backend
poetry install --no-cache

# フロントエンド依存関係の再インストール
cd frontend
rm -rf node_modules package-lock.json
npm install
```

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
