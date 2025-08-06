import React, { useEffect, useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  RefreshControl,
  Dimensions,
  Alert,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Chip,
  ProgressBar,
  Avatar,
  List,
} from 'react-native-paper';
import { LineChart } from 'react-native-chart-kit';
import { useSelector, useDispatch } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';

// Redux actions
import { fetchGrowthMetrics, fetchViralAlerts } from '../store/slices/dashboardSlice';

// Services
import ApiService from '../services/ApiService';
import WebSocketService from '../services/WebSocketService';

// Types
interface GrowthMetric {
  platform: string;
  followers: number;
  daily_growth: number;
  posts_count: number;
  engagement_rate: number;
  target_progress: number;
}

interface ViralAlert {
  content_id: number;
  title: string;
  viral_score: number;
  trending_hashtags: string[];
  recommended_action: string;
}

const { width } = Dimensions.get('window');

const DashboardScreen: React.FC = () => {
  const dispatch = useDispatch();
  const [refreshing, setRefreshing] = useState(false);
  const [metrics, setMetrics] = useState<GrowthMetric[]>([]);
  const [viralAlerts, setViralAlerts] = useState<ViralAlert[]>([]);
  const [isMonitoring, setIsMonitoring] = useState(false);

  // Chart data
  const [chartData, setChartData] = useState({
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        data: [120, 245, 189, 356, 289, 412, 398],
        color: (opacity = 1) => `rgba(0, 255, 136, ${opacity})`,
        strokeWidth: 3,
      },
    ],
  });

  useEffect(() => {
    loadDashboardData();
    
    // Listen for real-time updates
    WebSocketService.on('growth_update', handleGrowthUpdate);
    WebSocketService.on('viral_alert', handleViralAlert);
    
    return () => {
      WebSocketService.off('growth_update', handleGrowthUpdate);
      WebSocketService.off('viral_alert', handleViralAlert);
    };
  }, []);

  const loadDashboardData = async () => {
    try {
      const [metricsResponse, alertsResponse] = await Promise.all([
        ApiService.getGrowthMetrics(),
        ApiService.getViralAlerts(),
      ]);
      
      setMetrics(metricsResponse.data);
      setViralAlerts(alertsResponse.data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      Alert.alert('Error', 'Failed to load dashboard data');
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  const handleGrowthUpdate = (data: any) => {
    console.log('Growth update received:', data);
    loadDashboardData(); // Refresh metrics
  };

  const handleViralAlert = (data: ViralAlert) => {
    console.log('Viral alert received:', data);
    
    // Add to viral alerts
    setViralAlerts(prev => [data, ...prev]);
    
    // Show push notification style alert
    Alert.alert(
      '🚨 Viral Opportunity!',
      `${data.title}\nViral Score: ${data.viral_score}/100`,
      [
        { text: 'Dismiss', style: 'cancel' },
        { text: 'View Details', onPress: () => handleViralAlertAction(data) },
      ]
    );
  };

  const handleViralAlertAction = (alert: ViralAlert) => {
    // Navigate to content creation with pre-filled viral topic
    Alert.alert(
      'Recommended Action',
      alert.recommended_action,
      [
        { text: 'Create Post', onPress: () => createViralPost(alert) },
        { text: 'Later', style: 'cancel' },
      ]
    );
  };

  const createViralPost = (alert: ViralAlert) => {
    // Navigate to content creation screen with viral template
    console.log('Creating viral post for:', alert.title);
  };

  const startMonitoring = async () => {
    try {
      setIsMonitoring(true);
      await ApiService.startMonitoring();
      
      Alert.alert('Success', 'DAO monitoring started successfully!');
    } catch (error) {
      console.error('Error starting monitoring:', error);
      Alert.alert('Error', 'Failed to start monitoring');
      setIsMonitoring(false);
    }
  };

  const getTotalFollowers = () => {
    return metrics.reduce((sum, metric) => sum + metric.followers, 0);
  };

  const getOverallProgress = () => {
    const totalTarget = 10000; // 10K target
    return (getTotalFollowers() / totalTarget) * 100;
  };

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'twitter':
        return 'logo-twitter';
      case 'linkedin':
        return 'logo-linkedin';
      case 'telegram':
        return 'send';
      default:
        return 'globe';
    }
  };

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case 'twitter':
        return '#1DA1F2';
      case 'linkedin':
        return '#0077B5';
      case 'telegram':
        return '#0088CC';
      default:
        return '#6B7280';
    }
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
      }
    >
      {/* Overall Progress Card */}
      <Card style={styles.progressCard}>
        <Card.Content>
          <Title style={styles.cardTitle}>
            🎯 2-Month Growth Challenge
          </Title>
          <View style={styles.progressContainer}>
            <View style={styles.progressInfo}>
              <Paragraph style={styles.followerCount}>
                {getTotalFollowers().toLocaleString()} / 10,000 followers
              </Paragraph>
              <ProgressBar 
                progress={getOverallProgress() / 100} 
                color="#00ff88" 
                style={styles.progressBar}
              />
              <Paragraph style={styles.progressText}>
                {getOverallProgress().toFixed(1)}% complete
              </Paragraph>
            </View>
          </View>
        </Card.Content>
      </Card>

      {/* Growth Chart */}
      <Card style={styles.chartCard}>
        <Card.Content>
          <Title style={styles.cardTitle}>📈 Weekly Growth</Title>
          <LineChart
            data={chartData}
            width={width - 60}
            height={200}
            chartConfig={{
              backgroundColor: '#1a1a1a',
              backgroundGradientFrom: '#1a1a1a',
              backgroundGradientTo: '#2a2a2a',
              decimalPlaces: 0,
              color: (opacity = 1) => `rgba(0, 255, 136, ${opacity})`,
              labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
              style: {
                borderRadius: 16,
              },
            }}
            bezier
            style={styles.chart}
          />
        </Card.Content>
      </Card>

      {/* Platform Metrics */}
      <Card style={styles.metricsCard}>
        <Card.Content>
          <Title style={styles.cardTitle}>🚀 Platform Performance</Title>
          {metrics.map((metric, index) => (
            <View key={metric.platform} style={styles.metricRow}>
              <View style={styles.metricLeft}>
                <Avatar.Icon
                  size={40}
                  icon={() => (
                    <Ionicons
                      name={getPlatformIcon(metric.platform)}
                      size={20}
                      color="white"
                    />
                  )}
                  style={[
                    styles.platformIcon,
                    { backgroundColor: getPlatformColor(metric.platform) },
                  ]}
                />
                <View style={styles.metricInfo}>
                  <Title style={styles.platformTitle}>
                    {metric.platform.charAt(0).toUpperCase() + metric.platform.slice(1)}
                  </Title>
                  <Paragraph style={styles.followerText}>
                    {metric.followers.toLocaleString()} followers
                  </Paragraph>
                </View>
              </View>
              <View style={styles.metricRight}>
                <Chip
                  mode="outlined"
                  style={[
                    styles.growthChip,
                    { borderColor: metric.daily_growth > 0 ? '#00ff88' : '#ff6b6b' },
                  ]}
                  textStyle={[
                    styles.chipText,
                    { color: metric.daily_growth > 0 ? '#00ff88' : '#ff6b6b' },
                  ]}
                >
                  {metric.daily_growth > 0 ? '+' : ''}{metric.daily_growth}/day
                </Chip>
              </View>
            </View>
          ))}
        </Card.Content>
      </Card>

      {/* Viral Alerts */}
      {viralAlerts.length > 0 && (
        <Card style={styles.alertsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>🚨 Viral Opportunities</Title>
            {viralAlerts.slice(0, 3).map((alert) => (
              <List.Item
                key={alert.content_id}
                title={alert.title}
                description={`Viral Score: ${alert.viral_score}/100`}
                left={() => (
                  <Avatar.Icon
                    size={40}
                    icon="trending-up"
                    style={{ backgroundColor: '#ff6b6b' }}
                  />
                )}
                right={() => (
                  <Button
                    mode="contained"
                    compact
                    onPress={() => handleViralAlertAction(alert)}
                    style={styles.alertButton}
                  >
                    Act Now
                  </Button>
                )}
                style={styles.alertItem}
              />
            ))}
          </Card.Content>
        </Card>
      )}

      {/* Quick Actions */}
      <Card style={styles.actionsCard}>
        <Card.Content>
          <Title style={styles.cardTitle}>⚡ Quick Actions</Title>
          <View style={styles.actionButtons}>
            <Button
              mode="contained"
              onPress={startMonitoring}
              loading={isMonitoring}
              style={[styles.actionButton, { backgroundColor: '#00ff88' }]}
              labelStyle={styles.actionButtonText}
            >
              {isMonitoring ? 'Monitoring...' : 'Start Monitoring'}
            </Button>
            <Button
              mode="outlined"
              onPress={() => console.log('Create post')}
              style={styles.actionButton}
              labelStyle={styles.actionButtonText}
            >
              Create Post
            </Button>
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
    padding: 16,
  },
  progressCard: {
    backgroundColor: '#1a1a1a',
    marginBottom: 16,
    elevation: 4,
  },
  chartCard: {
    backgroundColor: '#1a1a1a',
    marginBottom: 16,
    elevation: 4,
  },
  metricsCard: {
    backgroundColor: '#1a1a1a',
    marginBottom: 16,
    elevation: 4,
  },
  alertsCard: {
    backgroundColor: '#1a1a1a',
    marginBottom: 16,
    elevation: 4,
  },
  actionsCard: {
    backgroundColor: '#1a1a1a',
    marginBottom: 16,
    elevation: 4,
  },
  cardTitle: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
  },
  progressContainer: {
    marginTop: 8,
  },
  progressInfo: {
    alignItems: 'center',
  },
  followerCount: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  progressBar: {
    width: '100%',
    height: 8,
    marginBottom: 8,
  },
  progressText: {
    color: '#00ff88',
    fontSize: 14,
    fontWeight: '600',
  },
  chart: {
    marginTop: 8,
    borderRadius: 16,
  },
  metricRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#333333',
  },
  metricLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  metricRight: {
    alignItems: 'flex-end',
  },
  platformIcon: {
    marginRight: 12,
  },
  metricInfo: {
    flex: 1,
  },
  platformTitle: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 2,
  },
  followerText: {
    color: '#cccccc',
    fontSize: 14,
  },
  growthChip: {
    backgroundColor: 'transparent',
  },
  chipText: {
    fontSize: 12,
    fontWeight: '600',
  },
  alertItem: {
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#333333',
  },
  alertButton: {
    backgroundColor: '#ff6b6b',
    minWidth: 80,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 12,
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 4,
  },
  actionButtonText: {
    fontSize: 14,
    fontWeight: '600',
  },
});

export default DashboardScreen;