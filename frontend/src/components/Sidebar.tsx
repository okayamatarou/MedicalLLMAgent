import { useState } from 'react'
import { Plus, User, Clock, Settings } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

interface SidebarProps {
  config: any
  currentSession: string | null
  onSessionSelect: (sessionId: string) => void
  onCreateSession: (userId: string, promptConfig: string, modelConfig: string) => Promise<string | null>
}

export function Sidebar({ config, currentSession, onCreateSession }: SidebarProps) {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [newSessionData, setNewSessionData] = useState({
    userId: '',
    promptConfig: 'default_patient',
    modelConfig: 'llama2'
  })

  const handleCreateSession = async () => {
    if (!newSessionData.userId.trim()) return

    const sessionId = await onCreateSession(
      newSessionData.userId,
      newSessionData.promptConfig,
      newSessionData.modelConfig
    )

    if (sessionId) {
      setIsCreateDialogOpen(false)
      setNewSessionData({
        userId: '',
        promptConfig: 'default_patient',
        modelConfig: 'llama2'
      })
    }
  }

  return (
    <aside className="w-80 bg-white border-r border-gray-200 p-4">
      <div className="space-y-4">
        {/* Create Session Button */}
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button className="w-full flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>新しいセッション</span>
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>新しいカウンセリングセッション</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="userId">ユーザーID</Label>
                <Input
                  id="userId"
                  value={newSessionData.userId}
                  onChange={(e) => setNewSessionData(prev => ({ ...prev, userId: e.target.value }))}
                  placeholder="学生ID または 教官ID"
                />
              </div>
              
              <div>
                <Label htmlFor="promptConfig">患者シナリオ</Label>
                <Select
                  value={newSessionData.promptConfig}
                  onValueChange={(value) => setNewSessionData(prev => ({ ...prev, promptConfig: value }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {config?.available_prompts?.map((prompt: string) => (
                      <SelectItem key={prompt} value={prompt}>
                        {prompt === 'default_patient' ? '標準患者' : 
                         prompt === 'anxious_patient' ? '不安の強い患者' : prompt}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label htmlFor="modelConfig">LLMモデル</Label>
                <Select
                  value={newSessionData.modelConfig}
                  onValueChange={(value) => setNewSessionData(prev => ({ ...prev, modelConfig: value }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {config?.available_models?.map((model: string) => (
                      <SelectItem key={model} value={model}>
                        {model}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <Button onClick={handleCreateSession} className="w-full">
                セッション開始
              </Button>
            </div>
          </DialogContent>
        </Dialog>

        {/* Current Session Info */}
        {currentSession && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm flex items-center space-x-2">
                <User className="h-4 w-4" />
                <span>現在のセッション</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-gray-600 font-mono">
                {currentSession}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Quick Settings */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center space-x-2">
              <Settings className="h-4 w-4" />
              <span>クイック設定</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="text-xs">
              <p className="text-gray-600">現在のモデル:</p>
              <p className="font-medium">{config?.config?.model?.name || 'Unknown'}</p>
            </div>
            <div className="text-xs">
              <p className="text-gray-600">現在のシナリオ:</p>
              <p className="font-medium">{config?.config?.prompt?.name || 'Unknown'}</p>
            </div>
          </CardContent>
        </Card>

        {/* System Status */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center space-x-2">
              <Clock className="h-4 w-4" />
              <span>システム状態</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <div className="h-2 w-2 bg-green-500 rounded-full"></div>
              <span className="text-xs text-gray-600">オンライン</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </aside>
  )
}
