import random
import time
import matplotlib.pyplot as plt
import numpy as np
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

def generate_dish_data(size, case='average'):
    """Генерация данных с реальными названиями блюд"""
    data = []
    
    if case == 'best':
        for i in range(size):
            base_name = dish_names[i % len(dish_names)]
            name = f"{base_name} #{i+1}"
            price = random.randint(100, 500)
            data.append((name, price))
        random.shuffle(data)
        
    elif case == 'worst':
        for i in range(size):
            letter = chr(ord('А') + (i // 100))
            num = i % 100
            name = f"{letter} Блюдо {num:03d}"
            price = random.randint(100, 500)
            data.append((name, price))
        data.sort(key=lambda x: x[0])
        
    else:  
        for i in range(size):
            base_name = random.choice(dish_names)
            name = f"{base_name} #{i+1}"
            price = random.randint(100, 500)
            data.append((name, price))
        random.shuffle(data)
    
    return data

def measure_insert_time(size, case='average'):
    manager = MenuManager()
    data = generate_dish_data(size, case)
    start_time = time.perf_counter()
    for name, price in data:
        manager.add(name, price)
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    return total_time / size if size > 0 else 0

def measure_search_time(size, case='average'):
    manager = MenuManager()
    data = generate_dish_data(size, case)
    
    for name, price in data:
        manager.add(name, price)

    num_searches = min(100, max(10, size // 10))
    search_names = []
    for _ in range(num_searches):
        if random.random() < 0.8:  
            name, _ = random.choice(data)
        else: 
            name = f"Несуществующее блюдо {random.randint(100000, 999999)}"
        search_names.append(name)
    start_time = time.perf_counter()
    for name in search_names:
        manager.get_price(name)
    end_time = time.perf_counter()
    
    return (end_time - start_time) / num_searches

def measure_delete_time_fixed(size, case='average', num_measurements=50):
    total_time = 0
    for _ in range(num_measurements):
        manager = MenuManager()
        data = generate_dish_data(size, case)
        
        all_names = []
        for name, price in data:
            manager.add(name, price)
            all_names.append(name)
        delete_name = random.choice(all_names)
        start_time = time.perf_counter()
        manager.remove(delete_name)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)
    
    return total_time / num_measurements

def measure_traversal_time(size, case='average'):
    manager = MenuManager()
    data = generate_dish_data(size, case)
    for name, price in data:
        manager.add(name, price)
    start_time = time.perf_counter()
    for _ in manager:
        pass
    end_time = time.perf_counter()
    
    return end_time - start_time 

def run_benchmark():
    operations = ['insert', 'search', 'delete', 'traversal']
    cases = ['best', 'average', 'worst']
    case_symbols = {'best': 'л', 'average': 'с', 'worst': 'х'}
    
    sizes = [10, 50, 100, 200, 500, 1000]
    results = {}
    
    for op in operations:
        results[op] = {}
        for case in cases:
            results[op][case] = []
        
        print(f"\nИзмерение: {op}")
        for size in sizes:
            print(f"  n={size:4}: ", end="")
            
            for case in cases:
                total_time = 0
                iterations = 5  
                
                for _ in range(iterations):
                    if op == 'insert':
                        time_val = measure_insert_time(size, case)
                    elif op == 'search':
                        time_val = measure_search_time(size, case)
                    elif op == 'delete':
                        time_val = measure_delete_time_fixed(size, case)
                    elif op == 'traversal':
                        time_val = measure_traversal_time(size, case)
                    
                    total_time += time_val
                
                avg_time = total_time / iterations
                results[op][case].append(avg_time)
                
                symbol = case_symbols[case]
                if op == 'traversal':
                    if avg_time < 0.001:
                        print(f"{symbol}:{avg_time*1000:6.2f}мс ", end="")
                    else:
                        print(f"{symbol}:{avg_time:6.4f}с ", end="")
                else:
                    if avg_time < 0.000001:
                        print(f"{symbol}:{avg_time*1e6:6.1f}µс ", end="")
                    elif avg_time < 0.001:
                        print(f"{symbol}:{avg_time*1000:6.3f}мс ", end="")
                    else:
                        print(f"{symbol}:{avg_time:7.6f}с ", end="")
            
            print()
    
    return results, sizes

def create_separate_plots(results, sizes):
    """Создает 4 отдельных графика (по одному на операцию)"""
    
    operations = ['insert', 'search', 'delete', 'traversal']
    
    operation_names = {
        'insert': 'Вставка',
        'search': 'Поиск', 
        'delete': 'Удаление',
        'traversal': 'Обход'
    }
    
    case_names = {
        'best': 'Лучший случай',
        'average': 'Средний случай', 
        'worst': 'Худший случай'
    }
    
    colors = {'best': 'green', 'average': 'blue', 'worst': 'red'}
    markers = {'best': 'o', 'average': 's', 'worst': '^'}
    
    for op in operations:
        plt.figure(figsize=(10, 7))
        for case in ['best', 'average', 'worst']:
            times = results[op][case]
            plt.plot(sizes, times, marker=markers[case], linewidth=2,
                    markersize=8, label=case_names[case], color=colors[case])
        
        if op == 'traversal':
            if len(results[op]['average']) > 2 and sizes[2] > 0:
                scale_factor = results[op]['average'][2] / sizes[2]
                theoretical = [scale_factor * n for n in sizes]
                plt.plot(sizes, theoretical, 'k--', linewidth=2, alpha=0.7, 
                         label='Теоретическая O(n)')
        else:
            if len(results[op]['average']) > 2 and sizes[2] > 0:
                n_log = [np.log2(max(2, n)) for n in sizes]
                scale_factor = results[op]['average'][2] / n_log[2]
                theoretical = [scale_factor * nl for nl in n_log]
                plt.plot(sizes, theoretical, 'k--', linewidth=2, alpha=0.7, 
                         label='Теоретическая O(log n)')
        
        plt.xlabel('Количество элементов, n', fontsize=12)
        
        if op == 'traversal':
            plt.ylabel('Время полного обхода, с', fontsize=12)
            plt.yscale('linear')
            plt.xscale('linear')
        else:
            plt.ylabel('Среднее время на операцию, с', fontsize=12)
            plt.yscale('log')
            plt.xscale('log')
            plt.gca().xaxis.set_major_formatter(plt.ScalarFormatter())
            plt.gca().xaxis.set_minor_formatter(plt.NullFormatter())
        
        plt.title(f'Операция {operation_names[op]} - AVL-дерево', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3, which='both', linestyle='--', linewidth=0.5)
        
        filename = f"avl_{op}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
if __name__ == "__main__":
    results, sizes = run_benchmark()
    create_separate_plots(results, sizes)