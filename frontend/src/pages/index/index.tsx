import { View, Text } from '@tarojs/components'
import { useAuth } from '../../store/auth'
import './index.scss'

export default function Index() {
  const { isLoggedIn, userId } = useAuth()
  return (
    <View className="index">
      <Text className="title">AI 健康生活助手</Text>
      <Text className="status">
        {isLoggedIn ? `已登录（user_id: ${userId}）` : '未登录'}
      </Text>
    </View>
  )
}
