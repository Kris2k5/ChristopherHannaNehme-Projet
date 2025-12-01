package com.fitgen.app.activities

import android.content.Intent
import android.os.Bundle
import android.util.Patterns
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.fitgen.app.R
import com.fitgen.app.databinding.ActivityRegisterBinding
import com.fitgen.app.utils.Constants
import com.fitgen.app.viewmodels.UserViewModel

class RegisterActivity : AppCompatActivity() {

    private lateinit var binding: ActivityRegisterBinding
    private val viewModel: UserViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRegisterBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupClickListeners()
        observeViewModel()
    }

    private fun setupClickListeners() {
        binding.btnBack.setOnClickListener {
            finish()
        }

        binding.btnRegister.setOnClickListener {
            val email = binding.etEmail.text.toString().trim()
            val password = binding.etPassword.text.toString()
            val confirmPassword = binding.etConfirmPassword.text.toString()

            if (validateInput(email, password, confirmPassword)) {
                viewModel.register(email, password)
            }
        }

        binding.tvSignIn.setOnClickListener {
            finish()
        }
    }

    private fun observeViewModel() {
        viewModel.isLoading.observe(this) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
            binding.btnRegister.isEnabled = !isLoading
            binding.btnRegister.text = if (isLoading) "" else getString(R.string.btn_register)
        }

        viewModel.registerResult.observe(this) { result ->
            result?.let {
                if (it.isSuccess) {
                    navigateToOnboarding()
                } else {
                    Toast.makeText(this, R.string.error_register_failed, Toast.LENGTH_SHORT).show()
                }
                viewModel.clearRegisterResult()
            }
        }
    }

    private fun validateInput(email: String, password: String, confirmPassword: String): Boolean {
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

        if (confirmPassword != password) {
            binding.tilConfirmPassword.error = getString(R.string.error_passwords_not_match)
            isValid = false
        } else {
            binding.tilConfirmPassword.error = null
        }

        return isValid
    }

    private fun navigateToOnboarding() {
        val intent = Intent(this, OnboardingActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
        finish()
    }
}
