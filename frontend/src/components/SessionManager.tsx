import { useState, useEffect } from 'react'
import { User, Eye } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { useToast } from '@/hooks/use-toast'

interface Session {
  session_id: string
  user_id: string
  prompt_config: string
  model_config: string
  created_at: string
  status: string
  messages: any[]
}

interface SessionManagerProps {
  apiUrl: string
  onSessionSelect: (sessionId: string) => void
  onCreateSession: (userId: string, promptConfig: string, modelConfig: string) => Promise<string | null>
}

export function SessionManager({ apiUrl, onSessionSelect }: SessionManagerProps) {
  const [sessions, setSessions] = useState<Session[]>([])
  const [searchUserId, setSearchUserId] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedSession, setSelectedSession] = useState<Session | null>(null)
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    if (searchUserId.trim()) {
      loadUserSessions(searchUserId)
    }
  }, [searchUserId])

  const loadUserSessions = async (userId: string) => {
    setIsLoading(true)
    try {
      const response = await fetch(`${apiUrl}/users/${userId}/sessions`)
      if (response.ok) {
        const data = await response.json()
        setSessions(data.sessions)
      } else {
        setSessions([])
        if (response.status !== 404) {
          toast({
            title: "セッション読み込みエラー",
            description: "セッションの読み込みに失敗しました。",
            variant: "destructive"
          })
        }
      }
    } catch (error) {
      console.error('Failed to load sessions:', error)
      setSessions([])
      toast({
        title: "通信エラー",
        description: "サーバーとの通信に失敗しました。",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleSessionSelect = (session: Session) => {
    onSessionSelect(session.session_id)
    toast({
      title: "セッション選択",
      description: `セッション ${session.session_id.substring(0, 8)}... を選択しました。`,
    })
  }

  const handleViewDetails = (session: Session) => {
    setSelectedSession(session)
    setIsDetailDialogOpen(true)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('ja-JP')
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'active':
        return <Badge className="bg-green-100 text-green-800">アクティブ</Badge>
      case 'completed':
        return <Badge className="bg-blue-100 text-blue-800">完了</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">セッション管理</h2>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>セッション検索</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-4">
            <div className="flex-1">
              <Label htmlFor="search-user">ユーザーIDで検索</Label>
              <Input
                id="search-user"
                value={searchUserId}
                onChange={(e) => setSearchUserId(e.target.value)}
                placeholder="学生ID または 教官ID を入力"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {isLoading && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">セッションを読み込み中...</p>
        </div>
      )}

      {!isLoading && searchUserId && sessions.length === 0 && (
        <div className="text-center py-8">
          <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            セッションが見つかりません
          </h3>
          <p className="text-gray-600">
            ユーザーID「{searchUserId}」のセッションは存在しません。
          </p>
        </div>
      )}

      {sessions.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900">
            {searchUserId} のセッション ({sessions.length}件)
          </h3>
          
          <div className="grid gap-4">
            {sessions.map((session) => (
              <Card key={session.session_id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h4 className="font-medium text-gray-900">
                          セッション {session.session_id.substring(0, 8)}...
                        </h4>
                        {getStatusBadge(session.status)}
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                        <div>
                          <p><strong>シナリオ:</strong> {session.prompt_config}</p>
                          <p><strong>モデル:</strong> {session.model_config}</p>
                        </div>
                        <div>
                          <p><strong>作成日時:</strong> {formatDate(session.created_at)}</p>
                          <p><strong>メッセージ数:</strong> {session.messages?.length || 0}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleViewDetails(session)}
                      >
                        <Eye className="h-4 w-4 mr-1" />
                        詳細
                      </Button>
                      <Button
                        variant="default"
                        size="sm"
                        onClick={() => handleSessionSelect(session)}
                      >
                        選択
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      <Dialog open={isDetailDialogOpen} onOpenChange={setIsDetailDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>セッション詳細</DialogTitle>
          </DialogHeader>
          
          {selectedSession && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>セッションID</Label>
                  <p className="font-mono text-sm bg-gray-100 p-2 rounded">
                    {selectedSession.session_id}
                  </p>
                </div>
                <div>
                  <Label>ユーザーID</Label>
                  <p className="font-medium">{selectedSession.user_id}</p>
                </div>
                <div>
                  <Label>患者シナリオ</Label>
                  <p className="font-medium">{selectedSession.prompt_config}</p>
                </div>
                <div>
                  <Label>LLMモデル</Label>
                  <p className="font-medium">{selectedSession.model_config}</p>
                </div>
                <div>
                  <Label>ステータス</Label>
                  {getStatusBadge(selectedSession.status)}
                </div>
                <div>
                  <Label>作成日時</Label>
                  <p className="font-medium">{formatDate(selectedSession.created_at)}</p>
                </div>
              </div>

              <div>
                <Label>会話履歴 ({selectedSession.messages?.length || 0}件)</Label>
                <div className="bg-gray-50 p-3 rounded-md max-h-60 overflow-y-auto">
                  {selectedSession.messages?.length > 0 ? (
                    <div className="space-y-2">
                      {selectedSession.messages
                        .filter(msg => msg.role !== 'system')
                        .slice(-10)
                        .map((msg, index) => (
                        <div key={index} className="text-sm">
                          <span className={`font-medium ${
                            msg.role === 'user' ? 'text-blue-600' : 'text-green-600'
                          }`}>
                            {msg.role === 'user' ? 'カウンセラー' : '患者'}:
                          </span>
                          <p className="mt-1 text-gray-700">
                            {msg.content.length > 100 
                              ? msg.content.substring(0, 100) + '...' 
                              : msg.content}
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">メッセージがありません</p>
                  )}
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}
