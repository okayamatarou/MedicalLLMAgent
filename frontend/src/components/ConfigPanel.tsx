import { useState } from 'react'
import { RefreshCw, Settings, Database, Palette } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Switch } from '@/components/ui/switch'
import { useToast } from '@/hooks/use-toast'

interface ConfigPanelProps {
  config: any
  onConfigUpdate: (overrides: Record<string, any>) => void
  onReload: () => void
}

export function ConfigPanel({ config, onConfigUpdate, onReload }: ConfigPanelProps) {
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleModelChange = async (modelName: string) => {
    setIsLoading(true)
    try {
      await onConfigUpdate({ model: modelName })
      toast({
        title: "モデル変更完了",
        description: `${modelName}に切り替えました。`,
      })
    } catch (error) {
      toast({
        title: "モデル変更エラー",
        description: "モデルの変更に失敗しました。",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handlePromptChange = async (promptName: string) => {
    setIsLoading(true)
    try {
      await onConfigUpdate({ prompt: promptName })
      toast({
        title: "シナリオ変更完了",
        description: `${promptName}に切り替えました。`,
      })
    } catch (error) {
      toast({
        title: "シナリオ変更エラー",
        description: "シナリオの変更に失敗しました。",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleUIConfigChange = async (uiName: string) => {
    setIsLoading(true)
    try {
      await onConfigUpdate({ ui: uiName })
      toast({
        title: "UI設定変更完了",
        description: `${uiName}に切り替えました。`,
      })
    } catch (error) {
      toast({
        title: "UI設定変更エラー",
        description: "UI設定の変更に失敗しました。",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  const currentModel = config?.config?.model || {}
  const currentPrompt = config?.config?.prompt || {}
  const currentUI = config?.config?.ui || {}

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">システム設定</h2>
        <Button onClick={onReload} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          設定を再読み込み
        </Button>
      </div>

      <Tabs defaultValue="models" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="models" className="flex items-center space-x-2">
            <Database className="h-4 w-4" />
            <span>LLMモデル</span>
          </TabsTrigger>
          <TabsTrigger value="prompts" className="flex items-center space-x-2">
            <Settings className="h-4 w-4" />
            <span>患者シナリオ</span>
          </TabsTrigger>
          <TabsTrigger value="ui" className="flex items-center space-x-2">
            <Palette className="h-4 w-4" />
            <span>UI設定</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="models" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>LLMモデル設定</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="model-select">使用するモデル</Label>
                <Select
                  value={currentModel.name || ''}
                  onValueChange={handleModelChange}
                  disabled={isLoading}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="モデルを選択" />
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

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="temperature">Temperature</Label>
                  <Input
                    id="temperature"
                    type="number"
                    step="0.1"
                    min="0"
                    max="2"
                    value={currentModel.temperature || 0.7}
                    readOnly
                  />
                </div>
                <div>
                  <Label htmlFor="max-tokens">Max Tokens</Label>
                  <Input
                    id="max-tokens"
                    type="number"
                    value={currentModel.max_tokens || 2048}
                    readOnly
                  />
                </div>
              </div>

              <div>
                <Label>モデル情報</Label>
                <div className="bg-gray-50 p-3 rounded-md text-sm">
                  <p><strong>タイプ:</strong> {currentModel.type || 'Unknown'}</p>
                  <p><strong>モデルID:</strong> {currentModel.model_id || 'Unknown'}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="prompts" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>患者シナリオ設定</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="prompt-select">シナリオを選択</Label>
                <Select
                  value={currentPrompt.name || ''}
                  onValueChange={handlePromptChange}
                  disabled={isLoading}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="シナリオを選択" />
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
                <Label>シナリオ説明</Label>
                <Textarea
                  value={currentPrompt.description || ''}
                  readOnly
                  className="min-h-[100px]"
                />
              </div>

              <div>
                <Label>システムプロンプト（プレビュー）</Label>
                <Textarea
                  value={currentPrompt.system_prompt?.substring(0, 500) + '...' || ''}
                  readOnly
                  className="min-h-[150px] text-xs"
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ui" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>UI設定</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="ui-select">UI設定を選択</Label>
                <Select
                  value={currentUI.name || ''}
                  onValueChange={handleUIConfigChange}
                  disabled={isLoading}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="UI設定を選択" />
                  </SelectTrigger>
                  <SelectContent>
                    {config?.available_ui_configs?.map((ui: string) => (
                      <SelectItem key={ui} value={ui}>
                        {ui === 'standard' ? '標準UI' : 
                         ui === 'instructor' ? '教官向けUI' : ui}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-3">
                <Label>機能設定</Label>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">自動保存</span>
                    <Switch checked={currentUI.features?.auto_save || false} disabled />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">会話エクスポート</span>
                    <Switch checked={currentUI.features?.export_conversation || false} disabled />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">リアルタイム評価</span>
                    <Switch checked={currentUI.features?.real_time_evaluation || false} disabled />
                  </div>
                  {currentUI.features?.session_recording !== undefined && (
                    <div className="flex items-center justify-between">
                      <span className="text-sm">セッション録画</span>
                      <Switch checked={currentUI.features?.session_recording || false} disabled />
                    </div>
                  )}
                </div>
              </div>

              <div>
                <Label>テーマ設定</Label>
                <div className="bg-gray-50 p-3 rounded-md text-sm space-y-1">
                  <p><strong>プライマリカラー:</strong> {currentUI.theme?.primary_color || '#2563eb'}</p>
                  <p><strong>セカンダリカラー:</strong> {currentUI.theme?.secondary_color || '#64748b'}</p>
                  <p><strong>背景色:</strong> {currentUI.theme?.background_color || '#f8fafc'}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
