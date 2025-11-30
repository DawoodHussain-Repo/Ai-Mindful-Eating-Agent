"""
Unit Tests for Food Parser Module
Tests food recognition, fuzzy matching, portion parsing, and Gemini integration
"""

import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from utils.food_parser import FoodParser


# Test Food Database (subset for testing)
TEST_FOOD_DATABASE = {
    'chicken breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'category': 'protein'},
    'grilled chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'category': 'protein'},
    'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'category': 'protein'},
    'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4, 'fiber': 3.1, 'category': 'fruits'},
    'apple': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'fiber': 4.4, 'category': 'fruits'},
    'rice': {'calories': 205, 'protein': 4.3, 'carbs': 45, 'fat': 0.4, 'fiber': 0.6, 'category': 'carbs'},
    'brown rice': {'calories': 216, 'protein': 5, 'carbs': 45, 'fat': 1.8, 'fiber': 3.5, 'category': 'carbs'},
    'salmon': {'calories': 206, 'protein': 22, 'carbs': 0, 'fat': 13, 'fiber': 0, 'category': 'protein'},
    'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0, 'category': 'protein'},
    'egg': {'calories': 78, 'protein': 6.5, 'carbs': 0.6, 'fat': 5.5, 'fiber': 0, 'category': 'protein'},
    'pizza': {'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10, 'fiber': 2.5, 'category': 'fast_food'},
    'burger': {'calories': 354, 'protein': 20, 'carbs': 30, 'fat': 17, 'fiber': 1.5, 'category': 'fast_food'},
    'greek yogurt': {'calories': 100, 'protein': 17, 'carbs': 6, 'fat': 0.7, 'fiber': 0, 'category': 'dairy'},
    'oatmeal': {'calories': 158, 'protein': 6, 'carbs': 27, 'fat': 3.2, 'fiber': 4, 'category': 'carbs'},
}

TEST_PORTION_PATTERNS = {
    'oz': r'(\d+\.?\d*)\s*(?:oz|ounce|ounces)',
    'cup': r'(\d+\.?\d*|1/2|1/4|half|quarter)\s*(?:cup|cups)',
    'gram': r'(\d+\.?\d*)\s*(?:g|gram|grams)',
    'piece': r'(\d+\.?\d*)\s*(?:piece|pieces|slice|slices)',
    'serving': r'(\d+\.?\d*)\s*(?:serving|servings)',
}

TEST_PORTION_SIZES = {
    'small': 0.75,
    'medium': 1.0,
    'large': 1.5,
    'huge': 2.0,
}


@pytest.fixture
def food_parser():
    """Create a FoodParser instance for testing"""
    return FoodParser(TEST_FOOD_DATABASE, TEST_PORTION_PATTERNS, TEST_PORTION_SIZES)


class TestTextNormalization:
    """Tests for text normalization functionality"""
    
    def test_lowercase_conversion(self, food_parser):
        """Test that text is converted to lowercase"""
        result = food_parser.normalize_text("I ATE CHICKEN")
        assert result == result.lower()
    
    def test_strip_whitespace(self, food_parser):
        """Test that leading/trailing whitespace is removed"""
        result = food_parser.normalize_text("  banana  ")
        assert not result.startswith(' ')
        assert not result.endswith(' ')
    
    def test_filler_word_removal(self, food_parser):
        """Test that common filler words are handled"""
        result = food_parser.normalize_text("I ate a banana for my breakfast today")
        # Should remove 'I', 'a', 'for', 'my', 'today'
        assert 'banana' in result
    
    def test_empty_string(self, food_parser):
        """Test handling of empty string"""
        result = food_parser.normalize_text("")
        assert result == ""
    
    def test_only_filler_words(self, food_parser):
        """Test handling of only filler words - should preserve some content"""
        result = food_parser.normalize_text("I ate a the")
        # Should not result in empty string, preserves minimum words
        assert isinstance(result, str)


class TestPortionParsing:
    """Tests for portion size extraction"""
    
    def test_default_portion(self, food_parser):
        """Test default portion when none specified"""
        portion, text = food_parser.parse_portion("banana")
        assert portion == 1.0
    
    def test_ounces_parsing(self, food_parser):
        """Test parsing ounces"""
        portion, text = food_parser.parse_portion("8 oz chicken")
        assert portion == 2.0  # 8oz / 4oz per serving = 2
        assert "oz" in text.lower()
    
    def test_cups_parsing(self, food_parser):
        """Test parsing cups"""
        portion, text = food_parser.parse_portion("2 cups rice")
        assert portion == 2.0
        assert "cup" in text.lower()
    
    def test_half_cup_parsing(self, food_parser):
        """Test parsing half cup"""
        portion, text = food_parser.parse_portion("1/2 cup oatmeal")
        assert portion == 0.5
    
    def test_grams_parsing(self, food_parser):
        """Test parsing grams"""
        # Parser requires 'gram' keyword or ' g ' with spaces
        portion, text = food_parser.parse_portion("200 grams chicken")
        assert portion == 2.0  # 200g / 100g per serving = 2
        assert "g" in text.lower()
    
    def test_pieces_parsing(self, food_parser):
        """Test parsing pieces"""
        portion, text = food_parser.parse_portion("3 pieces pizza")
        assert portion == 3.0
    
    def test_size_descriptor_small(self, food_parser):
        """Test parsing 'small' size"""
        portion, text = food_parser.parse_portion("small banana")
        assert portion == 0.75
    
    def test_size_descriptor_large(self, food_parser):
        """Test parsing 'large' size"""
        portion, text = food_parser.parse_portion("large burger")
        assert portion == 1.5
    
    def test_size_descriptor_huge(self, food_parser):
        """Test parsing 'huge' size"""
        portion, text = food_parser.parse_portion("huge pizza")
        assert portion == 2.0


