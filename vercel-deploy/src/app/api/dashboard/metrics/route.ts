import { NextRequest, NextResponse } from 'next/server'

async function getTwitterFollowers() {
  try {
    if (!process.env.TWITTER_BEARER_TOKEN) {
      console.error('TWITTER_BEARER_TOKEN not set')
      return 60
    }
    
    const response = await fetch('https://api.twitter.com/2/users/by/username/Treasure_Corp?user.fields=public_metrics', {
      headers: {
        'Authorization': `Bearer ${process.env.TWITTER_BEARER_TOKEN}`
      }
    })
    
    if (!response.ok) {
      console.error('Twitter API HTTP error:', response.status, await response.text())
      return 60
    }
    
    const data = await response.json()
    console.log('Twitter API response:', data)
    return data.data?.public_metrics?.followers_count || 60
  } catch (error) {
    console.error('Twitter API error:', error)
    return 60 // Fallback to current count
  }
}

async function getTelegramSubscribers() {
  try {
    if (!process.env.TELEGRAM_BOT_TOKEN || !process.env.TELEGRAM_CHANNEL_ID) {
      console.error('Telegram env vars not set:', {
        token: !!process.env.TELEGRAM_BOT_TOKEN,
        channelId: !!process.env.TELEGRAM_CHANNEL_ID
      })
      return 3
    }
    
    const response = await fetch(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/getChatMemberCount?chat_id=${process.env.TELEGRAM_CHANNEL_ID}`)
    
    if (!response.ok) {
      console.error('Telegram API HTTP error:', response.status, await response.text())
      return 3
    }
    
    const data = await response.json()
    console.log('Telegram API response:', data)
    return data.result || 3
  } catch (error) {
    console.error('Telegram API error:', error)
    return 3 // Fallback to current count
  }
}

export async function GET(request: NextRequest) {
  try {
    // Get real data directly from APIs
    const twitterFollowers = await getTwitterFollowers()
    const telegramSubscribers = await getTelegramSubscribers()
    
    const realTimeData = [
      { 
        platform: 'twitter', 
        followers: twitterFollowers, 
        daily_growth: 0, // Calculate from historical data
        target_progress: (twitterFollowers / 7000) * 100 
      },
      { 
        platform: 'telegram', 
        followers: telegramSubscribers, 
        daily_growth: 0, // Calculate from historical data
        target_progress: (telegramSubscribers / 3000) * 100 
      }
    ]
    
    return NextResponse.json(realTimeData)
  } catch (error) {
    console.error('API Error:', error)
    
    // Fallback to current known counts
    return NextResponse.json([
      { platform: 'twitter', followers: 60, daily_growth: 0, target_progress: (60/7000)*100 },
      { platform: 'telegram', followers: 3, daily_growth: 0, target_progress: (3/3000)*100 }
    ])
  }
}