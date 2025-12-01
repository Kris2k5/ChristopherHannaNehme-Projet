package com.fitgen.app.fragments

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.RadioGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import com.fitgen.app.R
import com.fitgen.app.activities.LoginActivity
import com.fitgen.app.databinding.FragmentProfileBinding
import com.fitgen.app.utils.Constants
import com.fitgen.app.viewmodels.UserViewModel
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.textfield.TextInputEditText

class ProfileFragment : Fragment() {

    private var _binding: FragmentProfileBinding? = null
    private val binding get() = _binding!!
    private val viewModel: UserViewModel by activityViewModels()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentProfileBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupClickListeners()
        observeViewModel()
    }

    private fun setupClickListeners() {
        binding.btnEditProfile.setOnClickListener {
            showEditProfileDialog()
        }

        binding.btnLogout.setOnClickListener {
            showLogoutConfirmation()
        }
    }

    private fun observeViewModel() {
        viewModel.user.observe(viewLifecycleOwner) { user ->
            user?.let {
                binding.tvEmail.text = it.email
                binding.tvAge.text = getString(R.string.years_format, it.age)
                binding.tvHeight.text = getString(R.string.cm_format, it.height)
                binding.tvWeight.text = getString(R.string.kg_format, it.weight)
                binding.tvGoal.text = getGoalDisplayText(it.goal)
                binding.tvActivityLevel.text = getActivityLevelDisplayText(it.activityLevel)
            }
        }

        viewModel.profileUpdateResult.observe(viewLifecycleOwner) { result ->
            result?.let {
                if (it.isSuccess) {
                    Toast.makeText(requireContext(), R.string.profile_updated, Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(requireContext(), R.string.profile_update_failed, Toast.LENGTH_SHORT).show()
                }
                viewModel.clearProfileUpdateResult()
            }
        }
    }

    private fun getGoalDisplayText(goal: String): String {
        return when (goal) {
            Constants.GOAL_LOSE_WEIGHT -> getString(R.string.goal_lose_weight)
            Constants.GOAL_MAINTAIN -> getString(R.string.goal_maintain)
            Constants.GOAL_GAIN_MUSCLE -> getString(R.string.goal_gain_muscle)
            else -> goal
        }
    }

    private fun getActivityLevelDisplayText(activityLevel: String): String {
        return when (activityLevel) {
            Constants.ACTIVITY_SEDENTARY -> getString(R.string.activity_sedentary)
            Constants.ACTIVITY_LIGHTLY_ACTIVE -> getString(R.string.activity_lightly_active)
            Constants.ACTIVITY_MODERATELY_ACTIVE -> getString(R.string.activity_moderately_active)
            Constants.ACTIVITY_VERY_ACTIVE -> getString(R.string.activity_very_active)
            else -> activityLevel
        }
    }

    private fun showEditProfileDialog() {
        val dialogView = LayoutInflater.from(requireContext())
            .inflate(R.layout.dialog_edit_profile, null)

        val etAge = dialogView.findViewById<TextInputEditText>(R.id.etAge)
        val etHeight = dialogView.findViewById<TextInputEditText>(R.id.etHeight)
        val etWeight = dialogView.findViewById<TextInputEditText>(R.id.etWeight)
        val rgGoal = dialogView.findViewById<RadioGroup>(R.id.rgGoal)
        val rgActivity = dialogView.findViewById<RadioGroup>(R.id.rgActivity)

        // Pre-fill with current values
        viewModel.user.value?.let { user ->
            etAge.setText(user.age.toString())
            etHeight.setText(user.height.toString())
            etWeight.setText(user.weight.toString())
            
            when (user.goal) {
                Constants.GOAL_LOSE_WEIGHT -> rgGoal.check(R.id.rbLoseWeight)
                Constants.GOAL_MAINTAIN -> rgGoal.check(R.id.rbMaintain)
                Constants.GOAL_GAIN_MUSCLE -> rgGoal.check(R.id.rbGainMuscle)
            }
            
            when (user.activityLevel) {
                Constants.ACTIVITY_SEDENTARY -> rgActivity.check(R.id.rbSedentary)
                Constants.ACTIVITY_LIGHTLY_ACTIVE -> rgActivity.check(R.id.rbLightlyActive)
                Constants.ACTIVITY_MODERATELY_ACTIVE -> rgActivity.check(R.id.rbModeratelyActive)
                Constants.ACTIVITY_VERY_ACTIVE -> rgActivity.check(R.id.rbVeryActive)
            }
        }

        MaterialAlertDialogBuilder(requireContext())
            .setTitle(R.string.edit_profile_title)
            .setView(dialogView)
            .setPositiveButton(R.string.btn_save) { _, _ ->
                val age = etAge.text.toString().toIntOrNull() ?: 0
                val height = etHeight.text.toString().toIntOrNull() ?: 0
                val weight = etWeight.text.toString().toDoubleOrNull() ?: 0.0
                
                val goal = when (rgGoal.checkedRadioButtonId) {
                    R.id.rbLoseWeight -> Constants.GOAL_LOSE_WEIGHT
                    R.id.rbMaintain -> Constants.GOAL_MAINTAIN
                    R.id.rbGainMuscle -> Constants.GOAL_GAIN_MUSCLE
                    else -> Constants.GOAL_LOSE_WEIGHT
                }
                
                val activityLevel = when (rgActivity.checkedRadioButtonId) {
                    R.id.rbSedentary -> Constants.ACTIVITY_SEDENTARY
                    R.id.rbLightlyActive -> Constants.ACTIVITY_LIGHTLY_ACTIVE
                    R.id.rbModeratelyActive -> Constants.ACTIVITY_MODERATELY_ACTIVE
                    R.id.rbVeryActive -> Constants.ACTIVITY_VERY_ACTIVE
                    else -> Constants.ACTIVITY_SEDENTARY
                }

                if (validateProfileInput(age, height, weight)) {
                    viewModel.updateProfile(age, height, weight, goal, activityLevel)
                }
            }
            .setNegativeButton(R.string.btn_cancel, null)
            .show()
    }

    private fun validateProfileInput(age: Int, height: Int, weight: Double): Boolean {
        if (age < Constants.MIN_AGE || age > Constants.MAX_AGE) {
            Toast.makeText(requireContext(), R.string.error_invalid_age, Toast.LENGTH_SHORT).show()
            return false
        }
        if (height < Constants.MIN_HEIGHT || height > Constants.MAX_HEIGHT) {
            Toast.makeText(requireContext(), R.string.error_invalid_height, Toast.LENGTH_SHORT).show()
            return false
        }
        if (weight < Constants.MIN_WEIGHT || weight > Constants.MAX_WEIGHT) {
            Toast.makeText(requireContext(), R.string.error_invalid_weight, Toast.LENGTH_SHORT).show()
            return false
        }
        return true
    }

    private fun showLogoutConfirmation() {
        MaterialAlertDialogBuilder(requireContext())
            .setMessage(R.string.logout_confirm)
            .setPositiveButton(R.string.yes) { _, _ ->
                viewModel.signOut()
                navigateToLogin()
            }
            .setNegativeButton(R.string.no, null)
            .show()
    }

    private fun navigateToLogin() {
        val intent = Intent(requireContext(), LoginActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
        requireActivity().finish()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
