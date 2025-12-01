# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.kts.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# Keep Firebase classes
-keep class com.google.firebase.** { *; }
-keep class com.fitgen.app.models.** { *; }
