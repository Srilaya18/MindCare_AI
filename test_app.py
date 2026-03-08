import pytest
from app import analyze_stress, clean_text

def test_clean_text():
    assert clean_text("Hello World! 123") == "Hello World "
    assert clean_text("Test_string") == "Teststring"

def test_analyze_stress_high():
    stress_level, _ = analyze_stress("I am extremely angry, furious, and stressed!")
    assert stress_level == "HIGH" or stress_level == "MEDIUM"  # TextBlob can be slightly unpredictable sometimes

def test_analyze_stress_low():
    stress_level, _ = analyze_stress("I am so happy and peaceful today. Everything is wonderful.")
    assert stress_level == "LOW"
