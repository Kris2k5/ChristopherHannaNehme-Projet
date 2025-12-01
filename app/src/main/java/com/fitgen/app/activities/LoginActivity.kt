package com.fitgen.app.activities

import android.content.Intent
import android.os.Bundle
import android.util.Patterns
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.fitgen.app.R
import com.fitgen.app.databinding.ActivityLoginBinding
import com.fitgen.app.utils.Constants
import com.fitgen.app.viewmodels.UserViewModel
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.textfield.TextInputEditText
import kotlinx.coroutines.launch

class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding
    private val viewModel: UserViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        checkIfAlreadyLoggedIn()
        setupClickListeners()
        observeViewModel()
    }

    private fun checkIfAlreadyLoggedIn() {
        if (viewModel.isLoggedIn.value == true) {
            lifecycleScope.launch {
                if (viewModel.hasCompletedOnboarding()) {
                    navigateToMain()
                } else {
                    navigateToOnboarding()
                }
            }
        }
    }

    private fun setupClickListeners() {
        binding.btnLogin.setOnClickListener {
            val email = binding.etEmail.text.toString().trim()
            val password = binding.etPassword.text.toString()

            if (validateInput(email, password)) {
                viewModel.signIn(email, password)
            }
        }

        binding.tvSignUp.setOnClickListener {
            startActivity(Intent(this, RegisterActivity::class.java))
        }

        binding.tvForgotPassword.setOnClickListener {
            showForgotPasswordDialog()
        }
    }

    private fun observeViewModel() {
        viewModel.isLoading.observe(this) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
            binding.btnLogin.isEnabled = !isLoading
            binding.btnLogin.text = if (isLoading) "" else getString(R.string.btn_login)
        }

        viewModel.loginResult.observe(this) { result ->
            result?.let {
                if (it.isSuccess) {
                    lifecycleScope.launch {
                        if (viewModel.hasCompletedOnboarding()) {
                            navigateToMain()
                        } else {
                            navigateToOnboarding()
                        }
                    }
                } else {
                    Toast.makeText(this, R.string.error_login_failed, Toast.LENGTH_SHORT).show()
                }
                viewModel.clearLoginResult()
            }
        }

        viewModel.passwordResetResult.observe(this) { result ->
            result?.let {
                if (it.isSuccess) {
                    Toast.makeText(this, R.string.password_reset_sent, Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this, R.string.password_reset_failed, Toast.LENGTH_SHORT).show()
                }
                viewModel.clearPasswordResetResult()
            }
        }
    }

    private fun validateInput(email: String, password: String): Boolean {
        var isValid = true

        if (email.isEmpty() || !Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            binding.tilEmail.error = getString(R.string.error_invalid_email)
            isValid = false
        } else {
            binding.tilEmail.error = null
        }

        if (password.isEmpty()) {
            binding.tilPassword.error = getString(R.string.error_empty_password)
            isValid = false
        } else if (password.length < Constants.MIN_PASSWORD_LENGTH) {
            binding.tilPassword.error = getString(R.string.error_password_min_length)
            isValid = false
        } else {
            binding.tilPassword.error = null
        }

        return isValid
    }

    private fun showForgotPasswordDialog() {
        val editText = TextInputEditText(this)
        editText.hint = getString(R.string.hint_email)

        MaterialAlertDialogBuilder(this)
            .setTitle(R.string.forgot_password)
            .setView(editText)
            .setPositiveButton(R.string.btn_login) { _, _ ->
                val email = editText.text.toString().trim()
                if (email.isNotEmpty() && Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
                    viewModel.sendPasswordResetEmail(email)
                } else {
                    Toast.makeText(this, R.string.error_invalid_email, Toast.LENGTH_SHORT).show()
                }
            }
            .setNegativeButton(R.string.btn_cancel, null)
            .show()
    }

    private fun navigateToMain() {
        val intent = Intent(this, MainActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
        finish()
    }

    private fun navigateToOnboarding() {
        val intent = Intent(this, OnboardingActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
        finish()
    }
}
