# FitGen - Android Fitness Application

A simplified Android fitness application demonstrating user authentication, profile management, and health statistics calculations (BMI, BMR, calorie goals). Built for a teacher presentation.

## Features

- **User Authentication**: Firebase Authentication with email/password
  - Login with validation
  - Registration with password confirmation
  - Password reset functionality
  
- **User Onboarding**: 5-step guided setup
  - Age, height, weight input
  - Fitness goal selection
  - Activity level selection
  
- **Health Dashboard**:
  - Daily calorie goal calculation
  - BMR (Basal Metabolic Rate) calculation using Mifflin-St Jeor equation
  - BMI (Body Mass Index) with classification
  
- **Profile Management**:
  - View personal information
  - Edit profile details
  - Logout functionality

## Technical Stack

- **Language**: Kotlin
- **UI**: XML layouts with Material Design 3
- **Architecture**: MVVM (Model-View-ViewModel)
- **Navigation**: Android Navigation Component
- **Authentication**: Firebase Authentication
- **Database**: Firebase Firestore
- **Local Storage**: SharedPreferences

## Project Structure

```
app/src/main/java/com/fitgen/app/
├── activities/
│   ├── LoginActivity.kt
│   ├── RegisterActivity.kt
│   ├── OnboardingActivity.kt
│   └── MainActivity.kt
├── fragments/
│   ├── HomeFragment.kt
│   ├── WorkoutsFragment.kt
│   └── ProfileFragment.kt
├── models/
│   └── User.kt
├── viewmodels/
│   └── UserViewModel.kt
├── repositories/
│   └── UserRepository.kt
└── utils/
    ├── CalorieCalculator.kt
    └── Constants.kt
```

## Setup Instructions

### Prerequisites

1. Android Studio Arctic Fox (2020.3.1) or newer
2. Android SDK 35 (Android 14)
3. Firebase account

### Firebase Configuration

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Add an Android app with package name: `com.fitgen.app`
4. Download the `google-services.json` file
5. Place it in the `app/` directory (replacing the example file)

### Enable Firebase Services

1. **Authentication**:
   - Go to Firebase Console > Authentication
   - Click "Get Started"
   - Enable "Email/Password" sign-in provider

2. **Firestore Database**:
   - Go to Firebase Console > Firestore Database
   - Click "Create database"
   - Select "Start in test mode" for development
   - Choose a location and create

### Running the App

1. Clone this repository
2. Open in Android Studio
3. Configure Firebase (see above)
4. Sync Gradle files
5. Run on emulator or device (API 24+)

## Requirements

- **minSdk**: 24 (Android 7.0)
- **targetSdk**: 35 (Android 14)
- **compileSdk**: 35

## Health Calculations

### BMR (Basal Metabolic Rate) - Mifflin-St Jeor Equation

**For men:**
```
BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) + 5
```

**For women:**
```
BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) - 161
```

### Daily Calorie Goal

Based on activity level multiplier:
- Sedentary: BMR × 1.2
- Lightly Active: BMR × 1.375
- Moderately Active: BMR × 1.55
- Very Active: BMR × 1.725

Adjusted for goals:
- Lose Weight: TDEE - 500 calories
- Maintain Weight: TDEE
- Gain Muscle: TDEE + 300 calories

### BMI (Body Mass Index)

```
BMI = weight(kg) / height(m)²
```

Classifications:
- Underweight: < 18.5
- Normal: 18.5 - 24.9
- Overweight: 25 - 29.9
- Obese: ≥ 30

## License

This project is for educational purposes.