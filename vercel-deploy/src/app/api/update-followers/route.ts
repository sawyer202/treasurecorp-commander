import { NextRequest, NextResponse } from 'next/server'

// Simple storage (in production, use a database)
let followerData = {
  twitter: 60,
  telegram: 3,
  lastUpdated: new Date().toISOString()
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    if (body.twitter !== undefined) {
      followerData.twitter = body.twitter
    }
    if (body.telegram !== undefined) {
      followerData.telegram = body.telegram
    }
    
    followerData.lastUpdated = new Date().toISOString()
    
    return NextResponse.json({ 
      success: true, 
      data: followerData 
    })
  } catch (error) {
    return NextResponse.json({ error: 'Invalid data' }, { status: 400 })
  }
}

export async function GET() {
  return NextResponse.json(followerData)
}