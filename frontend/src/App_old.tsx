import { useState, useEffect } from 'react'
import { Toaster } from '@/components/ui/toaster'
import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { ChatInterface } from '@/components/ChatInterface'
import { ConfigPanel } from '@/components/ConfigPanel'
import { SessionManager } from '@/components/SessionManager'
import { useToast } from '@/hooks/use-toast'

interface Config {
  config: any
  available_models: string[]
  available_prompts: string[]
  available_ui_configs: string[]
}

function App() {
  const [config, setConfig] = useState<Config | null>(null)
  const [currentSession, setCurrentSession] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'chat' | 'config' | 'sessions'>('chat')
  const [loading, setLoading] = useState(true)
  const { toast } = useToast()

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    loadConfig()
  }, [])

  const loadConfig = async () => {
    try {
      console.log('Loading config from:', `${API_URL}/config`)
      const response = await fetch(`${API_URL}/config`)
      console.log('Config response status:', response.status)
      if (response.ok) {
        const configData = await response.json()
        console.log('Config data received:', configData)
        setConfig(configData)
      } else {
        console.error('Config response not ok:', response.status, response.statusText)
        toast({
          title: "設定の読み込みエラー",
          description: "設定を読み込めませんでした。",
          variant: "destructive"
        })
      }
    } catch (error) {
      console.error('Config load error:', error)
      toast({
        title: "接続エラー",
        description: "サーバーに接続できません。",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const updateConfig = async (overrides: Record<string, any>) => {
    try {
      const response = await fetch(`${API_URL}/config/update`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ overrides }),
      })

      if (response.ok) {
        await loadConfig()
        toast({
          title: "設定更新完了",
          description: "設定が正常に更新されました。",
        })
      } else {
        toast({
          title: "設定更新エラー",
          description: "設定の更新に失敗しました。",
          variant: "destructive"
        })
      }
    } catch (error) {
      console.error('Config update error:', error)
      toast({
        title: "更新エラー",
        description: "設定の更新中にエラーが発生しました。",
        variant: "destructive"
      })
    }
  }

  const createSession = async (userId: string, promptConfig: string, modelConfig: string) => {
    try {
      const response = await fetch(`${API_URL}/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          prompt_config: promptConfig,
          model_name: modelConfig,
        }),
      })

      if (response.ok) {
        const result = await response.json()
        setCurrentSession(result.session_id)
        setActiveTab('chat')
        toast({
          title: "セッション開始",
          description: "新しいカウンセリングセッションを開始しました。",
        })
        return result.session_id
      } else {
        toast({
          title: "セッション作成エラー",
          description: "セッションの作成に失敗しました。",
          variant: "destructive"
        })
      }
    } catch (error) {
      console.error('Session creation error:', error)
      toast({
        title: "セッション作成エラー",
        description: "セッションの作成中にエラーが発生しました。",
        variant: "destructive"
      })
    }
    return null
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">システムを読み込み中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        config={config}
        onConfigUpdate={updateConfig}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
      
      <div className="flex">
        <Sidebar 
          config={config}
          currentSession={currentSession}
          onSessionSelect={setCurrentSession}
          onCreateSession={createSession}
        />
        
        <main className="flex-1 p-6">
          {activeTab === 'chat' && (
            <ChatInterface 
              sessionId={currentSession}
              apiUrl={API_URL}
            />
          )}
          
          {activeTab === 'config' && (
            <ConfigPanel 
              config={config}
              onConfigUpdate={updateConfig}
              onReload={loadConfig}
            />
          )}
          
          {activeTab === 'sessions' && (
            <SessionManager 
              apiUrl={API_URL}
              onSessionSelect={setCurrentSession}
              onCreateSession={createSession}
            />
          )}
        </main>
      </div>
      
      <Toaster />
    </div>
  )
}

export default App
