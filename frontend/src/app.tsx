import { PropsWithChildren } from 'react'
import { useLaunch } from '@tarojs/taro'
import { AuthProvider, useAuth } from './store/auth'
import './app.scss'

function LaunchRestore({ children }: PropsWithChildren) {
  const { restore } = useAuth()
  useLaunch(() => {
    restore()
  })
  return <>{children}</>
}

function App({ children }: PropsWithChildren) {
  return (
    <AuthProvider>
      <LaunchRestore>{children}</LaunchRestore>
    </AuthProvider>
  )
}

export default App
