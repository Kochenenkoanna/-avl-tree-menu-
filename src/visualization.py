import random
import graphviz
from cw import MenuManager

dish_names = [
    "Суп харчо", "Куриные котлеты", "Салат греческий", "Суп-лапша", "Шашлык из свинины",
    "Плов узбекский", "Блины с мясом", "Окрошка на квасе", "Котлеты по-домашнему", "Гречка с грибами",
    "Жаркое по-русски", "Картофель по-деревенски", "Рыба в кляре", "Паста карбонара", "Рагу овощное",
    "Лазанья с мясом", "Омлет с сыром", "Солянка сборная", "Салат цезарь", "Куриный бульон",
    "Харчо по-грузински", "Рассольник домашний", "Голубцы с фаршем", "Вареники с картошкой", "Ребра BBQ",
    "Ризотто с грибами", "Картофель запеченный", "Суши ассорти", "Роллы Филадельфия", "Том Ям с креветками",
    "Баклажаны на гриле", "Картофельные драники", "Пицца Пепперони", "Торт Прага", "Кекс маффин",
    "Тирамису классический", "Печенье овсяное", "Маффины черничные", "Фондан шоколадный", "Эклеры заварные",
    "Пирог с вишней", "Морс клюквенный", "Смузи ягодный", "Капучино", "Чай зеленый",
    "Компот из сухофруктов", "Коктейль молочный", "Сок апельсиновый", "Вода газированная", "Молоко топленое"
]

def create_tree_visualization(root):
    graph = graphviz.Digraph(format="png")
    graph.attr('node', shape='circle', fontname='Arial', fontsize='10')
    
    def add_node(node, parent=None):
        if not node:
            return
        node_label = f"{node.name}\n({node.price}₽)"
        graph.node(node_label)
        
        if parent:
            graph.edge(parent, node_label)
            
        if node.left:
            add_node(node.left, node_label)
        if node.right:
            add_node(node.right, node_label)
    
    if root:
        add_node(root)
    
    return graph


def demonstrate_menu_operations():
    print("ДЕМОНСТРАЦИЯ AVL-ДЕРЕВА ДЛЯ МЕНЮ СТОЛОВОЙ 'МАРИЯ'")
    menu = MenuManager()
    print("\n1. ДОБАВЛЕНИЕ БЛЮД В МЕНЮ")
    print("-" * 40)
    
    added_dishes = []
    for _ in range(12):
        name = random.choice(dish_names)
        price = random.randint(50, 1000)
    
        if menu.get_price(name) is None:
            if menu.add(name, price):
                added_dishes.append((name, price))
                print(f"   ✓ {name:25} - {price:4d} руб.")
    
    print(f"\n   Всего блюд: {menu.count()}")
    print("\n2. ПОИСК БЛЮД В МЕНЮ")
    print("-" * 40)
    if added_dishes:
        for name, price in added_dishes[:3]:
            found_price = menu.get_price(name)
            if found_price:
                print(f"   ✓ {name:25} - {found_price:4d} руб.")

    for test_name in ["Суп харчо", "Пицца Пепперони", "Капучино"]:
        if menu.get_price(test_name) is None:
            print(f"   ✗ {test_name:25} - нет в меню")

    print("\n3. ОТСОРТИРОВАННОЕ МЕНЮ")
    print("-" * 40)
    print("   Название блюда                Цена")
    print("   " + "-" * 35)
    
    for name, price in menu:
        print(f"   {name:25} {price:5d} руб.")
    
    graph = create_tree_visualization(menu.root)
    graph.attr(label='AVL-дерево меню столовой "Мария"\n(Автоматическая сортировка по названию)',
              labelloc='t', fontsize='14', fontname='Arial')
    
    output_file = "avl_tree_visualization"
    graph.render(output_file, cleanup=True)

    print("\n4. УДАЛЕНИЕ БЛЮДА ИЗ МЕНЮ")
    print("-" * 40)
    
    if added_dishes:
        dish_to_remove_name, dish_to_remove_price = added_dishes[0]
        exists_before = menu.get_price(dish_to_remove_name) is not None
        menu.remove(dish_to_remove_name)
        exists_after = menu.get_price(dish_to_remove_name) is not None
        if exists_before and not exists_after:
            print(f"   ✓ Удалено: {dish_to_remove_name} ({dish_to_remove_price} руб.)")
            print(f"   ✓ Осталось блюд: {menu.count()}")
            print("\n   Оставшиеся блюда в меню:")
            remaining_dishes = []
            for name, price in menu:
                remaining_dishes.append((name, price))
            
            for i, (name, price) in enumerate(remaining_dishes[:10], 1):
                print(f"   {i:2}. {name:25} - {price:4d} руб.")
            
            if len(remaining_dishes) > 10:
                print(f"   ... и ещё {len(remaining_dishes) - 10} блюд")
        else:
            if not exists_before:
                print(f"   ✗ Блюдо {dish_to_remove_name} не найдено в меню")
            else:
                print(f"   Блюдо {dish_to_remove_name} все еще в меню (ошибка удаления)")


if __name__ == "__main__":
    demonstrate_menu_operations()