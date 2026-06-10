import { View, Text } from '@tarojs/components'
import { Button } from '@nutui/nutui-react-taro'
import Taro from '@tarojs/taro'
import { useAuth } from '../../store/auth'
import './profile.scss'

export default function Profile() {
  const { isLoggedIn, userId, loginWithWechat, logout } = useAuth()

  const handleLogin = async () => {
    try {
      await loginWithWechat()
      Taro.showToast({ title: '登录成功', icon: 'success' })
    } catch {
      Taro.showToast({ title: '登录失败', icon: 'none' })
    }
  }

  return (
    <View className="profile">
      {isLoggedIn ? (
        <>
          <Text className="info">user_id: {userId}</Text>
          <Button type="default" onClick={logout}>退出登录</Button>
        </>
      ) : (
        <Button type="primary" onClick={handleLogin}>微信登录</Button>
      )}
    </View>
  )
}
