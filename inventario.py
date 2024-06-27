import numpy as np

# Parámetros del sistema
Q = 200  # Cantidad de pedido
r = 150  # Punto de reorden
initial_inventory = 300  # Inventario inicial
Co = 100  # Costo de realizar un pedido
Ch = 2  # Costo de mantener inventario por unidad por día
Cs = 5  # Costo de faltante por unidad no satisfecha
mu = 50  # Media de la demanda diaria
sigma = 10  # Desviación estándar de la demanda diaria
L = 3  # Tiempo de entrega en días
days = 30  # Periodo de simulación en días

# Variables de estado
inventory = initial_inventory
total_cost = 0
order_costs = 0
holding_costs = 0
shortage_costs = 0
pending_orders = []

# Simulación
for day in range(1, days + 1):
    # Generar demanda diaria
    demand = max(0, np.random.normal(mu, sigma))
    
    # Actualizar inventario
    if inventory >= demand:
        inventory -= demand
        unsatisfied_demand = 0
    else:
        unsatisfied_demand = demand - inventory
        inventory = 0
    
    # Calcular costos de faltantes
    shortage_costs += unsatisfied_demand * Cs
    
    # Revisión del punto de reorden
    if inventory < r:
        pending_orders.append((day + L, Q))
        order_costs += Co

    # Recepción de pedidos pendientes
    pending_orders = [(arrival_day, quantity) for (arrival_day, quantity) in pending_orders if arrival_day != day]
    for (arrival_day, quantity) in pending_orders:
        if arrival_day == day:
            inventory += quantity
    
    # Calcular costos de mantenimiento
    holding_costs += inventory * Ch
    
    # Guardar inventario diario para análisis
    daily_inventory.append(inventory)
    
# Calcular costo total
total_cost = order_costs + holding_costs + shortage_costs

# Imprimir resultados
print(f"Total de costos de orden: ${order_costs:.2f}")
print(f"Total de costos de mantenimiento: ${holding_costs:.2f}")
print(f"Total de costos de faltantes: ${shortage_costs:.2f}")
print(f"Costo total del sistema: ${total_cost:.2f}")
print(f"Inventario final: {inventory} unidades")
