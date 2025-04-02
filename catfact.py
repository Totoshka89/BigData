import pytest
from unittest.mock import patch, MagicMock
from cat_fact_processor import CatFactProcessor, APIError

class TestCatFactProcessor:
    """Пушистые тесты для CatFactProcessor 🐱"""
    
    def test_get_fact_success(self):
        """Тест-котёнок: успешное получение факта"""
        # Подготовка
        processor = CatFactProcessor()
        mock_response = MagicMock()
        mock_response.json.return_value = {"fact": "Cats are awesome!"}
        mock_response.raise_for_status.return_value = None
        
        # Действие (с моком API)
        with patch('requests.get', return_value=mock_response):
            fact = processor.get_fact()
        
        # Проверка
        assert fact == "Cats are awesome!"
        assert processor.last_fact == "Cats are awesome!"

    def test_get_fact_api_failure(self):
        """Тест-котик: проверяем падение при ошибке API 😿"""
        processor = CatFactProcessor()
        
        # Действие (мок с исключением)
        with patch('requests.get', side_effect=requests.exceptions.RequestException("Ой, котик сломал API")):
            with pytest.raises(APIError) as exc_info:
                processor.get_fact()
        
        # Проверка
        assert "Ошибка при запросе к API" in str(exc_info.value)

    def test_get_fact_analysis_empty(self):
        """Тест-кот: анализ пустого факта (кот ещё не намяукал)"""
        processor = CatFactProcessor()
        analysis = processor.get_fact_analysis()
        
        assert analysis["length"] == 0
        assert analysis["letter_frequencies"] == {}

    def test_get_fact_analysis_with_fact(self):
        """Тест-котэ: анализ настоящего кошачьего факта 🐾"""
        processor = CatFactProcessor()
        processor.last_fact = "Meow World"
        
        analysis = processor.get_fact_analysis()
        
        # Основные проверки
        assert analysis["length"] == 10
        assert analysis["letter_frequencies"]["m"] == 2
        assert analysis["letter_frequencies"]["e"] == 1
        assert analysis["letter_frequencies"]["o"] == 2
        assert " " in analysis["letter_frequencies"]  # Проверяем пробелы

    def test_letter_frequencies_case_insensitive(self):
        """Тест-киса: проверяем, что регистр букв не важен (котики не любят капс)"""
        processor = CatFactProcessor()
        processor.last_fact = "Cat CAT cat"
        
        analysis = processor.get_fact_analysis()
        
        assert analysis["letter_frequencies"]["c"] == 3
        assert analysis["letter_frequencies"]["a"] == 3
        assert analysis["letter_frequencies"]["t"] == 3

    @patch('requests.get')
    def test_json_format_error(self, mock_get):
        """Тест-котёнок: API вернул неожиданный формат (котик наступил на клавиатуру)"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"wrong": "format"}
        mock_get.return_value = mock_response
        
        processor = CatFactProcessor()
        
        with pytest.raises(APIError) as exc_info:
            processor.get_fact()
        
        assert "Ошибка при обработке ответа API" in str(exc_info.value)