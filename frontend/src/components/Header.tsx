import { Settings, MessageSquare, Users } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

interface HeaderProps {
  config: any
  onConfigUpdate: (overrides: Record<string, any>) => void
  activeTab: 'chat' | 'config' | 'sessions'
  onTabChange: (tab: 'chat' | 'config' | 'sessions') => void
}

export function Header({ config, activeTab, onTabChange }: HeaderProps) {
  const currentModel = config?.config?.model?.name || 'Unknown'
  const currentPrompt = config?.config?.prompt?.name || 'Unknown'

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold text-gray-900">
            遺伝カウンセリング教育システム
          </h1>
          <div className="flex space-x-2">
            <Badge variant="outline" className="text-sm">
              モデル: {currentModel}
            </Badge>
            <Badge variant="outline" className="text-sm">
              シナリオ: {currentPrompt}
            </Badge>
          </div>
        </div>

        <nav className="flex space-x-2">
          <Button
            variant={activeTab === 'chat' ? 'default' : 'ghost'}
            onClick={() => onTabChange('chat')}
            className="flex items-center space-x-2"
          >
            <MessageSquare className="h-4 w-4" />
            <span>チャット</span>
          </Button>
          
          <Button
            variant={activeTab === 'sessions' ? 'default' : 'ghost'}
            onClick={() => onTabChange('sessions')}
            className="flex items-center space-x-2"
          >
            <Users className="h-4 w-4" />
            <span>セッション管理</span>
          </Button>
          
          <Button
            variant={activeTab === 'config' ? 'default' : 'ghost'}
            onClick={() => onTabChange('config')}
            className="flex items-center space-x-2"
          >
            <Settings className="h-4 w-4" />
            <span>設定</span>
          </Button>
        </nav>
      </div>
    </header>
  )
}
