# Mac環境セットアップガイド

## 🍎 Mac専用インストールガイド

### 前提条件
- macOS 12.0 (Monterey) 以降
- 管理者権限でのインストールが可能
- インターネット接続

### 1. 必要なソフトウェアのインストール

#### Homebrewのインストール（推奨）
```bash
# Homebrewのインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# パスの設定（Apple Siliconの場合）
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

# パスの設定（Intelの場合）
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

#### Xcode Command Line Toolsのインストール
```bash
xcode-select --install
```

#### Python 3.12のインストール
```bash
# 方法1: Homebrewを使用（推奨）
brew install python@3.12

# 方法2: pyenvを使用（複数バージョン管理）
brew install pyenv
pyenv install 3.12.0
pyenv global 3.12.0

# 方法3: 公式サイトからダウンロード
# https://www.python.org/downloads/macos/
```

#### Node.js 18+のインストール
```bash
# 方法1: Homebrewを使用
brew install node

# 方法2: nvmを使用（推奨・複数バージョン管理）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.zshrc
nvm install 18
nvm use 18
nvm alias default 18
```

#### Gitのインストール
```bash
# Homebrewを使用
brew install git

# または、Xcodeに含まれているものを使用
git --version
```

#### Poetryのインストール
```bash
# 公式インストーラーを使用
curl -sSL https://install.python-poetry.org | python3 -

# パスの設定
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Ollamaのインストール

#### 方法1: Homebrewを使用（推奨）
```bash
brew install ollama
```

#### 方法2: 公式インストーラーを使用
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 方法3: 手動ダウンロード
1. https://ollama.ai/download/mac にアクセス
2. Mac版をダウンロード
3. アプリケーションフォルダにドラッグ&ドロップ

#### Ollamaサービスの設定
```bash
# サービスの開始（Homebrewの場合）
brew services start ollama

# 手動起動
ollama serve

# バックグラウンドで実行
nohup ollama serve > /dev/null 2>&1 &
```

### 3. プロジェクトのセットアップ

#### プロジェクトのダウンロード
```bash
# GitHubからクローン（URLは実際のリポジトリに置き換え）
git clone <リポジトリURL> genetic-counseling-system
cd genetic-counseling-system
```

#### バックエンドのセットアップ
```bash
cd backend

# 仮想環境の作成とパッケージインストール
poetry install

# 設定確認
poetry run python debug_config.py
```

#### フロントエンドのセットアップ
```bash
cd ../frontend

# パッケージのインストール
npm install

# 設定確認
npm run build
```

### 4. LLMモデルのダウンロード

```bash
# Llama2モデルのダウンロード
ollama pull llama2

# ダウンロード確認
ollama list
```

### 5. システムの起動

#### 3つのターミナルウィンドウを開いて以下を実行：

**ターミナル1: Ollamaサービス**
```bash
cd genetic-counseling-system
ollama serve
```

**ターミナル2: バックエンド**
```bash
cd genetic-counseling-system/backend
poetry run fastapi dev app/main.py
```

**ターミナル3: フロントエンド**
```bash
cd genetic-counseling-system/frontend
npm run dev
```

### 6. アクセス確認

ブラウザで以下のURLにアクセス：
- フロントエンド: http://localhost:5173
- バックエンドAPI: http://localhost:8000
- Ollama API: http://localhost:11434

## Mac固有の注意事項

### Apple Silicon（M1/M2/M3）での注意点

#### Rosetta 2のインストール
```bash
# Intel用アプリケーション実行のため
softwareupdate --install-rosetta
```

#### アーキテクチャの確認
```bash
# CPUアーキテクチャの確認
uname -m
# arm64: Apple Silicon
# x86_64: Intel

# Homebrewのアーキテクチャ確認
brew config | grep "CPU"
```

#### Intel版Homebrewの使用（必要に応じて）
```bash
# Intel版Homebrewでパッケージインストール
arch -x86_64 brew install <package>
```

### セキュリティとプライバシー設定

#### Gatekeeperの設定
```bash
# 開発者として署名されていないアプリの実行許可
sudo spctl --master-disable

# 特定のアプリの許可
sudo xattr -rd com.apple.quarantine /path/to/app
```

#### ファイアウォール設定
```bash
# ファイアウォールの状態確認
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# 必要に応じてポートの許可設定
```

### パフォーマンス最適化

#### システムリソースの確認
```bash
# メモリ使用量
top -l 1 | grep "PhysMem"

# CPU情報
sysctl -n machdep.cpu.brand_string

# ディスク容量
df -h
```

#### 推奨スペック
- RAM: 8GB以上（16GB推奨、Apple Siliconの場合は8GBでも十分）
- ストレージ: 10GB以上の空き容量
- macOS: 12.0 (Monterey) 以降

## トラブルシューティング

### よくある問題と解決方法

#### 1. "poetry: command not found"
```bash
# パスの確認
echo $PATH

# .zshrcに追加
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 再インストール
curl -sSL https://install.python-poetry.org | python3 -
```

#### 2. "ollama: command not found"
```bash
# Homebrewでの再インストール
brew uninstall ollama
brew install ollama

# パスの確認
which ollama
```

#### 3. ポート競合エラー
```bash
# 使用中のポート確認
lsof -i :8000
lsof -i :5173
lsof -i :11434

# プロセス終了
kill -9 <PID>
```

#### 4. Python/Node.jsバージョン問題
```bash
# バージョン確認
python3 --version
node --version
npm --version

# pyenv/nvmでのバージョン管理
pyenv versions
nvm list
```

#### 5. 権限エラー
```bash
# ファイル権限の修正
chmod +x ollama
chmod -R 755 genetic-counseling-system

# 所有者の変更
sudo chown -R $(whoami) genetic-counseling-system
```

#### 6. Apple Silicon特有の問題
```bash
# Intel版での実行
arch -x86_64 <command>

# Rosetta 2の確認
pgrep oahd
```

### ログとデバッグ

#### ログファイルの場所
```bash
# Ollamaログ
~/Library/Logs/ollama/

# システムログ
tail -f /var/log/system.log

# アプリケーションログ
tail -f backend/logs/app.log
```

#### デバッグモードでの実行
```bash
# 詳細ログ出力
export DEBUG=1
poetry run fastapi dev app/main.py

# Ollamaのデバッグ
OLLAMA_DEBUG=1 ollama serve
```

### サポート情報
- 問題が解決しない場合は、以下の情報を記録してサポートに連絡してください：
  - macOSバージョン: `sw_vers`
  - CPUアーキテクチャ: `uname -m`
  - エラーメッセージ
  - 実行したコマンドの履歴
