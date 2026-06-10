export default defineAppConfig({
  pages: [
    'pages/index/index',
    'pages/profile/profile',
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#fff',
    navigationBarTitleText: 'AI 健康生活助手',
    navigationBarTextStyle: 'black',
  },
  tabBar: {
    color: '#999',
    selectedColor: '#1989fa',
    backgroundColor: '#fff',
    list: [
      { pagePath: 'pages/index/index', text: '首页' },
      { pagePath: 'pages/profile/profile', text: '我的' },
    ],
  },
})