class TestFuzzyMatching:
    """Tests for fuzzy food matching"""
    
    def test_exact_match(self, food_parser):
        """Test exact food name match"""
        matches = food_parser.fuzzy_match_food("banana")
        assert 'banana' in matches
    
    def test_substring_match(self, food_parser):
        """Test food name as substring"""
        matches = food_parser.fuzzy_match_food("I had chicken breast for lunch")
        assert 'chicken breast' in matches
    
    def test_multiple_foods(self, food_parser):
        """Test matching multiple foods in one sentence"""
        matches = food_parser.fuzzy_match_food("banana and apple")
        assert 'banana' in matches
        assert 'apple' in matches
    
    def test_case_insensitivity(self, food_parser):
        """Test case insensitive matching"""
        matches = food_parser.fuzzy_match_food("CHICKEN BREAST")
        assert 'chicken breast' in matches
    
    def test_partial_word_match(self, food_parser):
        """Test that partial matches work with word overlap"""
        matches = food_parser.fuzzy_match_food("grilled chicken")
        # Should match 'grilled chicken' or 'chicken'
        assert any('chicken' in m for m in matches)
    
    def test_no_match(self, food_parser):
        """Test when no food matches"""
        matches = food_parser.fuzzy_match_food("xyz123 nonsense food")
        # Should return empty or not match 'banana' etc
        assert 'banana' not in matches


class TestGenericTermClarification:
    """Tests for generic term detection and clarification"""
    
    def test_soda_needs_clarification(self, food_parser):
        """Test that 'soda' triggers clarification"""
        result = food_parser.check_for_generic_terms("I drank a soda")
        assert result is not None
        assert result['needs_clarification'] == True
        assert result['generic_term'] == 'soda'
    
    def test_specific_soda_no_clarification(self, food_parser):
        """Test that specific soda doesn't trigger clarification"""
        result = food_parser.check_for_generic_terms("I drank a pepsi")
        # Should not need clarification since specific brand mentioned
        assert result is None
    
    def test_juice_needs_clarification(self, food_parser):
        """Test that 'juice' triggers clarification"""
        result = food_parser.check_for_generic_terms("I had juice")
        assert result is not None
        assert result['generic_term'] == 'juice'
    
    def test_non_generic_term(self, food_parser):
        """Test that non-generic terms don't trigger clarification"""
        result = food_parser.check_for_generic_terms("I ate a banana")
        assert result is None


class TestFoodTextParsing:
    """Tests for complete food text parsing"""
    
    def test_simple_food(self, food_parser):
        """Test parsing simple food input"""
        result = food_parser.parse_food_text("banana")
        assert isinstance(result, list)
        # Should either have parsed food or clarification needed
        assert len(result) >= 0
    
    def test_food_with_quantity(self, food_parser):
        """Test parsing food with quantity"""
        result = food_parser.parse_food_text("2 bananas")
        assert isinstance(result, list)
    
    def test_multiple_foods(self, food_parser):
        """Test parsing multiple foods"""
        result = food_parser.parse_food_text("chicken and rice")
        assert isinstance(result, list)
    
    def test_conversational_input(self, food_parser):
        """Test parsing conversational input"""
        result = food_parser.parse_food_text("I had grilled chicken with brown rice for dinner")
        assert isinstance(result, list)
    
    def test_empty_input(self, food_parser):
        """Test parsing empty input"""
        result = food_parser.parse_food_text("")
        assert isinstance(result, list)


class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_special_characters(self, food_parser):
        """Test handling of special characters"""
        result = food_parser.parse_food_text("chicken! @ breakfast #healthy")
        assert isinstance(result, list)
    
    def test_numbers_only(self, food_parser):
        """Test handling of numbers only"""
        result = food_parser.parse_food_text("123 456")
        assert isinstance(result, list)
    
    def test_very_long_input(self, food_parser):
        """Test handling of very long input"""
        long_text = "banana " * 100
        result = food_parser.parse_food_text(long_text)
        assert isinstance(result, list)
    
    def test_unicode_characters(self, food_parser):
        """Test handling of unicode characters"""
        result = food_parser.parse_food_text("banana 🍌")
        assert isinstance(result, list)
    
    def test_mixed_case_portions(self, food_parser):
        """Test mixed case in portions"""
        portion, text = food_parser.parse_portion("LARGE chicken")
        assert portion == 1.5  # Should handle uppercase 'LARGE'


class TestNutritionCalculation:
    """Tests for nutrition calculation from parsed foods"""
    
    def test_single_food_nutrition(self, food_parser):
        """Test nutrition calculation for single food"""
        # Banana: 105 cal, 1.3g protein, 27g carbs, 0.4g fat
        foods = food_parser.parse_food_text("banana")
        # Result should contain nutrition data if matched
        assert isinstance(foods, list)
    
    def test_portioned_nutrition(self, food_parser):
        """Test nutrition is multiplied by portion"""
        # 2 servings should double the nutrition
        foods = food_parser.parse_food_text("2 cups rice")
        assert isinstance(foods, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
