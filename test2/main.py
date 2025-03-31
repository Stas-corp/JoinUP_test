def distribute_value(numbers, total_value):
    total_sum = sum(numbers)
    proportions = [num / total_sum for num in numbers]
    proportion_values = [round(prop * total_value) for prop in proportions]
    difference = total_value - sum(proportion_values)
    sorted_indices = sorted(range(len(numbers)), key=lambda i: proportions[i], reverse=True)
    for i in range(abs(difference)):
        proportion_values[sorted_indices[i]] += 1 if difference > 0 else -1
    return proportion_values

numbers = [535, 418, 623, 418, 733]
total_value = 290

print(distribute_value(numbers, total_value))