# Testing TrackWise on iOS Simulator

## Setup Instructions

### Prerequisites
- Xcode installed with iOS simulators
- Flutter SDK configured
- Backend running on `http://localhost:8000`

### First-Time Setup (CocoaPods)

1. **Make sure you're using Homebrew Ruby** (required for CocoaPods):
   ```bash
   export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
   ```

2. **Install CocoaPods** (if not already installed):
   ```bash
   gem install cocoapods
   ```

3. **Install iOS dependencies**:
   ```bash
   cd ios
   pod install
   cd ..
   ```

### Running on iOS Simulator

1. **Start backend** (in a separate terminal):
   ```bash
   cd ../backend
   make run
   ```

2. **Check available simulators**:
   ```bash
   flutter devices
   ```

3. **Run on iPhone 16 Pro Max** (or any available simulator):
   ```bash
   export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
   flutter run -d 3A3AF854-C8E0-4336-9CFB-8DEB3712CF83
   ```

   Or to run on any available iOS device:
   ```bash
   flutter run -d ios
   ```

### Testing the Auth Flow

1. The app will launch with a welcome screen
2. Tap "Get Started" to see the login screen with the train illustration
3. Tap "Sign Up" to go to the signup screen
4. Try creating an account or logging in
5. You should be redirected to the home screen on success

### Common Issues

**CocoaPods not working:**
```bash
# Make sure to use Homebrew Ruby
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
cd ios && pod install && cd ..
```

**Simulator not found:**
```bash
# Open Simulator manually
open -a Simulator

# Then run flutter
flutter run
```

**Build errors:**
```bash
# Clean and rebuild
flutter clean
flutter pub get
cd ios && pod install && cd ..
flutter run
```

### Environment Setup

Make sure your `.env` file is configured:
```bash
API_BASE_URL=http://localhost:8000
ENVIRONMENT=development
```

### Quick Commands

```bash
# List all devices
flutter devices

# Run on specific device
flutter run -d <device-id>

# Run with verbose logging
flutter run -d ios --verbose

# Check for issues
flutter doctor -v
```

---

**Happy Testing! 🚀**
