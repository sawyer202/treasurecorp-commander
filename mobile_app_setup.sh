#!/bin/bash
"""
TreasureCorp Commander Mobile App Setup
React Native app with Expo for iOS and Android
"""

echo "🚀 Setting up TreasureCorp Commander Mobile App..."
echo "=================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Create React Native app with Expo
echo "📱 Creating React Native app with Expo..."
npx create-expo-app@latest TreasureCorpCommander --template typescript

cd TreasureCorpCommander

echo "📦 Installing dependencies..."

# Core dependencies
npm install @expo/vector-icons
npm install react-native-paper
npm install @react-navigation/native
npm install @react-navigation/stack
npm install @react-navigation/bottom-tabs
npm install react-native-screens
npm install react-native-safe-area-context
npm install react-native-gesture-handler
npm install react-native-reanimated

# State management
npm install @reduxjs/toolkit react-redux

# HTTP client and WebSocket
npm install axios
npm install socket.io-client

# Charts and animations
npm install react-native-chart-kit
npm install react-native-svg
npm install lottie-react-native

# Camera and media
npm install expo-camera
npm install expo-media-library
npm install expo-image-picker

# Push notifications
npm install expo-notifications

# Async storage
npm install @react-native-async-storage/async-storage

# Date/time utilities
npm install date-fns

# Development dependencies
npm install --save-dev @types/react-native

echo "✅ Dependencies installed successfully!"

echo "📱 Mobile app structure created!"
echo "📍 Location: ./TreasureCorpCommander/"
echo "🔧 To run: cd TreasureCorpCommander && npm start"