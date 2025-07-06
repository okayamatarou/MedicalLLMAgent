# Windows環境セットアップガイド

## 🪟 Windows専用インストールガイド

### 前提条件
- Windows 10/11 (64bit)
- 管理者権限でのインストールが可能
- インターネット接続

### 1. 必要なソフトウェアのインストール

#### Python 3.12のインストール
```powershell
# 方法1: Microsoft Store経由（推奨）
# Microsoft Storeで "Python 3.12" を検索してインストール

# 方法2: wingetを使用
winget install Python.Python.3.12

# 方法3: 公式サイトからダウンロード
# https://www.python.org/downloads/windows/
```

#### Node.js 18+のインストール
```powershell
# 方法1: wingetを使用（推奨）
winget install OpenJS.NodeJS

# 方法2: 公式サイトからダウンロード
# https://nodejs.org/ja/download/
```

#### Gitのインストール
```powershell
# wingetを使用
winget install Git.Git

# または公式サイトからダウンロード
# https://git-scm.com/download/win
```

#### Poetryのインストール
```powershell
# PowerShellで実行（管理者権限推奨）
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# パスの追加（必要に応じて）
$env:PATH += ";$env:APPDATA\Python\Scripts"
```

### 2. Ollamaのインストール

#### ダウンロードとインストール
1. https://ollama.ai/download/windows にアクセス
2. Windows版インストーラーをダウンロード
3. インストーラーを実行
4. インストール完了後、PowerShellで確認：

```powershell
ollama --version
```

#### Ollamaサービスの設定
```powershell
# サービスの状態確認
Get-Service ollama

# サービスの開始
Start-Service ollama

# 自動起動の設定
Set-Service -Name ollama -StartupType Automatic
```

### 3. プロジェクトのセットアップ

#### プロジェクトのダウンロード
```powershell
# GitHubからクローン（URLは実際のリポジトリに置き換え）
git clone <リポジトリURL> genetic-counseling-system
cd genetic-counseling-system
```

#### バックエンドのセットアップ
```powershell
cd backend

# 仮想環境の作成とパッケージインストール
poetry install

# 設定確認
poetry run python debug_config.py
```

#### フロントエンドのセットアップ
```powershell
cd ..\frontend

# パッケージのインストール
npm install

# 設定確認
npm run build
```

### 4. LLMモデルのダウンロード

```powershell
# Llama2モデルのダウンロード
ollama pull llama2

# ダウンロード確認
ollama list
```

### 5. システムの起動

#### 3つのPowerShellウィンドウを開いて以下を実行：

**ウィンドウ1: Ollamaサービス**
```powershell
cd genetic-counseling-system
ollama serve
```

**ウィンドウ2: バックエンド**
```powershell
cd genetic-counseling-system\backend
poetry run fastapi dev app/main.py
```

**ウィンドウ3: フロントエンド**
```powershell
cd genetic-counseling-system\frontend
npm run dev
```

### 6. アクセス確認

ブラウザで以下のURLにアクセス：
- フロントエンド: http://localhost:5173
- バックエンドAPI: http://localhost:8000
- Ollama API: http://localhost:11434

## Windows固有の注意事項

### PowerShell実行ポリシー
```powershell
# 現在のポリシー確認
Get-ExecutionPolicy

# 必要に応じて変更
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ファイアウォール設定
- 初回起動時にWindowsファイアウォールの許可ダイアログが表示される場合があります
- 「プライベートネットワーク」にチェックを入れて許可してください

### ウイルス対策ソフト
- 一部のウイルス対策ソフトがOllamaやPythonの実行を阻害する場合があります
- 必要に応じて除外設定を行ってください

### パフォーマンス最適化
```powershell
# システムリソースの確認
Get-ComputerInfo | Select-Object TotalPhysicalMemory, CsProcessors

# 推奨スペック：
# - RAM: 8GB以上（16GB推奨）
# - CPU: 4コア以上
# - ストレージ: 10GB以上の空き容量
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. "poetry: コマンドが見つかりません"
```powershell
# パスの確認
echo $env:PATH

# 手動でパス追加
$env:PATH += ";$env:APPDATA\Python\Scripts"

# 永続的なパス設定
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:APPDATA\Python\Scripts", [EnvironmentVariableTarget]::User)
```

#### 2. "ollama: コマンドが見つかりません"
```powershell
# Ollamaの再インストール
# 公式サイトから最新版をダウンロード

# サービスの確認
Get-Service ollama
```

#### 3. ポート競合エラー
```powershell
# 使用中のポート確認
netstat -ano | findstr :8000
netstat -ano | findstr :5173
netstat -ano | findstr :11434

# プロセス終了
taskkill /PID <プロセスID> /F
```

#### 4. Python/Node.jsバージョン問題
```powershell
# バージョン確認
python --version
node --version
npm --version

# 必要に応じて再インストール
```

### サポート情報
- 問題が解決しない場合は、エラーメッセージとシステム情報を記録してサポートに連絡してください
- ログファイルの場所：
  - Ollama: `%USERPROFILE%\.ollama\logs\`
  - アプリケーション: `backend/logs/` (作成される場合)
