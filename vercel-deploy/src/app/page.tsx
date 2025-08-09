'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

interface GrowthMetric {
  platform: string
  followers: number
  daily_growth: number
  target_progress: number
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<GrowthMetric[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, 30000) // Update every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchMetrics = async () => {
    try {
      const response = await axios.get('/api/dashboard/metrics')
      setMetrics(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching metrics:', error)
      setLoading(false)
    }
  }

  const getTotalFollowers = () => {
    return metrics.reduce((sum, metric) => sum + metric.followers, 0)
  }

  const chartData = {
    labels: ['Twitter', 'Telegram'],
    datasets: [
      {
        label: 'Current Followers',
        data: metrics.map(m => m.followers),
        borderColor: 'rgb(0, 255, 136)',
        backgroundColor: 'rgba(0, 255, 136, 0.2)',
      },
      {
        label: 'Target Progress (%)',
        data: metrics.map(m => m.target_progress),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
      }
    ]
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-400 mx-auto"></div>
          <h2 className="text-xl mt-4">Loading TreasureCorp Commander...</h2>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-green-400 mb-2">
            🚀 TreasureCorp Commander
          </h1>
          <p className="text-gray-300">
            2-Month Growth Challenge: {getTotalFollowers().toLocaleString()} / 10,000 followers
          </p>
        </div>

        {/* Progress Overview */}
        <div className="bg-gray-900 rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">📊 Growth Progress</h2>
          <div className="w-full bg-gray-700 rounded-full h-4 mb-4">
            <div 
              className="bg-green-400 h-4 rounded-full transition-all duration-500"
              style={{ width: `${(getTotalFollowers() / 10000) * 100}%` }}
            ></div>
          </div>
          <p className="text-center text-green-400 font-semibold">
            {((getTotalFollowers() / 10000) * 100).toFixed(1)}% Complete
          </p>
        </div>

        {/* Platform Metrics */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {metrics.map((metric) => (
            <div key={metric.platform} className="bg-gray-900 rounded-lg p-6">
              <h3 className="text-xl font-semibold mb-2 capitalize">
                {metric.platform === 'twitter' && '🐦 Twitter'}
                {metric.platform === 'telegram' && '📱 Telegram'}
              </h3>
              <div className="text-3xl font-bold text-green-400 mb-2">
                {metric.followers.toLocaleString()}
              </div>
              <div className="text-sm text-gray-400">
                +{metric.daily_growth}/day • {metric.target_progress.toFixed(1)}% to target
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                <div 
                  className="bg-green-400 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(metric.target_progress, 100)}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>

        {/* Growth Chart */}
        <div className="bg-gray-900 rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">📈 Platform Performance</h2>
          <div className="h-96">
            <Line 
              data={chartData} 
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    labels: {
                      color: 'white'
                    }
                  }
                },
                scales: {
                  x: {
                    ticks: { color: 'white' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                  },
                  y: {
                    ticks: { color: 'white' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                  }
                }
              }}
            />
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-900 rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">⚡ Quick Actions</h2>
          <div className="grid md:grid-cols-4 gap-4">
            <button 
              onClick={() => {
                setLoading(true)
                fetchMetrics()
                setTimeout(() => setLoading(false), 2000)
              }}
              className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              🚀 Refresh Data
            </button>
            <button 
              onClick={() => window.open('https://twitter.com/compose/tweet?text=🚀%20Growing%20@Treasure_Corp%20community!%20Join%20us%20for%20DAO%20insights%20and%20decentralized%20finance%20updates.%20%23DAO%20%23Web3%20%23TreasureCorp', '_blank')}
              className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              📝 Tweet Now
            </button>
            <button 
              onClick={() => alert('📊 Analytics Dashboard\n\nCurrent Progress:\n• Twitter: ' + getTotalFollowers() + ' followers\n• Target: 10,000 followers\n• Progress: ' + ((getTotalFollowers() / 10000) * 100).toFixed(1) + '%')}
              className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              📊 View Analytics
            </button>
            <a 
              href="/admin"
              className="bg-orange-600 hover:bg-orange-700 px-6 py-3 rounded-lg font-semibold transition-colors text-center"
            >
              ⚙️ Update Followers
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
