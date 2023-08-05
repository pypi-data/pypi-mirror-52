# Timeself

**Description**

Timeself is intended to measure and print, the caller script, execution time.

**Installation**

`pip install timeself`

**Usage example**

```
from timeself import timeself


def is_five_divisible(num):
	if num % 5 == 0:
		return True
	else:
		return False


print(is_five_divisible(20))
timeself()  # Must be the last line on the script.

# Output

Execution time: 2.2221007384359837e-05
```
