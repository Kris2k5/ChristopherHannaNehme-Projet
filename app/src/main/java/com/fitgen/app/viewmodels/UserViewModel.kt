package com.fitgen.app.viewmodels

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.fitgen.app.models.User
import com.fitgen.app.repositories.UserRepository
import com.fitgen.app.utils.CalorieCalculator
import com.fitgen.app.utils.Constants
import kotlinx.coroutines.launch

/**
 * ViewModel for managing user data and authentication state
 */
class UserViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = UserRepository(application)

    // User data
    private val _user = MutableLiveData<User?>()
    val user: LiveData<User?> = _user

    // Loading state
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading

    // Error state
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error

    // Authentication state
    private val _isLoggedIn = MutableLiveData<Boolean>()
    val isLoggedIn: LiveData<Boolean> = _isLoggedIn

    // Login result
    private val _loginResult = MutableLiveData<Result<String>?>()
    val loginResult: LiveData<Result<String>?> = _loginResult

    // Register result
    private val _registerResult = MutableLiveData<Result<String>?>()
    val registerResult: LiveData<Result<String>?> = _registerResult

    // Password reset result
    private val _passwordResetResult = MutableLiveData<Result<Unit>?>()
    val passwordResetResult: LiveData<Result<Unit>?> = _passwordResetResult

    // Profile update result
    private val _profileUpdateResult = MutableLiveData<Result<Unit>?>()
    val profileUpdateResult: LiveData<Result<Unit>?> = _profileUpdateResult

    // Onboarding completion result
    private val _onboardingResult = MutableLiveData<Result<Unit>?>()
    val onboardingResult: LiveData<Result<Unit>?> = _onboardingResult

    // Calorie data
    private val _bmr = MutableLiveData<Int>()
    val bmr: LiveData<Int> = _bmr

    private val _dailyCalories = MutableLiveData<Int>()
    val dailyCalories: LiveData<Int> = _dailyCalories

    private val _bmi = MutableLiveData<Double>()
    val bmi: LiveData<Double> = _bmi

    private val _bmiClassification = MutableLiveData<String>()
    val bmiClassification: LiveData<String> = _bmiClassification

    init {
        checkAuthState()
    }

    /**
     * Check if user is logged in and load their data
     */
    fun checkAuthState() {
        _isLoggedIn.value = repository.isUserLoggedIn()
        if (repository.isUserLoggedIn()) {
            loadCurrentUser()
        }
    }

    /**
     * Sign in with email and password
     */
    fun signIn(email: String, password: String) {
        _isLoading.value = true
        _error.value = null
        
        viewModelScope.launch {
            val result = repository.signIn(email, password)
            _loginResult.value = result
            _isLoading.value = false
            
            if (result.isSuccess) {
                _isLoggedIn.value = true
                loadCurrentUser()
            } else {
                _error.value = result.exceptionOrNull()?.message
            }
        }
    }

    /**
     * Register a new user
     */
    fun register(email: String, password: String) {
        _isLoading.value = true
        _error.value = null
        
        viewModelScope.launch {
            val result = repository.register(email, password)
            _registerResult.value = result
            _isLoading.value = false
            
            if (result.isSuccess) {
                _isLoggedIn.value = true
                // Create initial user profile
                val uid = result.getOrNull() ?: return@launch
                val newUser = User(
                    uid = uid,
                    email = email,
                    onboardingCompleted = false
                )
                repository.saveUser(newUser)
                _user.value = newUser
            } else {
                _error.value = result.exceptionOrNull()?.message
            }
        }
    }

    /**
     * Send password reset email
     */
    fun sendPasswordResetEmail(email: String) {
        _isLoading.value = true
        
        viewModelScope.launch {
            val result = repository.sendPasswordResetEmail(email)
            _passwordResetResult.value = result
            _isLoading.value = false
        }
    }

    /**
     * Sign out current user
     */
    fun signOut() {
        repository.signOut()
        _isLoggedIn.value = false
        _user.value = null
        _loginResult.value = null
        _registerResult.value = null
    }

    /**
     * Load current user from Firestore
     */
    fun loadCurrentUser() {
        val uid = repository.getCurrentUserId() ?: return
        _isLoading.value = true
        
        viewModelScope.launch {
            val result = repository.getUser(uid)
            _isLoading.value = false
            
            if (result.isSuccess) {
                val user = result.getOrNull()
                _user.value = user
                user?.let { calculateHealthMetrics(it) }
            } else {
                _error.value = result.exceptionOrNull()?.message
                // Try local user
                val localUser = repository.getLocalUser()
                if (localUser != null) {
                    _user.value = localUser
                    calculateHealthMetrics(localUser)
                }
            }
        }
    }

    /**
     * Check if user has completed onboarding
     */
    suspend fun hasCompletedOnboarding(): Boolean {
        val uid = repository.getCurrentUserId() ?: return false
        return repository.hasCompletedOnboarding(uid)
    }

    /**
     * Complete onboarding with user data
     */
    fun completeOnboarding(age: Int, height: Int, weight: Double, goal: String, activityLevel: String) {
        val uid = repository.getCurrentUserId() ?: return
        val email = repository.getCurrentUserEmail() ?: return
        
        _isLoading.value = true
        
        val user = User(
            uid = uid,
            email = email,
            age = age,
            height = height,
            weight = weight,
            gender = Constants.GENDER_MALE, // Default, can be added in future
            goal = goal,
            activityLevel = activityLevel,
            onboardingCompleted = true
        )
        
        viewModelScope.launch {
            val result = repository.saveUser(user)
            _onboardingResult.value = result
            _isLoading.value = false
            
            if (result.isSuccess) {
                _user.value = user
                calculateHealthMetrics(user)
            } else {
                _error.value = result.exceptionOrNull()?.message
            }
        }
    }

    /**
     * Update user profile
     */
    fun updateProfile(age: Int, height: Int, weight: Double, goal: String, activityLevel: String) {
        val currentUser = _user.value ?: return
        
        _isLoading.value = true
        
        val updatedUser = currentUser.copy(
            age = age,
            height = height,
            weight = weight,
            goal = goal,
            activityLevel = activityLevel
        )
        
        viewModelScope.launch {
            val result = repository.updateUser(updatedUser)
            _profileUpdateResult.value = result
            _isLoading.value = false
            
            if (result.isSuccess) {
                _user.value = updatedUser
                calculateHealthMetrics(updatedUser)
            } else {
                _error.value = result.exceptionOrNull()?.message
            }
        }
    }

    /**
     * Calculate health metrics (BMR, TDEE, daily calories, BMI)
     */
    private fun calculateHealthMetrics(user: User) {
        if (user.weight > 0 && user.height > 0 && user.age > 0) {
            val (bmr, _, dailyGoal) = CalorieCalculator.calculateCaloriesForUser(user)
            _bmr.value = bmr
            _dailyCalories.value = dailyGoal
            
            val bmi = CalorieCalculator.calculateBMI(user.weight, user.height)
            _bmi.value = bmi
            _bmiClassification.value = CalorieCalculator.getBMIClassification(bmi)
        }
    }

    /**
     * Get current user ID
     */
    fun getCurrentUserId(): String? {
        return repository.getCurrentUserId()
    }

    /**
     * Get display name from email (first part before @)
     */
    fun getDisplayName(): String {
        val email = _user.value?.email ?: repository.getCurrentUserEmail() ?: ""
        return email.substringBefore("@").replaceFirstChar { it.uppercase() }
    }

    /**
     * Clear error state
     */
    fun clearError() {
        _error.value = null
    }

    /**
     * Clear login result
     */
    fun clearLoginResult() {
        _loginResult.value = null
    }

    /**
     * Clear register result
     */
    fun clearRegisterResult() {
        _registerResult.value = null
    }

    /**
     * Clear password reset result
     */
    fun clearPasswordResetResult() {
        _passwordResetResult.value = null
    }

    /**
     * Clear profile update result
     */
    fun clearProfileUpdateResult() {
        _profileUpdateResult.value = null
    }

    /**
     * Clear onboarding result
     */
    fun clearOnboardingResult() {
        _onboardingResult.value = null
    }
}
