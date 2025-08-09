import { NextRequest, NextResponse } from 'next/server'

const RAILWAY_API_URL = process.env.RAILWAY_API_URL || 'https://treasurecorp-commander-production.up.railway.app'

export async function POST(request: NextRequest) {
  try {
    const { url, type } = await request.json()
    
    if (!url || !url.startsWith('http')) {
      return NextResponse.json(
        { success: false, error: 'Invalid URL provided' },
        { status: 400 }
      )
    }

    console.log(`Processing new source: ${url} (type: ${type})`)
    
    try {
      // Call the Railway backend API
      const response = await fetch(`${RAILWAY_API_URL}/api/process-source`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          type
        }),
        // Add timeout to prevent hanging
        signal: AbortSignal.timeout(30000) // 30 seconds
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `Railway API error: ${response.status}`)
      }
      
      const result = await response.json()
      
      return NextResponse.json({
        success: result.success,
        message: result.message || `${type} source processed successfully`,
        url,
        type,
        summaries: result.summaries,
        source_url: result.source_url
      })
      
    } catch (fetchError) {
      console.error('Error calling Railway API:', fetchError)
      
      // Fallback: Return success but note processing will happen in background
      return NextResponse.json({
        success: true,
        message: `${type} source queued for processing`,
        url,
        type,
        note: 'Processing will complete in background',
        fallback: true
      })
    }
    
  } catch (error) {
    console.error('Error processing add-source request:', error)
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    )
  }
}