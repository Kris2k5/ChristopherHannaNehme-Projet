package com.fitgen.app.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import com.fitgen.app.R
import com.fitgen.app.databinding.FragmentHomeBinding
import com.fitgen.app.viewmodels.UserViewModel

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    private val viewModel: UserViewModel by activityViewModels()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        observeViewModel()
    }

    private fun observeViewModel() {
        viewModel.user.observe(viewLifecycleOwner) { user ->
            user?.let {
                val displayName = viewModel.getDisplayName()
                binding.tvWelcome.text = getString(R.string.welcome_message, displayName)
            }
        }

        viewModel.dailyCalories.observe(viewLifecycleOwner) { calories ->
            binding.tvCalorieGoal.text = getString(R.string.calories_format, calories)
        }

        viewModel.bmr.observe(viewLifecycleOwner) { bmr ->
            binding.tvBMR.text = getString(R.string.calories_format, bmr)
        }

        viewModel.bmi.observe(viewLifecycleOwner) { bmi ->
            binding.tvBMI.text = getString(R.string.bmi_format, bmi)
        }

        viewModel.bmiClassification.observe(viewLifecycleOwner) { classification ->
            val (text, color) = when (classification) {
                "underweight" -> Pair(getString(R.string.bmi_underweight), R.color.bmi_underweight)
                "normal" -> Pair(getString(R.string.bmi_normal), R.color.bmi_normal)
                "overweight" -> Pair(getString(R.string.bmi_overweight), R.color.bmi_overweight)
                "obese" -> Pair(getString(R.string.bmi_obese), R.color.bmi_obese)
                else -> Pair("", R.color.text_secondary)
            }
            binding.tvBMIClassification.text = text
            binding.tvBMIClassification.setTextColor(ContextCompat.getColor(requireContext(), color))
            binding.tvBMI.setTextColor(ContextCompat.getColor(requireContext(), color))
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
