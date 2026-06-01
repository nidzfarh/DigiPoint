from django import template

register = template.Library()


@register.filter
def inr_currency(value):
    """Format value as Indian Rupee currency with proper formatting.
    
    Examples:
    - 499 → ₹499
    - 1299 → ₹1,299
    - 54999 → ₹54,999
    - 100000 → ₹1,00,000
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return "₹0"
    
    # Format as integer if no decimal places
    if value == int(value):
        value = int(value)
    
    # Convert to string for manipulation
    value_str = str(value)
    
    # Handle decimal point
    if '.' in value_str:
        parts = value_str.split('.')
        integer_part = parts[0]
        decimal_part = parts[1][:2]  # Keep only 2 decimal places
    else:
        integer_part = value_str
        decimal_part = ''
    
    # Add Indian comma formatting (groups of 2 from right, then 3)
    # Example: 1000000 → 10,00,000
    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        # Reverse the string to process from right to left
        reversed_str = integer_part[::-1]
        groups = []
        
        # First group of 3 digits (from right)
        groups.append(reversed_str[:3])
        remaining = reversed_str[3:]
        
        # Remaining groups of 2 digits
        for i in range(0, len(remaining), 2):
            groups.append(remaining[i:i+2])
        
        # Reverse back and join with commas
        formatted = ','.join(groups[::-1])
    
    # Add decimal part if exists
    if decimal_part:
        formatted = f"{formatted}.{decimal_part}"
    
    return f"₹{formatted}"
