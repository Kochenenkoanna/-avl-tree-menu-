import pytest
from cw import Stack, TreeIterator, MenuManager
from cw import avl_insert, avl_search, avl_delete, avl_size, avl_height

class TestAVLMenu:
    def test_stack_empty(self):
        """1. Пустой стек"""
        stack = Stack()
        assert stack.is_empty()
        assert stack.size == 0
    
    def test_stack_push_pop(self):
        """2. Добавление и извлечение"""
        stack = Stack()
        stack.push("тест")
        assert stack.pop() == "тест"
        assert stack.is_empty()
    
    def test_stack_lifo(self):
        """3. Порядок LIFO"""
        stack = Stack()
        stack.push("первый")
        stack.push("второй")
        assert stack.pop() == "второй"
        assert stack.pop() == "первый"
    
    def test_stack_peek(self):
        """4. Peek не удаляет"""
        stack = Stack()
        stack.push("элемент")
        assert stack.peek() == "элемент"
        assert stack.size == 1
    
    def test_avl_insert_search(self):
        """5. Вставка и поиск"""
        root = None
        root = avl_insert(root, "Борщ", 150)
        root = avl_insert(root, "Суп", 120)
        
        assert avl_search(root, "Борщ").price == 150
        assert avl_search(root, "Суп").price == 120
        assert avl_search(root, "Нет") is None
    
    def test_avl_update_price(self):
        """6. Обновление цены"""
        root = None
        root = avl_insert(root, "Борщ", 150)
        root = avl_insert(root, "Борщ", 180)
        
        assert avl_search(root, "Борщ").price == 180
        assert avl_size(root) == 1
    
    def test_avl_delete(self):
        """7. Удаление элемента"""
        root = None
        root = avl_insert(root, "Борщ", 150)
        root = avl_insert(root, "Суп", 120)
        
        root = avl_delete(root, "Суп")
        assert avl_search(root, "Суп") is None
        assert avl_size(root) == 1
    
    def test_avl_delete_root(self):
        """8. Удаление корня"""
        root = None
        root = avl_insert(root, "Борщ", 150)
        root = avl_insert(root, "Ананас", 200)
        root = avl_insert(root, "Суп", 120)
        
        root = avl_delete(root, "Борщ")
        assert avl_search(root, "Борщ") is None
        assert avl_size(root) == 2
    
    def test_avl_balance_small(self):
        """9. Балансировка малого дерева"""
        root = None
        for letter in "abcde":
            root = avl_insert(root, f"Блюдо_{letter}", 100)
        
        assert avl_size(root) == 5
        assert avl_height(root) <= 3
    
    def test_avl_balance_large(self):
        """10. Балансировка большого дерева"""
        root = None
        for i in range(100):
            root = avl_insert(root, f"Блюдо_{i:03d}", 100 + i)
        
        from math import log2
        max_height = 1.44 * log2(100 + 2)
        assert avl_height(root) <= max_height
    
    def test_iterator_order(self):
        """11. Лексикографический порядок"""
        root = None
        dishes = [("Десерт", 200), ("Борщ", 150), ("Суп", 120)]
        for name, price in dishes:
            root = avl_insert(root, name, price)
        
        result = list(TreeIterator(root))
        expected = sorted(dishes, key=lambda x: x[0].lower())
        assert result == expected
    
    def test_iterator_empty(self):
        """12. Пустой итератор"""
        assert list(TreeIterator(None)) == []
    
    def test_iterator_all_elements(self):
        """13. Все элементы в итераторе"""
        root = None
        for i in range(10):
            root = avl_insert(root, f"Блюдо_{i}", 100 + i)
        
        result = list(TreeIterator(root))
        assert len(result) == 10
    
    def test_menu_empty(self):
        """14. Пустое меню"""
        menu = MenuManager()
        assert menu.count() == 0
        assert menu.get_price("Борщ") is None
    
    def test_menu_add_valid(self):
        """15. Добавление блюд"""
        menu = MenuManager()
        assert menu.add("Борщ", 150)
        assert menu.add("Суп", 120)
        assert menu.count() == 2
    
    def test_menu_add_invalid(self):
        """16. Некорректное добавление"""
        menu = MenuManager()
        assert not menu.add("Паста", 0)
        assert not menu.add("Пицца", -100)
        assert menu.count() == 0
    
    def test_menu_get_update(self):
        """17. Получение и обновление цены"""
        menu = MenuManager()
        menu.add("Борщ", 150)
        assert menu.get_price("Борщ") == 150
        
        menu.add("Борщ", 180)
        assert menu.get_price("Борщ") == 180
    
    def test_menu_remove(self):
        """18. Удаление блюд"""
        menu = MenuManager()
        menu.add("Борщ", 150)
        assert menu.remove("Борщ")
        assert not menu.remove("Нет")
        assert menu.count() == 0
    
    def test_menu_case_insensitive(self):
        """19. Регистронезависимость"""
        menu = MenuManager()
        menu.add("борщ", 150)
        menu.add("БОРЩ", 200)
        assert menu.count() == 1
        assert menu.get_price("борщ") == 200
    
    def test_menu_full_scenario(self):
        """20. Полный сценарий из задачи"""
        menu = MenuManager()
        
        dishes = [("Борщ", 150), ("Солянка", 180), ("Компот", 80)]
        for name, price in dishes:
            menu.add(name, price)
        
        assert menu.count() == 3
        assert menu.get_price("Борщ") == 150
        menu.add("Борщ", 170)
        menu.add("Чай", 50)
        menu.remove("Компот")
        
        assert menu.count() == 3
        assert menu.get_price("Борщ") == 170
        
        items = list(menu)
        assert len(items) == 3
        assert items == sorted(items, key=lambda x: x[0].lower())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])