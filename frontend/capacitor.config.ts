import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.ispp.app',
  appName: 'ISPP',
  webDir: 'dist',
  server: {
    androidScheme: 'http',
    cleartext: true,
    hostname: '10.0.2.2'
  },
  android: {
    allowMixedContent: true,
    webContentsDebuggingEnabled: true
  }
};

export default config;
