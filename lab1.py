import math
import time
import matplotlib.pyplot as plt

class BigNumber:
    def __init__(self, value=0):
        if isinstance(value, str):
            self.value = int(value, 16) if value.startswith("0x") else int(value)
        elif isinstance(value, int):
            self.value = value
        else:
            raise ValueError("Непідтримуваний тип для ініціалізації BigNumber")

    def to_hex(self):
        return hex(self.value)

    def to_bin(self):
        return bin(self.value)

    def to_dec(self):
        return str(self.value)

    @staticmethod
    def from_string(value: str, base: int = 10):
        return BigNumber(int(value, base))

    def __add__(self, other):
        return BigNumber(self.value + other.value)

    def __sub__(self, other):
        return BigNumber(self.value - other.value)

    def __mul__(self, other):
        return BigNumber(self.value * other.value)

    def __rmul__(self, other):
        if isinstance(other, int):
            return BigNumber(self.value * other)
        raise ValueError("Множення підтримується лише для цілих чисел і BigNumber")

    def __floordiv__(self, other):
        return BigNumber(self.value // other.value)

    def __mod__(self, other):
        return BigNumber(self.value % other.value)

    def __pow__(self, exp):
        return BigNumber(pow(self.value, exp.value))

    def bit_length(self):
        return self.value.bit_length()

    def shift_left(self, n):
        return BigNumber(self.value << n)

    def shift_right(self, n):
        return BigNumber(self.value >> n)

# Завдання Б: Тести на коректність
def validate_identities():
    a = BigNumber(123456789012345678901234567890)
    b = BigNumber(987654321098765432109876543210)
    c = BigNumber(111111111111111111111111111111)

    assert ((a + b) * c).value == (a * c + b * c).value, "Помилка у формулі 1"

    n = 100
    assert (n * a).value == sum([a.value for _ in range(n)]), "Помилка у формулі 2"

    print("Формули перевірено успішно!")

# Завдання В: Обчислення часу виконання операцій
def benchmark_operations():
    a = BigNumber(2**1024)
    b = BigNumber(2**512)

    operations = {
        "Додавання": lambda: a + b,
        "Віднімання": lambda: a - b,
        "Множення": lambda: a * b,
        "Ділення": lambda: a // b,
        "Залишок від ділення": lambda: a % b,
        "Зсув вліво": lambda: a.shift_left(10),
        "Зсув вправо": lambda: a.shift_right(10),
    }

    results = {}

    for op_name, operation in operations.items():
        start_time = time.perf_counter()
        for _ in range(1000):
            operation()
        end_time = time.perf_counter()

        avg_time = (end_time - start_time) / 1000
        results[op_name] = avg_time

    return results

# Побудова діаграми
def plot_cycles(operation_times, cpu_frequency_hz=3 * 10**9):
    operation_cycles = {op: int(time * cpu_frequency_hz) for op, time in operation_times.items()}

    operations = list(operation_cycles.keys())
    cycles = list(operation_cycles.values())

    plt.figure(figsize=(10, 6))
    plt.bar(operations, cycles, color='orange')
    plt.title("Кількість тактів процесора на операцію")
    plt.ylabel("Кількість тактів")
    plt.xlabel("Операція")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Виконання тестів
validate_identities()

# Обчислення часу операцій
times = benchmark_operations()
for operation, avg_time in times.items():
    print(f"{operation}: {avg_time:.6f} секунд")

# Побудова діаграми
plot_cycles(times)
