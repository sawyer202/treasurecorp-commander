'use client'

import { useState } from 'react'

export default function AdminPanel() {
  const [twitter, setTwitter] = useState('')
  const [telegram, setTelegram] = useState('')
  const [message, setMessage] = useState('')

  const updateFollowers = async () => {
    try {
      const response = await fetch('/api/update-followers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          twitter: parseInt(twitter) || undefined,
          telegram: parseInt(telegram) || undefined,
        }),
      })

      const data = await response.json()
      if (data.success) {
        setMessage('✅ Followers updated successfully!')
        setTwitter('')
        setTelegram('')
      } else {
        setMessage('❌ Failed to update followers')
      }
    } catch (error) {
      setMessage('❌ Error updating followers')
    }
  }

  return (
    <div className="min-h-screen bg-black text-white p-8">
      <div className="max-w-md mx-auto">
        <h1 className="text-3xl font-bold text-green-400 mb-8 text-center">
          📊 Update Followers
        </h1>

        <div className="bg-gray-900 rounded-lg p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              🐦 Twitter Followers
            </label>
            <input
              type="number"
              value={twitter}
              onChange={(e) => setTwitter(e.target.value)}
              placeholder="60"
              className="w-full px-3 py-2 bg-gray-800 rounded border border-gray-700 focus:border-green-400 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              📱 Telegram Subscribers
            </label>
            <input
              type="number"
              value={telegram}
              onChange={(e) => setTelegram(e.target.value)}
              placeholder="3"
              className="w-full px-3 py-2 bg-gray-800 rounded border border-gray-700 focus:border-green-400 focus:outline-none"
            />
          </div>

          <button
            onClick={updateFollowers}
            className="w-full bg-green-600 hover:bg-green-700 px-4 py-2 rounded font-semibold transition-colors"
          >
            Update Dashboard
          </button>

          {message && (
            <div className="text-center text-sm mt-4">
              {message}
            </div>
          )}

          <div className="text-center mt-6">
            <a 
              href="/"
              className="text-green-400 hover:text-green-300 underline"
            >
              ← Back to Dashboard
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}