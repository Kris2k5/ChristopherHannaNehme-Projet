package com.fitgen.app.utils

/**
 * Application-wide constants
 */
object Constants {
    // Firebase Collections
    const val COLLECTION_USERS = "users"
    
    // SharedPreferences
    const val PREFS_NAME = "fitgen_prefs"
    const val PREF_USER_DATA = "user_data"
    
    // Goals
    const val GOAL_LOSE_WEIGHT = "lose_weight"
    const val GOAL_MAINTAIN = "maintain"
    const val GOAL_GAIN_MUSCLE = "gain_muscle"
    
    // Activity Levels
    const val ACTIVITY_SEDENTARY = "sedentary"
    const val ACTIVITY_LIGHTLY_ACTIVE = "lightly_active"
    const val ACTIVITY_MODERATELY_ACTIVE = "moderately_active"
    const val ACTIVITY_VERY_ACTIVE = "very_active"
    
    // Gender
    const val GENDER_MALE = "male"
    const val GENDER_FEMALE = "female"
    
    // Validation Constants
    const val MIN_AGE = 15
    const val MAX_AGE = 100
    const val MIN_HEIGHT = 100
    const val MAX_HEIGHT = 250
    const val MIN_WEIGHT = 30.0
    const val MAX_WEIGHT = 300.0
    const val MIN_PASSWORD_LENGTH = 6
    
    // Onboarding Steps
    const val ONBOARDING_STEPS = 5
    const val STEP_AGE = 0
    const val STEP_HEIGHT = 1
    const val STEP_WEIGHT = 2
    const val STEP_GOAL = 3
    const val STEP_ACTIVITY = 4
}
