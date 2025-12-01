package com.fitgen.app.utils

import com.fitgen.app.models.User

/**
 * Utility class for calculating calories, BMR, and BMI
 * Uses the Mifflin-St Jeor equation for BMR calculation
 */
object CalorieCalculator {

    /**
     * Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor equation
     * 
     * For men: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) + 5
     * For women: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) - 161
     * 
     * @param weight Weight in kilograms
     * @param height Height in centimeters
     * @param age Age in years
     * @param gender Gender (male or female)
     * @return BMR in calories
     */
    fun calculateBMR(weight: Double, height: Int, age: Int, gender: String): Double {
        val baseBMR = (10 * weight) + (6.25 * height) - (5 * age)
        return if (gender == Constants.GENDER_MALE) {
            baseBMR + 5
        } else {
            baseBMR - 161
        }
    }

    /**
     * Get activity multiplier based on activity level
     * 
     * @param activityLevel Activity level constant
     * @return Multiplier value
     */
    fun getActivityMultiplier(activityLevel: String): Double {
        return when (activityLevel) {
            Constants.ACTIVITY_SEDENTARY -> 1.2
            Constants.ACTIVITY_LIGHTLY_ACTIVE -> 1.375
            Constants.ACTIVITY_MODERATELY_ACTIVE -> 1.55
            Constants.ACTIVITY_VERY_ACTIVE -> 1.725
            else -> 1.2
        }
    }

    /**
     * Calculate Total Daily Energy Expenditure (TDEE)
     * TDEE = BMR × Activity Multiplier
     * 
     * @param bmr Basal Metabolic Rate
     * @param activityLevel Activity level constant
     * @return TDEE in calories
     */
    fun calculateTDEE(bmr: Double, activityLevel: String): Double {
        return bmr * getActivityMultiplier(activityLevel)
    }

    /**
     * Calculate daily calorie goal based on user's goal
     * 
     * - Lose Weight: TDEE - 500 calories (0.5kg/week deficit)
     * - Maintain: TDEE
     * - Gain Muscle: TDEE + 300 calories (lean bulk)
     * 
     * @param tdee Total Daily Energy Expenditure
     * @param goal User's fitness goal
     * @return Daily calorie goal
     */
    fun calculateDailyCalorieGoal(tdee: Double, goal: String): Int {
        val adjustedCalories = when (goal) {
            Constants.GOAL_LOSE_WEIGHT -> tdee - 500
            Constants.GOAL_MAINTAIN -> tdee
            Constants.GOAL_GAIN_MUSCLE -> tdee + 300
            else -> tdee
        }
        return adjustedCalories.toInt().coerceAtLeast(1200) // Minimum safe calorie intake
    }

    /**
     * Calculate all calorie metrics for a user
     * 
     * @param user User object with all necessary data
     * @return Triple of (BMR, TDEE, DailyCalorieGoal)
     */
    fun calculateCaloriesForUser(user: User): Triple<Int, Int, Int> {
        val bmr = calculateBMR(user.weight, user.height, user.age, user.gender)
        val tdee = calculateTDEE(bmr, user.activityLevel)
        val dailyGoal = calculateDailyCalorieGoal(tdee, user.goal)
        return Triple(bmr.toInt(), tdee.toInt(), dailyGoal)
    }

    /**
     * Calculate Body Mass Index (BMI)
     * BMI = weight(kg) / height(m)²
     * 
     * @param weight Weight in kilograms
     * @param height Height in centimeters
     * @return BMI value
     */
    fun calculateBMI(weight: Double, height: Int): Double {
        val heightInMeters = height / 100.0
        return weight / (heightInMeters * heightInMeters)
    }

    /**
     * Get BMI classification
     * 
     * @param bmi BMI value
     * @return Classification string
     */
    fun getBMIClassification(bmi: Double): String {
        return when {
            bmi < 18.5 -> "underweight"
            bmi < 25.0 -> "normal"
            bmi < 30.0 -> "overweight"
            else -> "obese"
        }
    }
}
