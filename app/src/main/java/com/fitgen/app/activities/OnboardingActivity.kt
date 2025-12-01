package com.fitgen.app.activities

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.RadioGroup
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.fitgen.app.R
import com.fitgen.app.databinding.ActivityOnboardingBinding
import com.fitgen.app.utils.Constants
import com.fitgen.app.viewmodels.UserViewModel
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout

class OnboardingActivity : AppCompatActivity() {

    private lateinit var binding: ActivityOnboardingBinding
    private val viewModel: UserViewModel by viewModels()

    private var currentStep = 0
    
    // User data collected during onboarding
    private var age: Int = 0
    private var height: Int = 0
    private var weight: Double = 0.0
    private var goal: String = Constants.GOAL_LOSE_WEIGHT
    private var activityLevel: String = Constants.ACTIVITY_SEDENTARY

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOnboardingBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupClickListeners()
        observeViewModel()
        showStep(currentStep)
    }

    private fun setupClickListeners() {
        binding.btnNext.setOnClickListener {
            if (validateCurrentStep()) {
                saveCurrentStepData()
                if (currentStep < Constants.ONBOARDING_STEPS - 1) {
                    currentStep++
                    showStep(currentStep)
                } else {
                    completeOnboarding()
                }
            }
        }

        binding.btnPrevious.setOnClickListener {
            if (currentStep > 0) {
                currentStep--
                showStep(currentStep)
            }
        }
    }

    private fun observeViewModel() {
        viewModel.isLoading.observe(this) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
            binding.btnNext.isEnabled = !isLoading
            binding.btnPrevious.isEnabled = !isLoading
        }

        viewModel.onboardingResult.observe(this) { result ->
            result?.let {
                if (it.isSuccess) {
                    navigateToMain()
                } else {
                    Toast.makeText(this, R.string.error_general, Toast.LENGTH_SHORT).show()
                }
                viewModel.clearOnboardingResult()
            }
        }
    }

    private fun showStep(step: Int) {
        // Update step indicator
        binding.tvStepIndicator.text = getString(R.string.step_indicator, step + 1, Constants.ONBOARDING_STEPS)

        // Show/hide previous button
        binding.btnPrevious.visibility = if (step > 0) View.VISIBLE else View.INVISIBLE

        // Update next button text
        binding.btnNext.text = if (step == Constants.ONBOARDING_STEPS - 1) {
            getString(R.string.btn_finish)
        } else {
            getString(R.string.btn_next)
        }

        // Load step layout
        binding.stepContainer.removeAllViews()
        val stepView = when (step) {
            Constants.STEP_AGE -> inflateAgeStep()
            Constants.STEP_HEIGHT -> inflateHeightStep()
            Constants.STEP_WEIGHT -> inflateWeightStep()
            Constants.STEP_GOAL -> inflateGoalStep()
            Constants.STEP_ACTIVITY -> inflateActivityStep()
            else -> null
        }
        stepView?.let { binding.stepContainer.addView(it) }
    }

    private fun inflateAgeStep(): View {
        val view = LayoutInflater.from(this).inflate(R.layout.onboarding_step_age, binding.stepContainer, false)
        if (age > 0) {
            view.findViewById<TextInputEditText>(R.id.etAge).setText(age.toString())
        }
        return view
    }

    private fun inflateHeightStep(): View {
        val view = LayoutInflater.from(this).inflate(R.layout.onboarding_step_height, binding.stepContainer, false)
        if (height > 0) {
            view.findViewById<TextInputEditText>(R.id.etHeight).setText(height.toString())
        }
        return view
    }

    private fun inflateWeightStep(): View {
        val view = LayoutInflater.from(this).inflate(R.layout.onboarding_step_weight, binding.stepContainer, false)
        if (weight > 0) {
            view.findViewById<TextInputEditText>(R.id.etWeight).setText(weight.toString())
        }
        return view
    }

    private fun inflateGoalStep(): View {
        val view = LayoutInflater.from(this).inflate(R.layout.onboarding_step_goal, binding.stepContainer, false)
        val radioGroup = view.findViewById<RadioGroup>(R.id.rgGoal)
        when (goal) {
            Constants.GOAL_LOSE_WEIGHT -> radioGroup.check(R.id.rbLoseWeight)
            Constants.GOAL_MAINTAIN -> radioGroup.check(R.id.rbMaintain)
            Constants.GOAL_GAIN_MUSCLE -> radioGroup.check(R.id.rbGainMuscle)
        }
        return view
    }

    private fun inflateActivityStep(): View {
        val view = LayoutInflater.from(this).inflate(R.layout.onboarding_step_activity, binding.stepContainer, false)
        val radioGroup = view.findViewById<RadioGroup>(R.id.rgActivity)
        when (activityLevel) {
            Constants.ACTIVITY_SEDENTARY -> radioGroup.check(R.id.rbSedentary)
            Constants.ACTIVITY_LIGHTLY_ACTIVE -> radioGroup.check(R.id.rbLightlyActive)
            Constants.ACTIVITY_MODERATELY_ACTIVE -> radioGroup.check(R.id.rbModeratelyActive)
            Constants.ACTIVITY_VERY_ACTIVE -> radioGroup.check(R.id.rbVeryActive)
        }
        return view
    }

    private fun validateCurrentStep(): Boolean {
        return when (currentStep) {
            Constants.STEP_AGE -> validateAge()
            Constants.STEP_HEIGHT -> validateHeight()
            Constants.STEP_WEIGHT -> validateWeight()
            Constants.STEP_GOAL -> validateGoal()
            Constants.STEP_ACTIVITY -> validateActivity()
            else -> true
        }
    }

    private fun validateAge(): Boolean {
        val etAge = binding.stepContainer.findViewById<TextInputEditText>(R.id.etAge)
        val tilAge = binding.stepContainer.findViewById<TextInputLayout>(R.id.tilAge)
        val ageValue = etAge?.text.toString().toIntOrNull() ?: 0

        return if (ageValue < Constants.MIN_AGE || ageValue > Constants.MAX_AGE) {
            tilAge?.error = getString(R.string.error_invalid_age)
            false
        } else {
            tilAge?.error = null
            true
        }
    }

    private fun validateHeight(): Boolean {
        val etHeight = binding.stepContainer.findViewById<TextInputEditText>(R.id.etHeight)
        val tilHeight = binding.stepContainer.findViewById<TextInputLayout>(R.id.tilHeight)
        val heightValue = etHeight?.text.toString().toIntOrNull() ?: 0

        return if (heightValue < Constants.MIN_HEIGHT || heightValue > Constants.MAX_HEIGHT) {
            tilHeight?.error = getString(R.string.error_invalid_height)
            false
        } else {
            tilHeight?.error = null
            true
        }
    }

    private fun validateWeight(): Boolean {
        val etWeight = binding.stepContainer.findViewById<TextInputEditText>(R.id.etWeight)
        val tilWeight = binding.stepContainer.findViewById<TextInputLayout>(R.id.tilWeight)
        val weightValue = etWeight?.text.toString().toDoubleOrNull() ?: 0.0

        return if (weightValue < Constants.MIN_WEIGHT || weightValue > Constants.MAX_WEIGHT) {
            tilWeight?.error = getString(R.string.error_invalid_weight)
            false
        } else {
            tilWeight?.error = null
            true
        }
    }

    private fun validateGoal(): Boolean {
        val radioGroup = binding.stepContainer.findViewById<RadioGroup>(R.id.rgGoal)
        return if (radioGroup?.checkedRadioButtonId == -1) {
            Toast.makeText(this, R.string.error_select_goal, Toast.LENGTH_SHORT).show()
            false
        } else {
            true
        }
    }

    private fun validateActivity(): Boolean {
        val radioGroup = binding.stepContainer.findViewById<RadioGroup>(R.id.rgActivity)
        return if (radioGroup?.checkedRadioButtonId == -1) {
            Toast.makeText(this, R.string.error_select_activity, Toast.LENGTH_SHORT).show()
            false
        } else {
            true
        }
    }

    private fun saveCurrentStepData() {
        when (currentStep) {
            Constants.STEP_AGE -> {
                val etAge = binding.stepContainer.findViewById<TextInputEditText>(R.id.etAge)
                age = etAge?.text.toString().toIntOrNull() ?: 0
            }
            Constants.STEP_HEIGHT -> {
                val etHeight = binding.stepContainer.findViewById<TextInputEditText>(R.id.etHeight)
                height = etHeight?.text.toString().toIntOrNull() ?: 0
            }
            Constants.STEP_WEIGHT -> {
                val etWeight = binding.stepContainer.findViewById<TextInputEditText>(R.id.etWeight)
                weight = etWeight?.text.toString().toDoubleOrNull() ?: 0.0
            }
            Constants.STEP_GOAL -> {
                val radioGroup = binding.stepContainer.findViewById<RadioGroup>(R.id.rgGoal)
                goal = when (radioGroup?.checkedRadioButtonId) {
                    R.id.rbLoseWeight -> Constants.GOAL_LOSE_WEIGHT
                    R.id.rbMaintain -> Constants.GOAL_MAINTAIN
                    R.id.rbGainMuscle -> Constants.GOAL_GAIN_MUSCLE
                    else -> Constants.GOAL_LOSE_WEIGHT
                }
            }
            Constants.STEP_ACTIVITY -> {
                val radioGroup = binding.stepContainer.findViewById<RadioGroup>(R.id.rgActivity)
                activityLevel = when (radioGroup?.checkedRadioButtonId) {
                    R.id.rbSedentary -> Constants.ACTIVITY_SEDENTARY
                    R.id.rbLightlyActive -> Constants.ACTIVITY_LIGHTLY_ACTIVE
                    R.id.rbModeratelyActive -> Constants.ACTIVITY_MODERATELY_ACTIVE
                    R.id.rbVeryActive -> Constants.ACTIVITY_VERY_ACTIVE
                    else -> Constants.ACTIVITY_SEDENTARY
                }
            }
        }
    }

    private fun completeOnboarding() {
        viewModel.completeOnboarding(age, height, weight, goal, activityLevel)
    }

    private fun navigateToMain() {
        val intent = Intent(this, MainActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
        finish()
    }
}
