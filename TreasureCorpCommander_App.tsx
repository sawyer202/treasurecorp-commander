import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider } from 'react-redux';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, Platform } from 'react-native';
import { Provider as PaperProvider } from 'react-native-paper';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

// Import custom screens
import DashboardScreen from './src/screens/DashboardScreen';
import ContentScreen from './src/screens/ContentScreen';
import AnalyticsScreen from './src/screens/AnalyticsScreen';
import ScheduleScreen from './src/screens/ScheduleScreen';
import SettingsScreen from './src/screens/SettingsScreen';

// Redux store
import { store } from './src/store/store';

// WebSocket service
import WebSocketService from './src/services/WebSocketService';

// Theme
import { theme } from './src/theme/theme';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Main tab navigator
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'Dashboard') {
            iconName = focused ? 'analytics' : 'analytics-outline';
          } else if (route.name === 'Content') {
            iconName = focused ? 'document-text' : 'document-text-outline';
          } else if (route.name === 'Analytics') {
            iconName = focused ? 'bar-chart' : 'bar-chart-outline';
          } else if (route.name === 'Schedule') {
            iconName = focused ? 'calendar' : 'calendar-outline';
          } else if (route.name === 'Settings') {
            iconName = focused ? 'settings' : 'settings-outline';
          } else {
            iconName = 'help-circle-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: theme.colors.disabled,
        tabBarStyle: {
          backgroundColor: theme.colors.surface,
          borderTopColor: theme.colors.outline,
          paddingBottom: Platform.OS === 'ios' ? 20 : 5,
          height: Platform.OS === 'ios' ? 80 : 60,
        },
        headerStyle: {
          backgroundColor: theme.colors.surface,
        },
        headerTintColor: theme.colors.onSurface,
        headerTitleStyle: {
          fontWeight: 'bold',
          fontSize: 18,
        },
      })}
    >
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen}
        options={{
          headerTitle: 'TreasureCorp Commander',
          headerRight: () => (
            <View style={{ paddingRight: 15 }}>
              <Ionicons name="notifications" size={24} color={theme.colors.onSurface} />
            </View>
          ),
        }}
      />
      <Tab.Screen 
        name="Content" 
        component={ContentScreen}
        options={{
          headerTitle: 'Content Hub',
        }}
      />
      <Tab.Screen 
        name="Analytics" 
        component={AnalyticsScreen}
        options={{
          headerTitle: 'Growth Analytics',
        }}
      />
      <Tab.Screen 
        name="Schedule" 
        component={ScheduleScreen}
        options={{
          headerTitle: 'Posting Schedule',
        }}
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{
          headerTitle: 'Settings',
        }}
      />
    </Tab.Navigator>
  );
}

// Main App component
export default function App() {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Initialize WebSocket connection
    const initializeWebSocket = async () => {
      try {
        await WebSocketService.connect();
        setIsConnected(true);
        
        // Listen for real-time updates
        WebSocketService.on('viral_alert', (data) => {
          // Handle viral content alerts
          console.log('Viral alert received:', data);
        });

        WebSocketService.on('growth_update', (data) => {
          // Handle growth metric updates
          console.log('Growth update:', data);
        });

        WebSocketService.on('post_created', (data) => {
          // Handle new post notifications
          console.log('New post created:', data);
        });
        
      } catch (error) {
        console.error('WebSocket connection failed:', error);
        setIsConnected(false);
      }
    };

    initializeWebSocket();

    // Cleanup on unmount
    return () => {
      WebSocketService.disconnect();
    };
  }, []);

  return (
    <Provider store={store}>
      <PaperProvider theme={theme}>
        <SafeAreaProvider>
          <NavigationContainer>
            <StatusBar style="light" backgroundColor={theme.colors.surface} />
            <MainTabs />
          </NavigationContainer>
        </SafeAreaProvider>
      </PaperProvider>
    </Provider>
  );
}

// Styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
});