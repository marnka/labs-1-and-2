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

    def gcd(self, other):
        return BigNumber(math.gcd(self.value, other.value))

    def lcm(self, other):
        return BigNumber((self.value * other.value) // math.gcd(self.value, other.value))

    def add_mod(self, other, mod):
        return BigNumber((self.value + other.value) % mod.value)

    def sub_mod(self, other, mod):
        return BigNumber((self.value - other.value) % mod.value)

    def mul_mod(self, other, mod):
        return BigNumber((self.value * other.value) % mod.value)

    def square_mod(self, mod):
        return BigNumber((self.value ** 2) % mod.value)

    def pow_mod(self, exp, mod):
        result = 1
        base = self.value
        exponent = exp.value
        modulo = mod.value

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulo
            base = (base * base) % modulo
            exponent //= 2

        return BigNumber(result)

    def modular_inverse(self, mod):
        g, x, _ = self.extended_gcd(self.value, mod.value)
        if g != 1:
            raise ValueError("Обернений елемент не існує")
        return BigNumber(x % mod.value)

    @staticmethod
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = BigNumber.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

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
    mod = BigNumber(2**256 - 1)

    operations = {
        "НСД": lambda: a.gcd(b),
        "НСК": lambda: a.lcm(b),
        "Додавання за модулем": lambda: a.add_mod(b, mod),
        "Віднімання за модулем": lambda: a.sub_mod(b, mod),
        "Множення за модулем": lambda: a.mul_mod(b, mod),
        "Піднесення до квадрату за модулем": lambda: a.square_mod(mod),
        "Піднесення до степеня за модулем": lambda: a.pow_mod(b, mod),
        "Обернений елемент": lambda: a.modular_inverse(mod)
    }

    results = {}

    for op_name, operation in operations.items():
        start_time = time.perf_counter()
        for _ in range(100):
            operation()
        end_time = time.perf_counter()

        avg_time = (end_time - start_time) / 100
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
