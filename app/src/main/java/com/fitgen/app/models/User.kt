package com.fitgen.app.models

import com.fitgen.app.utils.Constants

/**
 * User data model representing a user profile
 */
data class User(
    val uid: String = "",
    val email: String = "",
    val age: Int = 0,
    val height: Int = 0, // cm
    val weight: Double = 0.0, // kg
    val gender: String = Constants.GENDER_MALE,
    val goal: String = Constants.GOAL_LOSE_WEIGHT,
    val activityLevel: String = Constants.ACTIVITY_SEDENTARY,
    val onboardingCompleted: Boolean = false
) {
    /**
     * Convert User object to a Map for Firestore
     */
    fun toMap(): Map<String, Any> {
        return mapOf(
            "uid" to uid,
            "email" to email,
            "age" to age,
            "height" to height,
            "weight" to weight,
            "gender" to gender,
            "goal" to goal,
            "activityLevel" to activityLevel,
            "onboardingCompleted" to onboardingCompleted
        )
    }

    companion object {
        /**
         * Create User object from Firestore document data
         */
        fun fromMap(data: Map<String, Any?>): User {
            return User(
                uid = data["uid"] as? String ?: "",
                email = data["email"] as? String ?: "",
                age = (data["age"] as? Long)?.toInt() ?: 0,
                height = (data["height"] as? Long)?.toInt() ?: 0,
                weight = (data["weight"] as? Number)?.toDouble() ?: 0.0,
                gender = data["gender"] as? String ?: Constants.GENDER_MALE,
                goal = data["goal"] as? String ?: Constants.GOAL_LOSE_WEIGHT,
                activityLevel = data["activityLevel"] as? String ?: Constants.ACTIVITY_SEDENTARY,
                onboardingCompleted = data["onboardingCompleted"] as? Boolean ?: false
            )
        }
    }
}
