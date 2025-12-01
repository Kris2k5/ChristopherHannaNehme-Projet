package com.fitgen.app.repositories

import android.content.Context
import android.content.SharedPreferences
import com.fitgen.app.models.User
import com.fitgen.app.utils.Constants
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.gson.Gson
import kotlinx.coroutines.tasks.await

/**
 * Repository for managing user data operations
 * Handles Firebase Firestore operations and local SharedPreferences caching
 */
class UserRepository(private val context: Context) {

    private val auth: FirebaseAuth = FirebaseAuth.getInstance()
    private val firestore: FirebaseFirestore = FirebaseFirestore.getInstance()
    private val gson = Gson()

    private val prefs: SharedPreferences by lazy {
        context.getSharedPreferences(Constants.PREFS_NAME, Context.MODE_PRIVATE)
    }

    /**
     * Get the current authenticated user's UID
     */
    fun getCurrentUserId(): String? {
        return auth.currentUser?.uid
    }

    /**
     * Get the current user's email
     */
    fun getCurrentUserEmail(): String? {
        return auth.currentUser?.email
    }

    /**
     * Check if a user is currently logged in
     */
    fun isUserLoggedIn(): Boolean {
        return auth.currentUser != null
    }

    /**
     * Sign in with email and password
     * @return Result with user UID on success or exception on failure
     */
    suspend fun signIn(email: String, password: String): Result<String> {
        return try {
            val result = auth.signInWithEmailAndPassword(email, password).await()
            Result.success(result.user?.uid ?: "")
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Register a new user with email and password
     * @return Result with user UID on success or exception on failure
     */
    suspend fun register(email: String, password: String): Result<String> {
        return try {
            val result = auth.createUserWithEmailAndPassword(email, password).await()
            Result.success(result.user?.uid ?: "")
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Send password reset email
     */
    suspend fun sendPasswordResetEmail(email: String): Result<Unit> {
        return try {
            auth.sendPasswordResetEmail(email).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Sign out the current user
     */
    fun signOut() {
        auth.signOut()
        clearLocalUser()
    }

    /**
     * Save user data to Firestore
     */
    suspend fun saveUser(user: User): Result<Unit> {
        return try {
            firestore.collection(Constants.COLLECTION_USERS)
                .document(user.uid)
                .set(user.toMap())
                .await()
            saveLocalUser(user)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get user data from Firestore
     */
    suspend fun getUser(uid: String): Result<User> {
        return try {
            val document = firestore.collection(Constants.COLLECTION_USERS)
                .document(uid)
                .get()
                .await()
            
            if (document.exists()) {
                val user = User.fromMap(document.data ?: emptyMap())
                saveLocalUser(user)
                Result.success(user)
            } else {
                Result.failure(Exception("User not found"))
            }
        } catch (e: Exception) {
            // Try to get from local cache if network fails
            val localUser = getLocalUser()
            if (localUser != null) {
                Result.success(localUser)
            } else {
                Result.failure(e)
            }
        }
    }

    /**
     * Update user profile in Firestore
     */
    suspend fun updateUser(user: User): Result<Unit> {
        return try {
            firestore.collection(Constants.COLLECTION_USERS)
                .document(user.uid)
                .update(user.toMap())
                .await()
            saveLocalUser(user)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Check if user has completed onboarding
     */
    suspend fun hasCompletedOnboarding(uid: String): Boolean {
        return try {
            val user = getUser(uid).getOrNull()
            user?.onboardingCompleted ?: false
        } catch (e: Exception) {
            false
        }
    }

    /**
     * Save user data to SharedPreferences for offline access
     */
    private fun saveLocalUser(user: User) {
        val userJson = gson.toJson(user)
        prefs.edit().putString(Constants.PREF_USER_DATA, userJson).apply()
    }

    /**
     * Get user data from SharedPreferences
     */
    fun getLocalUser(): User? {
        val userJson = prefs.getString(Constants.PREF_USER_DATA, null) ?: return null
        return try {
            gson.fromJson(userJson, User::class.java)
        } catch (e: Exception) {
            null
        }
    }

    /**
     * Clear locally stored user data
     */
    private fun clearLocalUser() {
        prefs.edit().remove(Constants.PREF_USER_DATA).apply()
    }
}
