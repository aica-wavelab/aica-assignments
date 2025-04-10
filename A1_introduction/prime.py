def isprime(n: int) -> bool:
  """Returns true if and only if n is a prime number.

  Args:
      n (int): a positive number

  Returns:
      bool: True if and only if n is prime.
  """
  assert n > 0
  
  if n == 1:
    return False

  if n == 2:
    return True
  
  for i in range(2,n):
    if n % i == 0:
      return False
    
  return True
