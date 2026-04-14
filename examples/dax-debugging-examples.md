# DAX Debugging Examples

## Example 1: Incorrect total in a matrix

**Problem:**  
The row values look correct, but the total does not match the expected result.

**Original measure:**
```DAX
Open Cases =
IF(Operations[Status] = "Open", 1, 0)
```

**Improved measure:**
```DAX
Open Cases =
CALCULATE(
    COUNTROWS(Operations),
    Operations[Status] = "Open"
)
```

**AI-assisted value:**  
AI can help identify when a calculated-column style approach is being used where a measure is more appropriate.

---

## Example 2: Safe division for completion rate

**Problem:**  
The measure can fail or behave unexpectedly when the denominator is zero.

**Original measure:**
```DAX
Completion Rate = [Completed Items] / [Total Items]
```

**Improved measure:**
```DAX
Completion Rate =
DIVIDE([Completed Items], [Total Items], 0)
```

**AI-assisted value:**  
AI can quickly suggest safer DAX patterns and explain why they are preferred.

---

## Example 3: Average resolution days

**Measure:**
```DAX
Average Resolution Days =
AVERAGEX(
    FILTER(Operations, NOT(ISBLANK(Operations[CloseDate]))),
    DATEDIFF(Operations[OpenDate], Operations[CloseDate], DAY)
)
```

**AI-assisted value:**  
AI can help draft the formula and explain the logic, but human testing is still required.
