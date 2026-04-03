import pandas as pd
import numpy as np
import re

def parse_salary_range(salary_str):
    """Parse salary range string and return min, max, and validity flag"""
    if pd.isna(salary_str) or salary_str == 'nan':
        return np.nan, np.nan, 'missing'
    
    salary_str = str(salary_str).replace(',', '').replace(' ', '')
    
    if salary_str == '0-0':
        return 0, 0, 'zero_range'
    
    if re.match(r'^\w+-\w+$', salary_str) and any(month in salary_str for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
        return np.nan, np.nan, 'date_error'
    
    if '-' not in salary_str:
        try:
            val = float(salary_str)
            return val, val, 'single_value'
        except:
            return np.nan, np.nan, 'parse_error'
    
    try:
        parts = salary_str.split('-')
        if len(parts) == 2:
            min_sal = float(parts[0])
            max_sal = float(parts[1])
            
            # Check for reversed ranges
            if min_sal > max_sal:
                return max_sal, min_sal, 'reversed_range'
            
            # Check for unrealistic ranges
            if max_sal > 1e9:  # More than 1 billion
                return min_sal, max_sal, 'unrealistic_high'
            
            if max_sal < 100 and max_sal > 0:  # Likely hourly rate
                return min_sal, max_sal, 'likely_hourly'
            
            return min_sal, max_sal, 'valid'
        else:
            return np.nan, np.nan, 'parse_error'
    except:
        return np.nan, np.nan, 'parse_error'
      
def extract_country_from_location(location):
  """Extract country from location string"""
  if pd.isna(location):
      return 'Unknown'
  
  # Common patterns
  location = str(location).strip()
  
  # Check for country codes or full country names at the end
  parts = location.split(',')
  if len(parts) > 0:
      last_part = parts[-1].strip()
      
      # Map common country indicators
      country_map = {
          'US': 'USD', 'USA': 'USD', 'United States': 'USD',
          'UK': 'GBP', 'GB': 'GBP', 'United Kingdom': 'GBP',
          'CA': 'CAD', 'Canada': 'CAD',
          'AU': 'AUD', 'Australia': 'AUD',
          'IN': 'INR', 'India': 'INR',
          'DE': 'EUR', 'Germany': 'EUR',
          'FR': 'EUR', 'France': 'EUR',
          # Add more mappings as needed
      }
      
      return country_map.get(last_part, 'Unknown')
  
  return 'Unknown'
